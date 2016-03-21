'''
EPICS template (substitutions) file analysis
'''

import os

import database
import macros
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions
from utils import logMessage, FileRef


class DatabaseTemplateException(Exception): pass


class Template(object):
    '''
    EPICS template (substitutions) file
    
    Template files contain one or more database groups, 
    each containing one or more EPICS PV declarations.
    It is implied that each PV declaration is a call to 
    ``dbLoadRecords`` where the database is specified 
    in the database group header.
    '''
    
    def __init__(self, filename, env):
        self.filename = filename
        self.macros = macros.Macros(env)
        self.database_list = []
        self.reference_list = []
        self.reference = None       # TODO: Make the definition and usage of this term clearer

        self.source = text_file.read(self.macros.replace(filename))
        self.parse()
    
    def parse(self):
        '''
        interpret the template file for database declarations
        
        The Python tokenizer makes simple work of parsing database files.
        The TokenLog class interprets the contents according to a few simple terms
        such as NAME, OP, COMMENT, NEWLINE.
        '''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename)
        tok = tokenLog.nextActionable()
        actions = {
                   'NAME file': self._parse_file_statement,
                   'NAME global': self._parse_globals_statement,
                   }
        while tok is not None:
            tk = token_key(tok)
            if tk in actions:
                actions[tk](tokenLog)
            tok = tokenLog.nextActionable()
    
    def _parse_file_statement(self, tokenLog):
        '''
        support the *file* statement in a template file
        
        example::
        
            file "$(SSCAN)/sscanApp/Db/scanParms.db"
        
        '''
        tok = tokenLog.getCurrentToken()
        ref = FileRef(self.filename, tok['start'][0], tok['start'][1], 'database file')
        # TODO: Do something with ref
        
        tok = tokenLog.nextActionable()
        dbFileName = tokenLog.getFullWord().strip('"')
        fname = self.macros.replace(dbFileName)
        if dbFileName == fname:
            ref = FileRef(self.filename, tok['start'][0], tok['start'][1], dbFileName)
        else:
            ref = FileRef(self.filename, tok['start'][0], tok['start'][1], dbFileName + ' -> ' + fname)
        # TODO: Do something with ref

        tok = tokenLog.nextActionable()

        # When there is a "pattern" statement, the macro labels are given first, then values in each declaration
        pattern_keys = []
        if token_key(tok) == 'NAME pattern':
            tok = tokenLog.nextActionable()
            pattern_keys = tokenLog.tokens_to_list()
            tok = tokenLog.nextActionable()     # skip past the closing }
        
        while token_key(tok) != 'OP }':
            tok_ref = tok

            # define the macros for this set
            pattern_macros = macros.Macros(self.macros.getAll())
            if len(pattern_keys) > 0:
                # The macro labels were defined in a pattern statement
                value_list = tokenLog.tokens_to_list()
                kv = dict(zip(pattern_keys, value_list))
                pattern_macros.setMany(kv)
                tok = tokenLog.nextActionable()
            else:
                # No pattern statement, macro labels are defined with the values
                tok = tokenLog.getCurrentToken()
                kv = tokenLog.getKeyValueSet()
                pattern_macros.setMany(kv)
                tok = tokenLog.nextActionable()
            
            dbg = database.Database(self, fname, pattern_macros.getAll())
            self.database_list.append(dbg)
            tok = tokenLog.getCurrentToken()
            line, column = tok['start']
            dbg.reference = FileRef(self.filename, line, column, self)
            # TODO: Do something with ref
    
    def _parse_globals_statement(self, tokenLog):
        '''
        support the *globals* statement in a template file
        
        This statement was new starting with EPICS base 3.15
        
        example::
        
            global { P=12ida1:,SCANREC=12ida1:scan1 }
        
        '''
        tok = tokenLog.getCurrentToken()
        ref = FileRef(self.filename, tok['start'][0], tok['start'][1], 'global macros')
        # TODO: Do something with ref
        tok = tokenLog.nextActionable()
        if token_key(tok) == 'OP {':
            kv = parse_bracketed_macro_definitions(tokenLog)
            ref = FileRef(self.filename, tok['start'][0], tok['start'][1], kv)
            # TODO: Do something with ref
            self.macros.setMany(kv)
        else:
            msg = '(%s,%d,%d) ' % (self.filename, tok['start'][0], tok['start'][1])
            msg += 'missing "{" in globals statement'
            raise DatabaseTemplateException(msg)
    
    def getPVList(self):
        pv_list = []
        for db in self.database_list:
            pv_list += db.getPVList()
    
    def getPVs(self):
        pv_dict = {}
        for db in self.database_list:
            for k, v in db.getPVs():
                pv_dict[k] = v
        return pv_dict
    
    def get_databases(self):
        return self.database_list


def main():
    testfiles = []
    db = {}
    testfiles.append(os.path.join('.', 'testfiles', 'templates', 'example.template'))
    testfiles.append(os.path.join('.', 'testfiles', 'templates', 'omsMotors'))
    env = dict(TEST="./testfiles")
    for i, tf in enumerate(testfiles):
        try:
            db[tf] = Template(tf, env)
            db[tf].reference = FileRef(__file__, i+1, 0, 'testing')
        except text_file.FileNotFound, _exc:
            print 'file not found: ' + tf
    for k in testfiles:
        if k in db:
            print db[k].source.number_of_lines, k
            for pvname, pv in sorted(db[k].getPVs().items()):
                print '\t%015s : %s' % (pv.RTYP, pvname)
    pass


if __name__ == '__main__':
    main()

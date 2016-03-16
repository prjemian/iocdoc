'''
EPICS template (substitutions) file analysis
'''

import os

import database
import macros
import text_file
from token_support import token_key, TokenLog, getFullWord
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
    
    def __init__(self, filename, **env):
        self.filename = filename
        self.macros = macros.Macros(**env)
        self.database_list = []
        self.reference_list = []

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
        while tok is not None:
            if token_key(tok) == 'NAME file':
                self._parse_file_statement(tokenLog)
            elif token_key(tok) == 'NAME global':
                self._parse_globals_statement(tokenLog)
            tok = tokenLog.nextActionable()
    
    def _note_reference(self, tok, text):
        '''
        make a note of filename, line and column number for something
        '''
        line, column = tok['start']
        self.reference_list.append(FileRef(self.filename, line, column, text))
    
    def _parse_file_statement(self, tokenLog):
        '''
        support the *file* statement in a template file
        
        example::
        
            file "$(SSCAN)/sscanApp/Db/scanParms.db"
        
        '''
        self._note_reference(tokenLog.getCurrentToken(), 'database file')
        
        tok = tokenLog.nextActionable()
        dbFileName = getFullWord(tokenLog).strip('"')
        fname = self.macros.replace(dbFileName)
        self._note_reference(tok, dbFileName + ' -> ' + fname)

        tok = tokenLog.nextActionable()

        # If there is a "pattern" statement, the macro labels are given first, then values in each declaration
        pattern_keys = []
        if token_key(tok) == 'NAME pattern':
            tok = tokenLog.nextActionable()
            while token_key(tok) != 'OP }':
                tok = tokenLog.nextActionable()
                if tok['tokName'] == 'NAME':
                    pattern_keys.append(tok['tokStr'])
            tok = tokenLog.nextActionable()     # skip past the closing }

        
        while token_key(tok) != 'OP }':
            pattern_macros = macros.Macros(**dict(self.macros.getAll()))
            # define the macros for this set
            tok = tokenLog.nextActionable()
            tok_dbLoadRecords = tok
            if len(pattern_keys) > 0:
                # The macro labels were defined in a pattern statement
                for k in pattern_keys:      # TODO: what if #patterns and #values do not match?
                    v = getFullWord(tokenLog).strip('{').strip('}').strip('"')
                    pattern_macros.set(k, v)
                tok = tokenLog.getCurrentToken()
            else:
                # The macro labels are defined with the values
                text = tok['tokLine'].strip().strip('{').strip('}')
                for definition in text.split(','):
                    k, v = [_.strip() for _ in definition.split('=')]
                    v = v.strip(',').strip('"')
                    pattern_macros.set(k, v.strip('"'))
                while token_key(tok) != 'OP }':
                    tok = tokenLog.nextActionable()
                tok = tokenLog.nextActionable()
            
            dbg = database.DbLoadRecords(fname, **dict(pattern_macros.getAll()))
            self.database_list.append(dbg)
            self._note_reference(tok_dbLoadRecords, dbg)
    
    def _parse_globals_statement(self, tokenLog):
        '''
        support the *globals* statement in a template file
        
        This statement was new starting with EPICS base 3.15
        
        example::
        
            global { P=12ida1:,SCANREC=12ida1:scan1 }
        
        '''
        self._note_reference(tokenLog.getCurrentToken(), 'global macros')
        tok = tokenLog.nextActionable()
        if token_key(tok) == 'OP {':
            tok = tokenLog.nextActionable()
            for definition in getFullWord(tokenLog).strip('"').split(','):
                k, v = [_.strip() for _ in definition.split('=')]
                self.macros.set(k, v)
                self._note_reference(tokenLog.getCurrentToken(), k + '=' + v)
        else:
            msg = '(%s,%d,%d) ' % (self.filename, tok['start'][0], tok['start'][1])
            msg += 'missing "{" in globals statement'
            raise DatabaseTemplateException(msg)
    
    def get_pv_list(self):
        # TODO: get the PV list from each database
        pass
    
    def get_databases(self):
        return self.database_list
    
    def get_references(self):
        return self.reference_list


def main():
    testfiles = []
    db = {}
    testfiles.append(os.path.join('.', 'testfiles', 'templates', 'example.template'))
    testfiles.append(os.path.join('.', 'testfiles', 'templates', 'omsMotors'))
    macros = dict(STD="/synApps/std", SSCAN="/synApps/sscan")
    for tf in testfiles:
        try:
            db[tf] = Template(tf, **macros)
        except text_file.FileNotFound, _exc:
            print 'file not found: ' + tf
    for k in testfiles:
        if k in db:
            print db[k].source.number_of_lines, k
            for ref in db[k].get_references():
                print ' '*8, str(ref)


if __name__ == '__main__':
    main()

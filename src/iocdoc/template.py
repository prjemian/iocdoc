'''
EPICS template (substitutions) file analysis
'''

import os

import database
import text_file
from token_support import token_key, TokenLog, getFullWord
from utils import logMessage, FileRef


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
        self.env = dict(env.items())
        self.declarations = []
        self.references = []

        # filename must have all macros expanded
        self.source = text_file.read(filename)
        self.parse()
    
    def parse(self):
        '''
        interpret the template file for database declarations
        
        The Python tokenizer makes simple work of parsing database files.
        The TokenLog class interprets the contents according to a few simple terms
        such as NAME, OP, COMMENT, NEWLINE.
        '''
        self.tokenLog = TokenLog()
        self.tokenLog.processFile(self.filename)
        tok = self.tokenLog.nextActionable()
        while tok is not None:
            if token_key(tok) == 'NAME file':
                self._parse_file_statement()
            elif token_key(tok) == 'NAME global':
                self._parse_globals_statement()
            tok = self.tokenLog.nextActionable()
    
    def _parse_file_statement(self):
        #tok = self.tokenLog.getCurrentToken()
        #print '(%s,%d,%d) %s' % (self.filename, tok['start'][0], tok['start'][1], 'file name' )
        
        tok = self.tokenLog.nextActionable()
        dbFileName = getFullWord(self.tokenLog).strip('"')
        self.references.append(FileRef(self.filename, tok['start'][0], dbFileName))

        tok = self.tokenLog.nextActionable()

        # TODO: expand the macros in the dbFileName using self.env
        macro_keys = []     # TODO: read these from the template
        # If there is a "pattern" statement, the macro labels are given first, then values in each declaration
        # Otherwise, the macro labels are defined with the values
        for _ in []:  # iterate through the patterns for this dbFileName
            macros = dict(**self.env)       # start with the environment variables
            # define the macros for this set
            
            line_number = tok['start'][0]
            dbg = DbLoadRecords(dbFileName, **macros)
            self.declarations.append(dbg)
            self.references.append(FileRef(self.filename, line_number, dbg))
    
    def _parse_globals_statement(self):
        # starting with EPICS base 3.15
        tok = self.tokenLog.getCurrentToken()
        #print '(%s,%d,%d) %s' % (self.filename, tok['start'][0], tok['start'][1], 'global macros' )
        self.references.append(FileRef(self.filename, tok['start'][0], 'global macros'))
        # add macro definitions here to self.env
    
    def substitute_macros(self):
        '''apply macro substitutions'''
        pass
    
    def get_pv_list(self):
        pass


class DbLoadRecords(object):
    '''call for one EPICS database file with a given environment'''
     
    def __init__(self, dbFileName, **env):
        self.dbFileName = dbFileName
        self.env = dict(env.items())
     
    #def parse(self):
    #    '''interpret pattern sets for PV declarations'''
    #    pass
     
    def substitute_macros(self):
        '''apply macro/env substitutions'''
        pass
     
    def get_pv_list(self):
        pass


def main():
    testfiles = []
    db = {}
    testfiles.append(os.path.join('.', 'testfiles', 'templates', 'example.template'))
    testfiles.append(os.path.join('.', 'testfiles', 'templates', 'omsMotors'))
    for tf in testfiles:
        try:
            db[tf] = Template(tf)
        except text_file.FileNotFound, _exc:
            print 'file not found: ' + tf
    for k in testfiles:
        if k in db:
            print db[k].source.number_of_lines, k
            for ref in db[k].references:
                print ' '*8, str(ref)

if __name__ == '__main__':
    main()

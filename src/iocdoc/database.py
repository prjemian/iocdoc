'''
EPICS database file analysis
'''

import os
import macros
import record
import text_file
from token_support import token_key, TokenLog
from utils import logMessage, FileRef


class DatabaseException(Exception): pass


class Database(object):
    '''
    call for one EPICS database file with a given environment
    '''
     
    def __init__(self, dbFileName, **env):
        self.filename = dbFileName
        self.macros = macros.Macros(**env)

        try:
            self.source = text_file.read(self.macros.replace(dbFileName))
            self.parse()
        except Exception, _exc:
            pass
    
    def __str__(self):
        return 'dbLoadRecords ' + self.filename + '  ' + str(self.macros.db)
     
    def parse(self):
        '''interpret records for PV declarations'''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename)
        tok = tokenLog.nextActionable()
        actions = {
                   'NAME record': self._parse_record,
                   'NAME grecord': self._parse_record,
                   'NAME alias': self._parse_alias,
                   }
        while tok is not None:
            tk = token_key(tok)
            if tk in actions:
                actions[tk](tokenLog)
            tok = tokenLog.nextActionable()
    
    def _parse_record(self, tokenLog):
        tok = tokenLog.nextActionable()
        _l = tokenLog.tokens_to_list()
    
    def _parse_alias(self, tokenLog):
        tok = tokenLog.nextActionable()
        _l = tokenLog.tokens_to_list()
        # TODO: finish this
     
    def get_pv_list(self):
        pass


def main():
    db = {}
    testfiles = []
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'pseudoMotor.db'))
    # testfiles.append(os.path.join('.', 'testfiles', 'templates', 'omsMotors'))
    macros = dict(STD="/synApps/std", SSCAN="/synApps/sscan")
    for tf in testfiles:
        try:
            db[tf] = Database(tf, **macros)
        except text_file.FileNotFound, _exc:
            print 'file not found: ' + tf
        print db[tf]


if __name__ == '__main__':
    main()

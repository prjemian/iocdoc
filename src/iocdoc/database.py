'''
EPICS database file analysis
'''

import os
import macros
import record
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions
from utils import logMessage, FileRef


class DatabaseException(Exception): pass


class Database(object):
    '''
    call for one EPICS database file with a given environment
    '''
     
    def __init__(self, dbFileName, env={}):
        self.filename = dbFileName
        self.macros = macros.Macros(env)
        self.reference_list = []
        self.record_list = None
        self.pv_dict = {}

        #  1. read the file for the first time and parsing its content
        #  2. apply supplied macros for each call to the database file

        self.source = text_file.read(self.macros.replace(dbFileName))
        if not hasattr(self.source, 'record_list'):
            self.source.record_list = []
            self.record_list = self.source.record_list
            self.parse()    # step 1: parse the db file for its definitions
        else:
            self.record_list = self.source.record_list

        self.makeProcessVariables()
    
    def __str__(self):
        return 'dbLoadRecords ' + self.filename + '  ' + str(self.macros.getAll())
    
    def _note_reference(self, tok, text):
        '''
        make a note of filename, line and column number for something
        '''
        line, column = tok['start']
        self.reference_list.append(FileRef(self.filename, line, column, text))
     
    def makeProcessVariables(self):
        '''make the EPICS PVs from the record definitions'''
        # build self.pv_dict from self.record_list and self.macros
        if self.record_list is None:
            print self.filename
            print len(self.record_list)
        for rec in self.record_list:
            pv = record.PV(rec, self.macros.getAll())
            self.pv_dict[pv.NAME] = pv
     
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
        rtype, rname = tokenLog.tokens_to_list()
        self._note_reference(tokenLog.getCurrentToken(), '  record: ' + rtype + ' + ' + rname)

        record_object = record.Record(rtype, rname)
        self.record_list.append(record_object)

        tok = tokenLog.nextActionable()
        if token_key(tok) == 'OP {':
            tok = tokenLog.nextActionable()
            # get record's field definitions
            while token_key(tok) != 'OP }':
                if token_key(tok) == 'NAME field':
                    tok = tokenLog.nextActionable()
                    field, value = parse_bracketed_macro_definitions(tokenLog)
                    record_object.addFieldPattern(field, value.strip('"'))
                    tok = tokenLog.previous()   # backup before advancing below
                else:
                    tok = tokenLog.getCurrentToken()
                    msg = '(%s,%d,%d): ' % (self.filename, tok['start'][0], tok['start'][1])
                    msg += ' unexpected content: |%s|' % str(tok['tokStr'])
                    raise RuntimeError(msg)
                tok = tokenLog.nextActionable()
    
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
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'pseudoMotor.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'autoShutter.vdb'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'filterBladeNoSensor.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'filterDrive.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'saveData.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'scan_settings.req'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'scan.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'scanParms.db'))
    macros = dict(TEST="./testfiles", P='prj:', M='m11')
    for tf in testfiles:
        try:
            db[tf] = Database(tf, macros)
        except text_file.FileNotFound, _exc:
            print 'file not found: ' + tf
        print db[tf]


if __name__ == '__main__':
    main()

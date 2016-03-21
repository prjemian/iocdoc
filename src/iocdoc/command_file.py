'''
EPICS IOC command file analysis
'''

import os
import token
import tokenize

import database
import macros
import template
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions
from utils import logMessage, FileRef


'''
TODO: (from topdoc.CmdReader()): refactor this code to:
   - read the file as-is
   - render an analyzed version based on current global tables
   - needs a global cache of .db files
   - needs to know the pwd for each command
   - exception handling
'''


class UnhandledTokenPattern(Exception): pass


class CommandFile(object):
    '''
    analysis of an EPICS IOC command file
    '''


    def __init__(self, parent, filename, env={}, reference=None):
        self.parent = parent
        self.filename = filename
        self.reference = reference

        self.env = dict(env.items())
        self.symbols = {}
        self.commands = []
        self.ref_list = []

        # filename is a relative or absolute path to command file, no macros in the name
        self.source = text_file.read(filename)

        self.parse()
    
    def _make_ref(self, tok, item=None):
        '''make a FileRef() instance for this item'''
        return FileRef(self.filename, tok['start'][0], tok['start'][1], item or self)
    
    def parse(self):
        '''analyze this command file'''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename)
        tok = tokenLog.nextActionable()
        actions = {
                   'NAME cd':               self._parse_changeDirectory,
                   'NAME dbLoadRecords':    self._parse_dbLoadRecords,
                   'NAME dbLoadTemplate':   self._parse_dbLoadTemplate,
                   'NAME epicsEnvSet':      self._parse_epicsEnvSet,
                   'NAME iocshCmd':         self._parse_simpleCommand,
                   'NAME load':             self._parse_simpleCommand,
                   'NAME putenv':           self._parse_putenv,
                   'NAME sysVmeMapShow':    self._parse_simpleCommand,
                   'OP <':                  self._parse_includeCommandFile,
                   }
        while tok is not None:
            tk = token_key(tok)
            if tk in actions:
                ref = self._make_ref(tok, tok['tokStr'])
                self.ref_list.append(ref)
                actions[tk](tokenLog, ref)
            tok = tokenLog.nextActionable()
     
    def report(self):
        '''describe what was discovered'''
        raise NotImplementedError()

    def _parse_changeDirectory(self, tokenLog, ref):
        pass        # TODO: finish this

    def _parse_dbLoadRecords(self, tokenLog, ref):
        pass        # TODO: finish this

    def _parse_dbLoadTemplate(self, tokenLog, ref):
        pass        # TODO: finish this

    def _parse_epicsEnvSet(self, tokenLog, ref):
        pass        # TODO: finish this

    def _parse_includeCommandFile(self, tokenLog, ref):
        pass        # TODO: finish this

    def _parse_putenv(self, tokenLog, ref):
        pass        # TODO: finish this

    def _parse_simpleCommand(self, tokenLog, ref):
        pass        # TODO: finish this


def main():
    cmd = {}
    testfiles = []
    testfiles.append(os.path.join('.', 'testfiles', 'iocBoot', 'ioc495idc', 'st.cmd'))
    for tf in testfiles:
        try:
            cmd[tf] = CommandFile(None, tf)
        except text_file.FileNotFound, _exc:
            print 'file not found: ' + tf
            continue
        except NotImplementedError, _exc:
            print 'Not implemented yet: ' + str(_exc)
            continue
        print cmd[tf]
        for ref in cmd[tf].ref_list:
            print str(ref)


if __name__ == '__main__':
    main()

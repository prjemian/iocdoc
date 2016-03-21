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


    def __init__(self, parent, filename, env={}):
        self.parent = parent
        self.filename = filename
        self.reference = None

        self.env = dict(env.items())
        self.symbols = {}
        self.commands = []
        self.ref_list = []

        # filename is a relative or absolute path to command file, no macros in the name
        self.source = text_file.read(filename)

        self.parse()
    
    def parse(self):
        '''analyze this command file'''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename)
        tok = tokenLog.nextActionable()
        actions = {
                   'NAME putenv XX': self._parse_putenv,
                   }
        while tok is not None:
            tk = token_key(tok)
            if tok['tokName'] in ('NAME',):
                ref = FileRef(self.filename, tok['start'][0], tok['start'][1], tok['tokStr'])
                self.ref_list.append(ref)
            if tk in actions:
                actions[tk](tokenLog)
            tok = tokenLog.nextActionable()
     
    def report(self):
        '''describe what was discovered'''
        raise NotImplementedError()

    def _parse_putenv(self, tokenLog):
        raise NotImplementedError


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

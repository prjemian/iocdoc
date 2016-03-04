'''
EPICS IOC command file analysis
'''

import os
import token
import tokenize


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


    def __init__(self, parent, fobject, env={}):
        self.parent = parent
        self.fobject = fobject

        self.env = dict(env.items())
        self.symbols = {}
        self.commands = []
    
    def expand_macros(self):
        '''expand all known macros'''
        raise NotImplementedError()
    
    def parse(self):
        '''analyze this command file'''
        raise NotImplementedError()
     
    def report(self):
        '''describe what was discovered'''
        raise NotImplementedError()

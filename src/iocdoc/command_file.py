'''
EPICS IOC command file analysis
'''

import os
import token
import tokenize
import file_support


'''
TODO: (from topdoc.CmdReader()): refactor this code to:
   - read the file as-is
   - render an analyzed version based on current global tables
   - needs a global cache of .db files
   - needs to know the pwd for each command
   - exception handling
'''


class UnhandledTokenPattern(Exception): pass


class CommandFile(file_support.TextFile):
    '''
    analysis of an EPICS IOC command file
    '''


    def __init__(self, parent, filename, macros={}):
        super(CommandFile, self).__init__(parent, filename)

        self.env = {}
        self.symbols = {}
        self.commands = []

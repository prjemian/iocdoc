'''
Any text file related to an EPICS IOC
'''

import os


class TextFile(object):
    '''
    Any text file related to an EPICS IOC
    '''

    def __init__(self, parent, filename, file_cache, macros={}):
        if not os.path.exists(filename):
            raise IOError('file does not exist: ' + filename)
        self.parent = parent
        self.filename = filename
        self.absolute_filename = os.path.abspath(filename)
        self.absolute_directory = os.path.dirname(self.absolute_filename)
        self.cwd = os.getcwd()
        self.file_cache = file_cache
        
        if filename in file_cache:
            self.text = file_cache[filename]
        else:
            self.text = open(filename, 'r').read()
            file_cache[filename] = self.text

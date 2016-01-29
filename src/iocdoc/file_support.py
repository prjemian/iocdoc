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
        
        if filename in file_cache:
            self.file_text = file_cache[filename]
        else:
            self.file_text = open(filename, 'r').read()
            file_cache[filename] = self.file_text

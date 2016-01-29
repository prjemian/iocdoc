'''
Any text file related to an EPICS IOC
'''

import os


# TODO: manage a cache of all known text files
# TODO: return object from cache otherwise create


class TextFile(object):
    '''
    Any text file related to an EPICS IOC
    '''

    def __init__(self, parent, filename, macros={}):
        if not os.path.exists(filename):
            raise IOError('IOC command file does not exist: ' + filename)
        self.parent = parent
        self.filename = filename
        self.absolute_filename = os.path.abspath(filename)
        self.absolute_directory = os.path.dirname(self.absolute_filename)
        self.cwd = os.getcwd()

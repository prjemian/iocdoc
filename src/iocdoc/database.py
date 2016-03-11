'''
EPICS database file analysis
'''

import os
import text_file


class Database(object):
    '''
    EPICS template (substitutions) file
    
    Template files contain one or more pattern sets, 
    each containing one or more EPICS PV declarations.
    It is implied that each PV declaration is a call to 
    ``dbLoadRecords`` where the database is specified 
    in the pattern set header.
    '''
    
    def __init__(self, filename, **env):
        self.filename = filename
        self.env = dict(env.items())

        # TODO: ?wait for this step?  filename might need macro expansion
        #self.source = text_file.read(filename)
        #self.parse()
    
    def parse(self):
        '''interpret the source for pattern sets'''
        pass
    
    def substitute_macros(self):
        '''apply macro substitutions'''
        pass
    
    def get_pv_list(self):
        pass

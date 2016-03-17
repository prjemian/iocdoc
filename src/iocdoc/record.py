'''
EPICS record
'''

import os
import macros


class RecordException(Exception): pass


class Record(object):
    '''single instance of an EPICS record definition'''
     
    def __init__(self, rtyp, **env):
        self.RTYP = rtyp
        self.macros = macros.Macros(**env)
    
    def __str__(self):
        return 'record ' + self.RTYP + '  ' + str(self.macros.db)

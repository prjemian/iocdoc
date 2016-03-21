'''
EPICS record
'''

import os
import macros


class RecordException(Exception): pass


class Record(object):
    '''definition of an EPICS record'''
     
    def __init__(self, parent, rtype, rname, env={}):
        self.parent = parent
        self.RTYP = rtype
        self.rname = rname
        self.macros = macros.Macros(env)
        self.fields = dict(RTYP=rtype, NAME=rname)
        self.reference = None       # TODO: Make the definition and usage of this term clearer
    
    def __str__(self):
        return 'record ' + self.RTYP + '  ' + self.rname
    
    def addFieldPattern(self, field, value):
        self.fields[field] = value


class PV(object):
    '''single instance of an EPICS record'''
    
    # TODO: make ability to identify source file, line & column numbers for each PV instance
    # includes .db file, template file / command file
     
    def __init__(self, record_object, env={}):
        self.record = record_object
        self.macros = macros.Macros(env)
        self.RTYP = record_object.RTYP
        self.fields = {k: self.macros.replace(v) for k, v in self.record.fields.items()}
        self.NAME = self.fields['NAME']
        self.reference = record_object.reference       # TODO: Make the definition and usage of this term clearer
    
    def __str__(self):
        return 'record ' + self.RTYP + '  ' + str(self.macros.getAll())
    
    def getField(self, field):
        return self.fields[field]
    
    def getFields(self):
        return self.fields.items()
    
    def getFieldList(self):
        return self.fields.keys()

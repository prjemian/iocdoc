'''
EPICS record
'''

import os
import macros


class RecordException(Exception): pass


class Record(object):
    '''definition of an EPICS record, macros are not expanded'''
     
    def __init__(self, parent, rtype, rname, env={}, reference=None):
        self.parent = parent
        self.RTYP = rtype
        self.rname = rname
        self.macros = macros.Macros(env)
        self.fields = dict(RTYP=rtype, NAME=rname)
        self.reference = reference
        self.alias_dict = {}        # TODO: handle this
        self.info_dict = {}         # TODO: handle this
    
    def __str__(self):
        return 'record ' + self.RTYP + '  ' + self.rname
    
    def addFieldPattern(self, field, value):
        self.fields[field] = value


class PV(object):
    '''single instance of an EPICS record, will expand all macros as provided'''
     
    def __init__(self, record_object, env={}, reference=None):
        self.record = record_object
        self.RTYP = record_object.RTYP
        self.macros = macros.Macros(env)
        self.reference = reference

        self.fields = {k: self.macros.replace(v) for k, v in self.record.fields.items()}
        
        self.NAME = self.fields['NAME']
    
    def __str__(self):
        return 'record ' + self.RTYP + '  ' + str(self.macros.getAll())
    
    def getField(self, field):
        return self.fields[field]
    
    def getFields(self):
        return self.fields.items()
    
    def getFieldList(self):
        return self.fields.keys()

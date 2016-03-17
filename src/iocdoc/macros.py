'''
support for macro substitutions
'''

import re

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# regular expression catalog

# a-z A-Z 0-9 _ -- : . [ ] < > ;
EPICS_UNQUOTED_STRING_RE = r'[\d\w_:;.<>\-\[\],]+'
EPICS_MACRO_SPECIFICATION_P_RE = "\$\("+EPICS_UNQUOTED_STRING_RE+"\)"       # _P_: parentheses
EPICS_MACRO_SPECIFICATION_B_RE = "\$\{"+EPICS_UNQUOTED_STRING_RE+"\}"       # _B_: braces
# EPICS_MACRO_DEFAULT_RE cannot find $(P=$(S)), that's OK.
# If the inner $(S) was expanded, it would be found then, else macro expansion fails anyway
EPICS_MACRO_DEFAULT_RE = EPICS_UNQUOTED_STRING_RE+'='+EPICS_UNQUOTED_STRING_RE
EPICS_MACRO_SPECIFICATION_PD_RE = "\$\("+EPICS_MACRO_DEFAULT_RE+"\)"
EPICS_MACRO_SPECIFICATION_BD_RE = "\$\{"+EPICS_MACRO_DEFAULT_RE+"\}"

EPICS_UNQUOTED_STRING_PATTERN = re.compile(EPICS_UNQUOTED_STRING_RE, 0)
EPICS_MACRO_SPECIFICATION_P_PATTERN = re.compile(EPICS_MACRO_SPECIFICATION_P_RE, 0)
EPICS_MACRO_SPECIFICATION_B_PATTERN = re.compile(EPICS_MACRO_SPECIFICATION_B_RE, 0)
EPICS_MACRO_DEFAULT_PATTERN = re.compile(EPICS_MACRO_DEFAULT_RE, 0)
EPICS_MACRO_SPECIFICATION_PD_PATTERN = re.compile(EPICS_MACRO_SPECIFICATION_PD_RE, 0)
EPICS_MACRO_SPECIFICATION_BD_PATTERN = re.compile(EPICS_MACRO_SPECIFICATION_BD_RE, 0)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Macros(object):
    '''manage a set of macros (keys, substitutions)'''
     
    def __init__(self, env):
        self.db = {}
        self.setMany(env)
    
    def exists(self, key):
        '''is there such a *key*?'''
        return key in self.db
    
    def get(self, key, missing=None):
        '''find the *key* macro, if not found, return *missing*'''
        return self.db.get(key, missing)
    
    def set(self, key, value):
        '''define the *key* macro'''
        self.db[key] = value
    
    def setMany(self, env):
        '''define several macros'''
        self.db = dict(self.db.items() + env.items())
    
    def keys(self):
        '''get the list of macros'''
        return self.db.keys()
    
    def getAll(self):
        '''return the full database'''
        return self.db
    
    def replace(self, text):
        '''Replace macro parameters in source string'''
        return _replace_(text, self.db)


def _replace_(source, macros):
    '''
    Replace macro parameters in source string.
    Search through the list of macros since there 
    may not be enough macros defined for all the 
    substitution patterns given.

    :param source: string with possible macro replacements
    :param macros: dictionary of macro substitutions
    :return: string with substitutions applied
    :raise Exception: incorrect number of regular expression matches found
    '''
    last = ''
    while last != source:     # repeat to expand nested macros
        last = source
        # substitute the simple macro replacements
        for subst_marker in identifyEpicsMacros(source):
            parts = re.findall(EPICS_UNQUOTED_STRING_PATTERN, subst_marker, 0)
            if len(parts) == 1 and parts[0].find(','):
                parts = parts[0].split(',')
            if len(parts) == 1:
                # substitute the simple macros
                if parts[0] in macros:
                    replacement_text = macros[parts[0]]
                    source = source.replace(subst_marker, replacement_text)
            elif len(parts) == 2:
                # substitute the macros with default expressions
                macro_variable, default_substitution = parts
                if macro_variable in macros:
                    replacement_text = macros[macro_variable]
                else:
                    replacement_text = default_substitution
                source = source.replace(subst_marker, replacement_text)
            else:
                # add more diagnostics if this happens
                raise Exception, "should only match 1 or 2 parts here"
    return source


def identifyEpicsMacros(source):
    '''
    Identify any EPICS macro substitutions in the source string.
    Multiple entries of the same substitution (redundancies)
    are ignored.  Does not include nested macros such as:
    
    ::

        $(P=$(S))${S_$(P)}
        $(PJ=$(P))${S_$(P)}

    For these, only the innermost are returned:
    
    ::

        ['$(S)', '$(P)']
        ['$(P)']

    :note: This routine will also properly identify  command shell macro substitutions.

    :param source: string with possible (EPICS) macro substitution expressions
    :return: list of macro substitutions found
    '''
    parts = []
    for patt in (EPICS_MACRO_SPECIFICATION_P_PATTERN, 
                 EPICS_MACRO_SPECIFICATION_B_PATTERN):
        for subst_marker in re.findall(patt, source, 0):
            if subst_marker not in parts:
                parts.append( subst_marker )
    for patt in (EPICS_MACRO_SPECIFICATION_PD_PATTERN, 
                 EPICS_MACRO_SPECIFICATION_BD_PATTERN):
        for subst_marker in re.findall(patt, source, 0):
            parts.append( subst_marker )
    return parts

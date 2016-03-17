'''
EPICS database file analysis
'''

import os
import macros
import record
import text_file


class DatabaseException(Exception): pass


class DbLoadRecords(object):
    '''call for one EPICS database file with a given environment'''
     
    def __init__(self, dbFileName, **env):
        self.dbFileName = dbFileName
        self.macros = macros.Macros(**env)
    
    def __str__(self):
        return 'dbLoadRecords ' + self.dbFileName + '  ' + str(self.macros.db)
     
    #def parse(self):
    #    '''interpret pattern sets for PV declarations'''
    #    pass
     
    def get_pv_list(self):
        pass


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
    
    def get_pv_list(self):
        pass


def main():
    testfiles = []
    # testfiles.append(os.path.join('.', 'testfiles', 'templates', 'example.template'))
    # testfiles.append(os.path.join('.', 'testfiles', 'templates', 'omsMotors'))
    # macros = dict(STD="/synApps/std", SSCAN="/synApps/sscan")


if __name__ == '__main__':
    main()

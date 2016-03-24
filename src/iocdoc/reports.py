
'''
generate the standard reports for *iocdoc*
'''

import datetime
import os
import pyRestTable
import text_file


class writeReports(object):
    
    def __init__(self, obj, ioc_name='IOC'):
        self.st_cmd_object = obj
        self.ioc_name = ioc_name
        self.writeReports()

    def writeReports(self):
        '''report what was learned from the command file'''
        obj = self.st_cmd_object
        ioc_name = self.ioc_name
        files = []
        files.append(self.writeFile('command_sequence.rst',  ioc_name+': IOC Command sequence',              reportCommandSequence(obj.commands)))
        files.append(self.writeFile('rtyp.rst',              ioc_name+': EPICS Records types used',          reportRTYP(obj.pv_dict)))
        files.append(self.writeFile('command_list.rst',      ioc_name+': EPICS IOC shell commands used',     reportCommandCount(obj.commands)))
        files.append(self.writeFile('motor_types.rst',       ioc_name+': EPICS Motor types used',            reportMotorCount(obj.pv_dict)))
        files.append(self.writeFile('pvs.rst',               ioc_name+': Process Variables',                 reportPVs(obj.pv_dict)))
        files.append(self.writeFile('macros.rst',            ioc_name+': Macros',                            reportSymbols(obj.env.db)))
        files.append(self.writeFile('symbols.rst',           ioc_name+': Symbols',                           reportSymbols(obj.symbols.db)))
        files.append(self.writeFile('databases.rst',         ioc_name+': EPICS Databases',                   reportDatabases(obj.database_list)))
        files.append(self.writeFile('templates.rst',         ioc_name+': EPICS Templates/Substitutions',     reportDatabases(obj.template_list)))
        files.append(self.writeFile('text_files.rst',        ioc_name+': text file cache',                   reportTextFiles()))
    
        # write the index.rst that coordinates all this
        indent = ' '*3
        title = 'IOC: ' + ioc_name
        text = ':st.cmd file: ' + str(obj.filename)
        text += '\n'
        text += ':absolute path: ' + str(obj.filename_absolute)
        text += '\n'*2
        text += 'Contents:\n\n'
        text += '.. toctree::\n'
        text += indent + ':maxdepth: 1\n'
        text += indent + ':glob:\n'
        text += '\n'
        for f in sorted(files):
            nm = os.path.splitext(f)[0]
            text += indent + nm + '\n'
        self.writeFile('index.rst', title, text)
    
        # TODO: write a conf.py file

    def writeFile(self, fname, title, text):
        f =  open(fname, 'w')
        f.write('.. file - ' + fname)
        f.write('\n'*2)
        f.write('.. index:: ' + self.ioc_name + ', ' + os.path.splitext(fname)[0])
        f.write('\n'*2)
        f.write('.. _IOC_' + self.ioc_name + '_' + os.path.splitext(fname)[0])
        f.write('\n'*2)
        f.write(mk_title(title, '='))
        f.write('\n')
        f.write(text)
        f.write('\n')
        f.write('\n' + '-'*10 + '\n'*2)
        f.write('written: ' + str(datetime.datetime.now()))
        f.write('\n')
        f.close()
        return fname


def reportCmdFile(obj, ioc_name='Command File'):
    '''report what was learned from the command file'''
    print mk_title('IOC: ' + ioc_name, '=')
    print 'initial startup command script file: ', obj
    print 'absolute path: ', obj.filename_absolute
    
    print '\n'
    print mk_title('Table: IOC Command sequence')
    print reportCommandSequence(obj.commands)
    
    print '\n'
    print mk_title('Table: EPICS Records types used')
    print reportRTYP(obj.pv_dict)
    
    print '\n'
    print mk_title('Table: EPICS IOC shell commands used')
    print reportCommandCount(obj.commands)
    
    print '\n'
    print mk_title('Table: EPICS Motor types used')
    print reportMotorCount(obj.pv_dict)
    
    # print '\n'
    # print mk_title('Table: Process Variables')
    # print reportPVs(obj.pv_dict)
            
    print '\n'
    print mk_title('Table: MACROS')
    # switch reportSymbols() once macros get an object reference
    # old: reportMacros()
    print reportSymbols(obj.env.db)
    
    print '\n'
    print mk_title('Table: SYMBOLS')
    print reportSymbols(obj.symbols.db)
    
    print '\n'
    print mk_title('Table: EPICS Databases')
    print 'printed in the order they were called'
    # TODO: obj.database_list is not *ALL* the databases
    print reportDatabases(obj.database_list)
    
    print '\n'
    print mk_title('Table: EPICS Templates/Substitutions')
    print 'printed in the order they were called'
    # TODO: obj.database_list is not *ALL* the databases
    print reportDatabases(obj.template_list)
    
    print '\n'
    print mk_title('Table: text file cache')
    print reportTextFiles()


def mk_title(text='title', symbol='-'):
    return '\n'.join( [text, symbol*len(text), ''] )


def _makeCountTable(xref, label='subject'):
    '''show the xref table in a dict'''
    tbl = pyRestTable.Table()
    tbl.labels = ['#', label, 'count']
    count = 0
    i = 0
    for k, v in sorted(xref.items()):
        i += 1
        tbl.rows.append([i, k, v])
        count += v
    tbl.rows.append(['--', 'TOTAL', count])
    return tbl.reST()


def reportCommandCount(cmd_list):
    '''how many of each command?'''
    xref = {}
    for cmd in cmd_list:
        if cmd.command not in xref:
            xref[cmd.command] = 0
        xref[cmd.command] += 1
    return _makeCountTable(xref, label='command')


def reportCommandSequence(cmd_list):
    '''show the order of the commands'''
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'command', 'arguments']
    for i, command in enumerate(cmd_list):
        tbl.rows.append([i+1, command.reference, command.command, command.args])
    return tbl.reST()


def reportDatabases(db_list):
    '''show the databases that were used'''
    if len(db_list) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'database file']
    for i, db in enumerate(db_list):
        # TODO: distinguish between environment macros and new macros for this instance
        # TODO: also document each record's definition: db.record_list
        tbl.rows.append([i+1, db.reference, db.filename])
    return tbl.reST()


def reportMacros(macro_dict):
    '''Show the macros in a table'''
    if len(macro_dict) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['#', 'name', 'definition']
    i = 0
    for k, v in sorted(macro_dict.items()):
        i += 1
        tbl.rows.append([i, k, v])
    return tbl.reST()


def reportMotorCount(pv_dict):
    '''how many of each type of motor?'''
    xref = {}
    for k, pv in pv_dict.items():
        if pv.RTYP == 'motor' and k == pv.NAME:
            dtype = pv.getField('DTYP', 'undefined')
            if dtype == 'asynMotor':
                dtype += ' ' + pv.getField('OUT', '')
            if dtype not in xref:
                xref[dtype] = 0
            xref[dtype] += 1
    if len(xref) == 0:
        return 'no motors'
    return _makeCountTable(xref, label='motor type')


def reportPVs(pv_dict):
    '''List the defined process variables'''
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'record type', 'PV name']
    i = 0
    for _k, pv in sorted(pv_dict.items()):
        i += 1
        tbl.rows.append([i, pv.reference, pv.RTYP, pv.NAME])
    return tbl.reST()


def reportRTYP(pv_dict):
    '''how many of each record type?'''
    xref = {}
    for k, pv in pv_dict.items():
        if k != pv.NAME:
            rtype = 'alias'
        else:
            rtype = pv.RTYP
        if rtype not in xref:
            xref[rtype] = 0
        xref[rtype] += 1
    return _makeCountTable(xref, label='RTYP')


def reportSymbols(macro_dict):
    '''Show the symbols in a table'''
    if len(macro_dict) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'name', 'value']
    i = 0
    for _k, v in sorted(macro_dict.items()):
        i += 1
        tbl.rows.append([i, v.reference, v.key, v.value])
    return tbl.reST()


def reportTextFiles():
    '''show the text files that were read'''
    # sort by short file name (no path)
    xref = {}
    for k, v in text_file.items():
        f = os.path.split(k)[-1]
        if f not in xref:
            xref[f] = []
        xref[f].append(v)

    tbl = pyRestTable.Table()
    tbl.labels = ['#', 'file_name', 'path']
    i = 0
    for k in sorted(xref.keys()):
        for v in sorted(xref[k]):
            i += 1
            tbl.rows.append([i, k, v.absolute_filename])
    return tbl.reST()

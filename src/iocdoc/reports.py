
'''
generate the standard reports for *iocdoc*
'''

import os
import pyRestTable
import text_file
import utils


def pre(text):
    val = text.strip()
    if len(val) == 0:
        val = ' '
    return '``' + val + '``'


class writeReports(object):
    
    def __init__(self, obj, ioc_name='IOC', report_file_cache=True):
        self.st_cmd_object = obj
        self.ioc_name = ioc_name
        self.report_file_cache = report_file_cache
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
        if self.report_file_cache:
            files.append(self.writeFile('text_files.rst',    ioc_name+': text file cache',                   reportTextFiles()))

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
        topic = os.path.splitext(fname)[0]
        f.write('.. file - ' + fname)
        f.write('\n'*2)
        f.write('.. index:: ' + self.ioc_name + ', ' + topic)
        f.write('\n'*2)
        f.write('.. _IOC.' + self.ioc_name + '_' + topic + ':')
        f.write('\n'*2)
        f.write(mk_title(title, '='))
        f.write('\n')
        f.write(text)
        f.write('\n')
        f.write('\n' + '-'*10 + '\n'*2)
        f.write('written: ' + utils.datenow())
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


# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - 

# TODO: document records with stream support
# list of protocol files and database files from which they were called
# table of INP and OUT fields
# ...
'''
2 (DCMotorServer.db,20,9) DTYP  stream                              
3 (DCMotorServer.db,21,9) INP   @DCMotorServer.proto version $(PORT)

2 (DCMotorServer.db,27,9) DTYP  stream                            
3 (DCMotorServer.db,28,9) OUT   @DCMotorServer.proto debug $(PORT)
'''

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
    tbl.labels = ['#', '(file_name,line,column)', 'command and arguments']
    for i, command in enumerate(cmd_list):
        val = pre(command.command + ' ' + command.args)
        tbl.rows.append([i+1, command.reference, val])
    return tbl.reST()


def reportDatabases(db_list):
    '''show the databases that were used'''
    if len(db_list) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'database file']
    for i, db in enumerate(db_list):
        # TODO: distinguish between environment macros and new macros for this instance
        tbl.rows.append([i+1, db.reference, pre(db.filename)])
    text = tbl.reST()
    
    # avoid repeating
    xref = {db.filename: db for db in db_list}
    
    for dbName in sorted(xref.keys()):
        db = xref[dbName]
        if not hasattr(db, 'record_list'):
            continue    # Templates also use this report
        text += '\n'*2
        text += mk_title('Database Records: ' + db.filename, '*')
        text += '\n'
        if len(db.record_list) == 0:
            text += 'no records\n'
            continue
        i = 0
        tbl = pyRestTable.Table()
        tbl.labels = ['#', '(file_name,line,column)', 'RTYP', 'NAME']
        for record in db.record_list:
            i += 1
            tbl.rows.append([i, record.reference, record.RTYP, pre(record.rname) ])
        text += tbl.reST()

        # document each record's fields
        for record in db.record_list:
            text += '\n'
            text += mk_title('Record Fields: ' + record.RTYP + ': ' + record.rname, '+')
            text += '\n'
            if len(record.fields) < 3:
                text += 'no fields\n'
                continue
            tbl = pyRestTable.Table()
            tbl.labels = ['#', '(file_name,line,column)', 'field', 'value']
            i = 0
            for k, v in sorted(record.fields.items()):
                if k in ('NAME', 'RTYP'):
                    continue
                i += 1
                tbl.rows.append([i, v.reference, k, pre(v.value)])
            text += tbl.reST()
    return text


def reportMacros(macro_dict):
    '''Show the macros in a table'''
    if len(macro_dict) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['#', 'name', 'definition']
    i = 0
    for k, v in sorted(macro_dict.items()):
        i += 1
        tbl.rows.append([i, k, pre(v)])
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
        tbl.rows.append([i, pv.reference, pv.RTYP, pre(pv.NAME)])
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
        tbl.rows.append([i, v.reference, v.key, pre(v.value)])
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
    tbl.labels = ['#', 'uses', 'file_name', 'path']
    i = 0
    for k in sorted(xref.keys()):
        for v in sorted(xref[k]):
            i += 1
            tbl.rows.append([i, v.count_requests, k, v.absolute_filename])
    return tbl.reST()

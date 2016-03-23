
import pyRestTable
import text_file


def reportCmdFile(obj, ioc_name='Command File'):
    print title('IOC: ' + ioc_name, '=')
    print 'initial startup command script file: ', obj
    print 'absolute path: ', obj.filename_absolute
    
    # how many of each record type?
    print '\n'
    print title('Table: IOC Command sequence')
    print reportCommandSequence(obj.commands)
    
    # how many of each record type?
    print '\n'
    print title('Table: EPICS Records types used')
    print reportRTYP(obj.pv_dict)
    
    # how many of each record type?
    print '\n'
    print title('Table: EPICS IOC shell commands used')
    print reportCommandCount(obj.commands)
    
    # What kinds of motor were used?
    print '\n'
    print title('Table: EPICS Motor types used')
    print reportMotorCount(obj.pv_dict)
            
    # What is in the MACROS dictionary?
    print '\n'
    print title('Table: MACROS')
    print reportMacros(obj.env.getAll())
    
    # What is in the MACROS dictionary?
    print '\n'
    print title('Table: SYMBOLS')
    print reportSymbols(obj.symbols.getAll())
    
    # What EPICS Databases were used?
    print '\n'
    print title('Table: EPICS Databases')
    # TODO: obj.database_list is not *ALL* the databases
    print reportDatabases(obj.database_list)
    
    # What text files were used?
    print '\n'
    print title('Table: text file cache')
    print reportTextFiles()


def title(text='title', symbol='-'):
    return '\n'.join( [text, symbol*len(text), ''] )


def _makeCountTable(xref, label='subject'):
    '''show the xref table in a dict'''
    tbl = pyRestTable.Table()
    tbl.labels = [label, 'count']
    count = 0
    for k, v in sorted(xref.items()):
        tbl.rows.append([k, v])
        count += v
    tbl.rows.append(['TOTAL', count])
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
    '''show the order op the commands'''
    tbl = pyRestTable.Table()
    tbl.labels = ['(file_name,line,column)', 'command', 'arguments']
    for command in cmd_list:
        tbl.rows.append([command.reference, command.command, command.args])
    return tbl.reST()


def reportDatabases(db_list):
    '''show the databases that were used'''
    if len(db_list) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['(file_name,line,column)', 'database file']
    for db in db_list:
        # TODO: distinguish between environment macros and new macros for this instance
        tbl.rows.append([db.reference, db.filename])
    return tbl.reST()


def reportMacros(macro_dict):
    '''Show the macros in a table'''
    if len(macro_dict) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['name', 'definition']
    for k, v in sorted(macro_dict.items()):
        tbl.rows.append([k, v])
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
    tbl.labels = ['(file_name,line,column)', 'name', 'value']
    for _k, v in sorted(macro_dict.items()):
        tbl.rows.append([v.reference, v.symbol, v.value])
    return tbl.reST()


def reportTextFiles():
    '''show the text files that were read'''
    tbl = pyRestTable.Table()
    tbl.labels = ['file_name', 'path']
    for _k, v in sorted(text_file.items()):
        tbl.rows.append([v.filename, v.absolute_filename])
    return tbl.reST()

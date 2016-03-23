'''
EPICS IOC command file analysis
'''

import os
import pyRestTable
import token
import tokenize
import traceback


import database
import macros
import template
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions, reconstruct_line
from utils import logMessage, FileRef, strip_quotes, strip_parentheses


'''
TODO: (from topdoc.CmdReader()): refactor this code to:
   - read the file as-is
   - render an analyzed version based on current global tables
   - needs a global cache of .db files
   - needs to know the pwd for each command
   - exception handling
'''


class UnhandledTokenPattern(Exception): pass


class Command(object):
    '''
    one command in an EPICS IOC command file
    '''

    def __init__(self, parent, command, path, args, env={}, reference=None):
        self.parent = parent
        self.command = command
        self.path = path
        self.args = args
        self.env = macros.Macros(env)
        self.reference = reference
    
    def __str__(self):
        return self.command + ' ' + str(self.args) + ' ' + str(self.env)


class Symbol(object):
    '''
    one symbol in an EPICS IOC command file
    '''

    def __init__(self, parent, sym, value, reference=None):
        self.parent = parent
        self.symbol = sym
        self.value = value
        self.reference = reference
    
    def __str__(self):
        return self.symbol + ' = ' + str(self.value)


class CommandFile(object):
    '''
    analysis of an EPICS IOC command file
    '''

    def __init__(self, parent, filename, env={}, reference=None):
        self.parent = parent
        self.filename = filename
        self.reference = reference
        self.pwd = os.getcwd()      # TODO: needs some attention here

        self.env = macros.Macros(env)
        self.symbols = macros.Macros({})
        self.database_list = []
        self.commands = []
        self.template_list = []
        self.includedCommandFile_list = []
        self.pv_dict = {}

        # filename is a relative or absolute path to command file, no macros in the name
        self.filename_absolute = os.path.abspath(filename)
        self.dirname_absolute = os.path.dirname(self.filename_absolute)
        #self.filename_expanded = self.env.replace(filename)
        self.source = text_file.read(filename)

        self.knownHandlers = {
            '<': self.kh_loadCommandFile,
            'cd': self.kh_cd,
            # 'dbLoadDatabase': self.kh_dbLoadDatabase,
            'dbLoadRecords': self.kh_dbLoadRecords,
            'dbLoadTemplate': self.kh_dbLoadTemplate,
            'epicsEnvSet': self.kh_epicsEnvSet,
            'putenv': self.kh_putenv,
            # 'seq': self.kh_seq,
            'strcpy': self.kh_strcpy,
            # 'nfsMount': self.kh_nfsMount,
            # 'nfs2Mount': self.kh_nfsMount,
            #------ overrides -----------
            'dbLoadDatabase': self.kh_shell_command,
            'seq': self.kh_shell_command,
            'nfsMount': self.kh_shell_command,
            'nfs2Mount': self.kh_shell_command,
        }
        self.parse()
    
    def __str__(self):
        return str(self.reference) + ' ' + self.filename
    
    def _make_ref(self, tok, item=None):
        '''make a FileRef() instance for this item'''
        return FileRef(self.filename, tok['start'][0], tok['start'][1], item or self)
    
    def parse(self):
        '''analyze this command file'''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename)
        lines = tokenLog.lineAnalysis()
        del lines['numbers']
        for _lineNumber, line in sorted(lines.items()):
            isNamePattern = line['pattern'].startswith( 'NAME' )
            tk = token_key(line['tokens'][0])
            if isNamePattern or tk == 'OP <':
                arg0 = line['tokens'][0]['tokStr']
                ref = self._make_ref(line['tokens'][0], arg0)
                if line['tokens'][1]['tokStr'] == '=':
                    # this is a symbol assignment
                    handler = self.kh_symbol
                    handler(arg0, line['tokens'], ref)
                elif arg0 in self.knownHandlers:
                    # command arg0 has a known handler, call it
                    handler = self.knownHandlers[arg0]
                    handler(arg0, line['tokens'], ref)
                else:
                    self.kh_shell_command(arg0, line['tokens'], ref)
     
    def report(self):
        '''describe what was discovered'''
        raise NotImplementedError()

    def kh_cd(self, arg0, tokens, ref):
        path = reconstruct_line(tokens).strip()
        if self.symbols.exists(path):       # symbol substitution
            path = self.symbols.get(path).value
        path = self.env.replace(path)       # macro substitution
        path = strip_quotes(path)           # strip double-quotes
        if len(path) > 0 and os.path.exists(path):
            os.chdir(path)
            self.kh_shell_command(arg0, tokens, ref)

    def kh_dbLoadRecords(self, arg0, tokens, ref):
        local_macros = macros.Macros(self.env.getAll())
        tokenLog = TokenLog()
        tokenLog.tokenList = tokens
        tokenLog.token_pointer = 1
        parts = parse_bracketed_macro_definitions(tokenLog)
        count = len(parts)
        if count == 0 or count > 3:
            msg = str(ref) + reconstruct_line(tokens).strip()
            raise UnhandledTokenPattern, msg
        if count > 0:
            dbFileName = strip_quotes(parts[0])
        if count > 1:
            for definition in strip_quotes(parts[1]).split(','):
                k, v = definition.split('=')
                local_macros.set(k, v)
        if count == 3:
            path = parts[2]
            msg = str(ref) + reconstruct_line(tokens).strip()
            # TODO: how to handle this?
            raise UnhandledTokenPattern, msg
        try:
            obj = database.Database(self, dbFileName, local_macros.getAll(), ref)
            self.database_list.append(obj)
            self.kh_shell_command(arg0, tokens, ref)
        except text_file.FileNotFound, _exc:
            # TODO: what to do at this point?  Need report and continue mechanism
            traceback.print_exc()
            return
        for k, v in obj.getPVs():
            self.pv_dict[k] = v

    def kh_dbLoadTemplate(self, arg0, tokens, ref):
        local_macros = macros.Macros(self.env.getAll())
        tfile = strip_quotes(strip_parentheses(reconstruct_line(tokens).strip()))
        obj = template.Template(tfile, local_macros.getAll(), ref)
        self.template_list.append(obj)
        # TODO: anything else to be done?
        self.kh_shell_command(arg0, tokens, ref)
        for k, v in obj.getPVs():
            self.pv_dict[k] = v

    def kh_epicsEnvSet(self, arg0, tokens, ref):
        '''symbol assignment'''
        text = strip_parentheses(reconstruct_line(tokens).strip())
        parts = text.split(',')
        if len(parts) == 1:
            parts = text.split(' ')
        else:
            pass
        var, value = parts
        self.env.set(strip_quotes( var ), strip_quotes( value ))
        self.kh_shell_command('(env)', tokens, ref)

    def kh_loadCommandFile(self, arg0, tokens, ref):
        fname = strip_parentheses(reconstruct_line(tokens).strip())
        # fname is given relative to current working directory
        fname_expanded = self.env.replace(fname)
        obj = CommandFile(self, fname_expanded, self.env.getAll(), ref)
        self.includedCommandFile_list.append(obj)
        self.kh_shell_command('<', tokens, ref)

        self.commands += obj.commands
        self.symbols.setMany(obj.symbols.getAll())
        self.env.setMany(obj.env.getAll())
        for k, v in obj.pv_dict.items():
            self.pv_dict[k] = v

    def kh_putenv(self, arg0, tokens, ref):
        '''
        process an instance of putenv

        :param tokens: token list
        :param ref: instance of :class:`iocdoc.utils.FileRef`
        :raise UnhandledTokenPattern: unhandled token pattern
        '''
        argument_list = []
        for tkn in tokens[1:]:
            if tkn['tokName'] == 'STRING':
                argument_list.append( tkn['tokStr'] )

        if len(argument_list) == 1:
            var, arg = strip_quotes( argument_list[0].strip() ).split('=')
            arg = strip_quotes(arg.strip())
            self.env.set(var, arg)
        elif len(argument_list) == 2:
            var, arg = argument_list
            arg = strip_quotes(arg.strip())
            self.env.set(var, arg)
        else:
            msg = str(ref) + reconstruct_line(tokens).strip()
            raise UnhandledTokenPattern, msg

        self.kh_shell_command(arg0, tokens, ref)

    def kh_shell_command(self, arg0, tokens, ref):
        linetext = reconstruct_line(tokens).strip()
        cmd = Command(self, arg0, self.pwd, linetext, self.env.getAll(), ref)
        self.commands.append(cmd)

    def kh_strcpy(self, arg0, tokens, ref):
        '''symbol assignment'''
        self.kh_symbol(arg0, tokens, ref)

    def kh_symbol(self, arg0, tokens, ref):
        '''symbol assignment'''
        arg = strip_quotes( tokens[2]['tokStr'] )
        obj = Symbol(self, arg0, arg, ref)
        self.symbols.set(arg0, obj)
        self.kh_shell_command('(symbol)', tokens, ref)


def reportRTYP(pv_dict):
    '''how many of each record type?'''
    rtyp_dict = {}
    for k, pv in pv_dict.items():
        if k != pv.NAME:
            rtype = 'alias'
        else:
            rtype = pv.RTYP
        if rtype not in rtyp_dict:
            rtyp_dict[rtype] = 0
        rtyp_dict[rtype] += 1
    tbl = pyRestTable.Table()
    tbl.labels = ['RTYP', 'count']
    for k, v in sorted(rtyp_dict.items()):
        tbl.rows.append([k, v])
    tbl.rows.append(['TOTAL', len(pv_dict)])
    return tbl.reST()


def main():
    owd = os.getcwd()
    cmdFile_dict = {}
    testfiles = []
    testfiles.append(os.path.join('.', 'testfiles', 'iocBoot', 'ioc495idc', 'st.cmd'))
    for i, tf in enumerate(testfiles):
        try:
            os.chdir(os.path.dirname(os.path.abspath(tf)))
            ref = FileRef(__file__, i, 0, 'testing')
            cmdFile_object = CommandFile(None, os.path.split(tf)[-1], {}, ref)
        except Exception:
            traceback.print_exc()
            continue
        print cmdFile_object
        cmdFile_dict[tf] = cmdFile_object
        for command in cmdFile_object.commands:
            print str(command.reference), str(command.args)
        
        # how many of each record type?
        print '\nTable: EPICS Records types used'
        print reportRTYP(cmdFile_object.pv_dict)


if __name__ == '__main__':
    main()

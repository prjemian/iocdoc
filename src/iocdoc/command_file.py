'''
EPICS IOC command file analysis
'''

import os
import token
import tokenize
import traceback

import database
import macros
import template
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions, reconstruct_line
from utils import logMessage, FileRef, strip_quotes


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

        # filename is a relative or absolute path to command file, no macros in the name
        self.source = text_file.read(filename)

        self.knownHandlers = {
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
            if line['pattern'].startswith( 'OP' ):
                pass
            elif line['pattern'].startswith( 'NAME' ):
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
        arg = reconstruct_line(tokens).strip()
        print str(ref), arg     # TODO: finish this
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
            dbFileName = parts[0].strip('"')
        if count > 1:
            for definition in parts[1].strip('"').split(','):
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

    def kh_dbLoadTemplate(self, arg0, tokens, ref):
        local_macros = macros.Macros(self.env.getAll())
        tfile = reconstruct_line(tokens).strip().strip('(').strip(')').strip('"')
        obj = template.Template(tfile, local_macros.getAll(), ref)
        self.template_list.append(obj)
        # TODO: anything else to be done?
        self.kh_shell_command(arg0, tokens, ref)

    def kh_epicsEnvSet(self, arg0, tokens, ref):
        '''symbol assignment'''
        var = strip_quotes( tokens[2]['tokStr'] )       # FIXME: fragile, assumes STRING and quotes and ...
        value = strip_quotes( tokens[4]['tokStr'] )
        self.env.set(var, value)
        self.kh_shell_command('(env)', tokens, ref)

    def _parse_includeCommandFile(self, arg0, tokens, ref):
        pass        # TODO: finish this

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


def main():
    cmdFile_dict = {}
    testfiles = []
    testfiles.append(os.path.join('.', 'testfiles', 'iocBoot', 'ioc495idc', 'st.cmd'))
    for i, tf in enumerate(testfiles):
        try:
            ref = FileRef(__file__, i, 0, 'testing')
            cmdFile_object = CommandFile(None, tf, {}, ref)
        except Exception:
            traceback.print_exc()
            continue
        print cmdFile_object
        cmdFile_dict[tf] = cmdFile_object
        for command in cmdFile_object.commands:
            print str(command.reference), str(command.args)


if __name__ == '__main__':
    main()

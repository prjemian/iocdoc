'''
EPICS IOC command file analysis
'''

import os
import traceback


import database
import macros
import reports
import template
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions, reconstruct_line
import utils


class UnhandledTokenPattern(Exception): pass


class Command(object):
    '''
    one command in an EPICS IOC command file
    '''

    def __init__(self, parent, command, path, args, ref, **env):
        self.parent = parent
        self.command = command
        self.path = path
        self.args = args
        self.env = macros.Macros(**env)
        self.reference = ref
        utils.logMessage('command: ' + command + ' ' + args, utils.LOGGING_DETAIL__MEDIUM)
    
    def __str__(self):
        return self.command + ' ' + str(self.args) + ' ' + str(self.env)


class CommandFile(object):
    '''
    analysis of an EPICS IOC command file
    '''

    def __init__(self, parent, filename, ref, **env):
        self.parent = parent
        self.filename = filename
        self.reference = ref
        self.pwd = os.getcwd()

        self.env = macros.Macros(**env)
        self.symbols = macros.Macros()
        self.database_list = []
        self.commands = []
        self.template_list = []
        self.includedCommandFile_list = []
        self.pv_dict = {}

        # filename is a relative or absolute path to command file, no macros in the name
        self.filename_absolute = os.path.abspath(filename)
        self.dirname_absolute = os.path.dirname(self.filename_absolute)
        utils.logMessage('command file: ' + filename, utils.LOGGING_DETAIL__IMPORTANT)
        # self.source = text_file.read(filename)
        self.source = text_file.read(self.filename_absolute)
        
        if parent is None:
            self.startup_directory = self.dirname_absolute
        else:
            self.startup_directory = parent.startup_directory

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
        '''make a :func:`FileRef()` instance for this item'''
        return utils.FileRef(self.filename, tok['start'][0], tok['start'][1], item or self)
    
    def parse(self):
        '''analyze this command file'''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename_absolute)
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

    def kh_cd(self, arg0, tokens, ref):
        path = reconstruct_line(tokens).strip()
        path = utils.strip_quotes(path)           # strip double-quotes
        if self.symbols.exists(path):       # symbol substitution
            path = self.symbols.get(path).value
        path = self.env.replace(path)       # macro substitution
        if len(path) == 0:
            path = self.startup_directory
        if len(path) > 0 and os.path.exists(path):
            if os.path.abspath(path) != os.getcwd():    # only cd if it is really different
                os.chdir(path)
                self.kh_shell_command(arg0, tokens, ref)
                utils.logMessage(arg0 + ' ' + path, utils.LOGGING_DETAIL__MEDIUM)
    
    def parse_macro_args(self, arg, ref, tokens, parent_macros):
        local_macros = macros.Macros(**parent_macros.db)
        for definition in utils.strip_quotes(arg).split(','):
            if definition.find('=') < 0:
                # if self.symbols.get(definition, None)
                # such as:  iocSubString=asdCreateSubstitutionString("IOC",iocprefix)
                msg = str(ref) + reconstruct_line(tokens).strip()
                utils.logMessage(msg, utils.LOGGING_DETAIL__IMPORTANT)
                #raise UnhandledTokenPattern, msg
            else:
                k, v = definition.split('=')
                local_macros.set(k.strip(), v.strip(), self, ref)
        return local_macros


    def kh_dbLoadRecords(self, arg0, tokens, ref):
        local_macros = macros.Macros(**self.env.db)
        full_line = reconstruct_line(tokens).strip()
        tokenLog = TokenLog()
        tokenLog.tokenList = tokens
        tokenLog.token_pointer = 1
        args = parse_bracketed_macro_definitions(tokenLog)
        nargs = len(args)
        if nargs not in (1, 2, 3,):
            msg = str(ref) + full_line
            raise UnhandledTokenPattern, msg
        utils.logMessage(arg0 + full_line, utils.LOGGING_DETAIL__NOISY)

        dbFileName = local_macros.replace(utils.strip_quotes(args[0]))

        if nargs in (2, 3,):    # accumulate additional macro definitions
            local_macros = self.parse_macro_args(args[1], ref, tokens, local_macros)

        if nargs in (3,):
            path = args[2]
            # msg = str(ref) + full_line
            if self.symbols.exists(path):   # substitute from symbol table
                path = self.symbols.get(path).value
            if os.path.exists(path):
                dbFileName = os.path.join(path, dbFileName)

        try:
            obj = database.Database(self, dbFileName, ref, **local_macros.db)
            self.database_list.append(obj)
            self.kh_shell_command(arg0, tokens, ref)
        except text_file.FileNotFound, _exc:
            msg = 'Could not find database file'
            utils.detailedExceptionLog(msg)
            return
        for k, v in obj.getPVs():
            self.pv_dict[k] = v

    def kh_dbLoadTemplate(self, arg0, tokens, ref):
        # TODO: Can one template call another?
        local_macros = macros.Macros(**self.env.db)
        args = utils.strip_parentheses(reconstruct_line(tokens).strip()).split(',')
        if len(args) in (1, 2):
            tfile = os.path.join(self.dirname_absolute, utils.strip_quotes(args[0]))
        if len(args) == 2:
            # such as in 8idi:  dbLoadTemplate("aiRegister.substitutions", top)
            # This is an ERROR.  The IOC should be corrected.
            '''from the EPICS documentation regarding dbLoadTemplate():
            
            dbLoadTemplate(char *subfile, char *substitutions)
            
            This IOC command reads a template substitutions file which 
            provides instructions for loading database instance files a
            nd gives values for the $(xxx) macros they may contain. 
            This command performs those substitutions while loading the 
            database instances requested.
            
            The subfile parameter gives the name of the template substitution file to be used. 
            The optional substitutions parameter may contain additional global macro values, 
            which can be overridden by values given within the substitution file.
            '''
            path = self.symbols.get(utils.strip_quotes(args[1]).strip(), None)
            if isinstance(path, macros.KVpair):
                alternative = os.path.join(path.value, tfile)
                if os.path.exists(alternative):
                    tfile = alternative
            else:
                msg = 'problem parsing: ' + arg0 + reconstruct_line(tokens).strip()
                utils.logMessage(msg, utils.LOGGING_DETAIL__IMPORTANT)
        obj = template.Template(tfile, ref, **local_macros.db)
        self.template_list.append(obj)
        self.database_list += obj.database_list
        self.kh_shell_command(arg0, tokens, ref)
        for k, v in obj.getPVs():
            self.pv_dict[k] = v

    def kh_epicsEnvSet(self, arg0, tokens, ref):
        '''symbol assignment'''
        if len(tokens) == 7:
            var = tokens[2]['tokStr']
            value = tokens[4]['tokStr']
        else:
            text = utils.strip_parentheses(reconstruct_line(tokens).strip())
            parts = text.split(',')
            if len(parts) == 1:
                parts = text.split(' ')
            if len(parts) != 2:
                raise UnhandledTokenPattern('epicsEnvSet'+text)
            var, value = parts
        self.env.set(utils.strip_quotes( var ), utils.strip_quotes( value ), self, ref)
        self.kh_shell_command(arg0, tokens, ref)

    def kh_loadCommandFile(self, arg0, tokens, ref):
        fname = utils.strip_parentheses(reconstruct_line(tokens).strip())
        # fname is given relative to current working directory
        fname_expanded = self.env.replace(fname)
        self.kh_shell_command('<', tokens, ref)
        # FIXME: also need to pass self.symbols
        obj = CommandFile(self, fname_expanded, ref, **self.env.db)
        self.includedCommandFile_list.append(obj)

        self.commands += obj.commands
        self.template_list += obj.template_list
        self.database_list += obj.database_list
        self.symbols.setMany(**obj.symbols.db)
        self.env.setMany(**obj.env.db)
        for k, v in obj.pv_dict.items():
            self.pv_dict[k] = v

    def kh_putenv(self, arg0, tokens, ref):
        '''
        process an instance of putenv

        :param tokens: token list
        :param ref: instance of :class:`FileRef`
        :raise UnhandledTokenPattern: unhandled token pattern
        '''
        argument_list = []
        for tkn in tokens[1:]:
            if tkn['tokName'] == 'STRING':
                argument_list.append( tkn['tokStr'] )

        if len(argument_list) == 1:
            var, arg = utils.strip_quotes( argument_list[0].strip() ).split('=')
            arg = utils.strip_quotes(arg.strip())
            self.env.set(var, arg, self, ref)
        elif len(argument_list) == 2:
            var, arg = argument_list
            arg = utils.strip_quotes(arg.strip())
            self.env.set(var, arg)
        else:
            msg = str(ref) + reconstruct_line(tokens).strip()
            raise UnhandledTokenPattern, msg

        self.kh_shell_command(arg0, tokens, ref)

    def kh_shell_command(self, arg0, tokens, ref):
        linetext = reconstruct_line(tokens).strip()
        cmd = Command(self, arg0, self.pwd, linetext, ref, **self.env.db)
        self.commands.append(cmd)

    def kh_strcpy(self, arg0, tokens, ref):
        '''symbol assignment'''
        self.kh_symbol(arg0, tokens, ref)

    def kh_symbol(self, arg0, tokens, ref):
        '''symbol assignment'''
        # TODO: handle this:  sym=func(key,value)
        # iocSubString=asdCreateSubstitutionString("IOC",iocprefix)
        arg = utils.strip_quotes( tokens[2]['tokStr'] )
        self.symbols.set(arg0, arg, self, ref)
        self.kh_shell_command(arg0, tokens, ref)


def main():
    owd = os.getcwd()
    cmdFile_dict = {}
    testfiles = []
    testfiles.append(os.path.join('.', 'testfiles', 'iocBoot', 'ioc495idc', 'st.cmd'))
    IOC_NAME = 'testing'
    env = {}
    for i, tf in enumerate(testfiles):
        try:
            os.chdir(os.path.dirname(os.path.abspath(tf)))
            ref = utils.FileRef(__file__, i, 0, 'testing')
            cmdFile_object = CommandFile(None, os.path.split(tf)[-1], ref, **env)
        except Exception:
            traceback.print_exc()
            continue
        cmdFile_dict[tf] = cmdFile_object
        
        os.chdir(owd)
        reports.reportCmdFile(cmdFile_object, IOC_NAME)


if __name__ == '__main__':
    main()

'''
ioc.py - describe an EPICS IOC by examining its startup command file

EXAMPLE COMMAND-LINE USAGE::

    iocdoc ../path/to/st.cmd


EXAMPLE PYTHON USAGE::

    import iocdoc
    ioc = iocdoc.Ioc('../path/to/st.cmd')
    ioc.parse()
    ioc.expand_macros()
    ioc.report()

'''


import os

import command_file
import text_file


class Ioc(object):
    '''
    complete analysis of a single EPICS IOC
    '''
    
    def __init__(self, filename):
        self.st_cmd = text_file.read(filename)
        self.ioc_name = None    # TODO: How to determine this?
        self.commands = command_file.CommandFile(self, self.st_cmd, os.environ)
    
    def expand_macros(self):
        '''replace all known macros with their values'''
        pass

    def parse(self):
        '''analyze this IOC'''
        pass
    
    def report(self):
        '''describe what was discovered'''
        # TODO: this is the development version
        for key in sorted(text_file.keys()):
            print key
        print '-'*20
        print 'cwd', self.st_cmd.cwd
        print 'filename', self.st_cmd.filename
        print '|filename|', self.st_cmd.absolute_filename
        print '|dir|', self.st_cmd.absolute_directory
        print 'len(file)[lines, chars]', self.st_cmd.number_of_lines, self.st_cmd.bytes


def process_command_line():
    '''
    support command-line options such as ```--help``` and ```--version```
    '''
    import argparse
    import iocdoc
    version = iocdoc.__version__
    doc = iocdoc.__doc__
    doc = 'v' + version + ', ' + doc.strip()
    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument('command_file', 
                        action='store', 
                        #nargs='?', 
                        help="EPICS IOC command file name")
    parser.add_argument('-v', '--version', action='version', version=version)
    return parser.parse_args()


def main():
    cli = process_command_line()
    ioc = Ioc(cli.command_file)
    ioc.parse()
    ioc.report()


def main___developer_use():
    import sys
    test_ioc = os.path.join('..', '..', 'IOCs', 'OPC_SoftIOC', 'demo', 'st.cmd')
    # sys.argv.append('-h')
    # sys.argv.append('-v')
    sys.argv.append(test_ioc)
    main()


if __name__ == '__main__':
    # main()
    main___developer_use()  # developer-only : remove when release

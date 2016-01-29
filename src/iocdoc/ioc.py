'''
ioc.py - describe this IOC

EXAMPLE COMMAND-LINE USAGE::

    iocdoc ../path/to/st.cmd


EXAMPLE PYTHON USAGE::

    import iocdoc
    ioc = iocdoc.Ioc('../path/to/st.cmd')
    ioc.parse()
    ioc.report()

'''


import os

import command_file


class Ioc(object):
    '''
    complete analysis of a single EPICS IOC
    '''
    
    def __init__(self, filename, file_cache={}):
        self.ioc_name = None    # TODO: How to determine this?
        self.file_cache = file_cache
        self.commands = command_file.CommandFile(self, filename, self.file_cache, {})
    
    def parse(self):
        '''analyze this IOC'''
        pass
    
    def report(self):
        '''describe what was discovered'''
        print 'cwd', self.commands.cwd
        print 'filename', self.commands.filename
        print '|filename|', self.commands.absolute_filename
        print '|dir|', self.commands.absolute_directory


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
    pass


if __name__ == '__main__':
    # main()
    main___developer_use()  # developer-only : remove when release

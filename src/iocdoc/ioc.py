'''
ioc.py - describe this IOC
'''


import os

import command_file


class Ioc(object):
    '''
    complete analysis of a single EPICS IOC
    '''
    
    def __init__(self, filename):
        self.commands = command_file.CommandFile(self, filename, {})
        self.ioc_name = None    # TODO: How to determine this?


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


def main___developer_use():
    import sys
    test_ioc = os.path.join('..', '..', 'IOCs', 'OPC_SoftIOC', 'demo', 'st.cmd')
    # sys.argv.append('-h')
    # sys.argv.append('-v')
    sys.argv.append(test_ioc)
    cli = process_command_line()
    ioc = Ioc(cli.command_file)
    print 'cwd', ioc.commands.cwd
    print 'filename', ioc.commands.filename
    print '|filename|', ioc.commands.absolute_filename
    print '|dir|', ioc.commands.absolute_directory
    pass


if __name__ == '__main__':
    main___developer_use()

'''
ioc.py - describe this IOC
'''

class IOC(object):
    
    def __init__(self, command_file):
        self.command_file = command_file


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
                        nargs='+', 
                        help="EPICS IOC command file name")
    parser.add_argument('-v', '--version', action='version', version=version)
    return parser.parse_args()


if __name__ == '__main__':
    cli = process_command_line()

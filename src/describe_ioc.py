#!/usr/bin/env python

'''
use iocdoc to document a single APS IOC
'''

import os
import iocdoc.command_file
import iocdoc.reports
from iocdoc.utils import FileRef


def describe(ioc_name, st_cmd):
    filename = os.path.abspath(st_cmd)
    path = os.path.dirname(filename)

    owd = os.getcwd()
    os.chdir(path)
    ref = FileRef(__file__, 0, 0, ioc_name)
    env = {}
    obj = iocdoc.command_file.CommandFile(None, os.path.split(filename)[-1], ref, **env)
    
    os.chdir(owd)
    iocdoc.reports.reportCmdFile(obj, ioc_name)


def get_command_line_parameters():
    '''
    support user-supplied command-line parameters
    '''
    import argparse
    doc = __doc__
    doc = doc.strip()
    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument('IOC_name', 
                        action='store', 
                        help="IOC name")
    parser.add_argument('st_cmd', 
                        action='store', 
                        help="IOC startup script file name")
    return parser.parse_args()


def main():
    parms = get_command_line_parameters()
    if not os.path.exists(parms.st_cmd):
        raise RuntimeError('file not found: ' + parms.st_cmd)
    describe(parms.IOC_name, parms.st_cmd)


if __name__ == '__main__':
    import sys
    sys.argv += 'ioc33idd /net/s33dserv/xorApps/epics/synApps_5_6/ioc/33idd/iocBoot/ioc33idd/st.cmd'.split()
    main()

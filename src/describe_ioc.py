#!/usr/bin/env python

'''
use iocdoc to document a single APS IOC
'''

import os
import iocdoc.command_file
import iocdoc.reports
from iocdoc.utils import FileRef


def describe(ioc_name, st_cmd, output_path=None):
    filename = os.path.abspath(st_cmd)
    path = os.path.dirname(filename)

    owd = os.getcwd()
    os.chdir(path)
    ref = FileRef(__file__, 0, 0, ioc_name)
    env = {}
    obj = iocdoc.command_file.CommandFile(None, os.path.split(filename)[-1], ref, **env)
    
    os.chdir(owd)
    if output_path is None:
        iocdoc.reports.reportCmdFile(obj, ioc_name)
    else:
        os.chdir(output_path)
        iocdoc.reports.writeReports(obj, ioc_name)
        os.chdir(owd)


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
    parser.add_argument('output_dir', 
                        action='store', 
                        help="directory for program output")
    return parser.parse_args()


def main():
    parms = get_command_line_parameters()
    if not os.path.exists(parms.st_cmd):
        raise RuntimeError('file not found: ' + parms.st_cmd)
    if parms.output_dir is not None and not os.path.exists(parms.output_dir):
        raise RuntimeError('output directory not found: ' + parms.output_dir)
    describe(parms.IOC_name, parms.st_cmd, parms.output_dir)


if __name__ == '__main__':
    import sys
    # sys.argv += '9idcH1003 /net/s9dserv/xorApps/epics/synApps_5_8/ioc/9idcH1003/iocBoot/ioc9idcH1003/st.cmd  ./out'.split()
    # sys.argv += '33idd /net/s33dserv/xorApps/epics/synApps_5_6/ioc/33idd/iocBoot/ioc33idd/st.cmd ./out'.split()
    #sys.argv += '8idi /net/s8dserv/xorApps/epics/synApps_5_7/ioc/8id/iocBoot/ioc8idi/st.cmd ./out'.split()
    main()

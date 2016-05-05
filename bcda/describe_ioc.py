#!/usr/bin/env python

'''
use iocdoc to document a single APS IOC
'''

import os
import iocdoc.command_file
import iocdoc.reports
import iocdoc.utils


def describe(ioc_name, st_cmd, output_path=None):
    filename = os.path.abspath(st_cmd)
    path = os.path.dirname(filename)

    owd = os.getcwd()
    os.chdir(path)
    ref = iocdoc.utils.FileRef(__file__, 0, 0, ioc_name)
    env = {}
    iocdoc.utils.logMessage('IOC startup file: ' + st_cmd, iocdoc.utils.LOGGING_DETAIL__CERTAIN)
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
    msg = '(integer) level of detail as IOC files are parsed ' 
    parser.add_argument('-l', 
                        '--log_file',
                        dest='log_file', 
                        help='output file to store program logs',
                        default=iocdoc.utils.LOG_FILE)
    parser.add_argument('--reporting-level',
                        dest='reporting_level', 
                        help=msg, 
                        type=int, 
                        choices=iocdoc.utils.LOGGING_DETAIL_LEVELS,
                        default=iocdoc.utils.LOGGING_DETAIL__MEDIUM)
    return parser.parse_args()


def main():
    parms = get_command_line_parameters()
    if not os.path.exists(parms.st_cmd):
        raise RuntimeError('file not found: ' + parms.st_cmd)
    if parms.output_dir is not None and not os.path.exists(parms.output_dir):
        raise RuntimeError('output directory not found: ' + parms.output_dir)
    iocdoc.utils.LOG_FILE = parms.log_file
    iocdoc.utils.LOGGING_DETAIL = parms.reporting_level
    describe(parms.IOC_name, parms.st_cmd, parms.output_dir)


if __name__ == '__main__':
    # 9idcH1003 /net/s9dserv/xorApps/epics/synApps_5_8/ioc/9idcH1003/iocBoot/ioc9idcH1003/st.cmd  ./out
    # 33idd     /net/s33dserv/xorApps/epics/synApps_5_6/ioc/33idd/iocBoot/ioc33idd/st.cmd         ./out
    # 8idi      /net/s8dserv/xorApps/epics/synApps_5_7/ioc/8id/iocBoot/ioc8idi/st.cmd             ./out
    main()

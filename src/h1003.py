
'''
example use of iocdoc to document a single APS IOC
'''

import os
#import iocdoc
import iocdoc.command_file
import iocdoc.reports
from iocdoc.utils import logMessage, FileRef, strip_quotes

IOC_NAME = '9idcH1003'

cmdFile = '/net/s9dserv/xorApps/epics/synApps_5_8/ioc/9idcH1003/iocBoot/ioc9idcH1003/st.cmd'
owd = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(cmdFile)))
ref = FileRef(__file__, 0, 0, IOC_NAME)
obj = iocdoc.command_file.CommandFile(None, os.path.split(cmdFile)[-1], ref, {})

os.chdir(owd)
iocdoc.reports.reportCmdFile(obj, IOC_NAME)

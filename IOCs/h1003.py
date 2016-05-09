
'''
example use of iocdoc to document a single APS IOC
'''

import os
import sys
sys.path.append(os.path.join('..', 'src'))
import iocdoc


IOC_NAME = '9idcH1003'
cmdFile = '/net/s9dserv/xorApps/epics/synApps_5_8/ioc/9idcH1003/iocBoot/ioc9idcH1003/st.cmd'
iocdoc.describe_ioc.describe(IOC_NAME, cmdFile)

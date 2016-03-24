
'''
example use of iocdoc to document a single APS IOC
'''

import describe_ioc


IOC_NAME = '9idcH1003'
cmdFile = '/net/s9dserv/xorApps/epics/synApps_5_8/ioc/9idcH1003/iocBoot/ioc9idcH1003/st.cmd'
describe_ioc.describe(IOC_NAME, cmdFile)

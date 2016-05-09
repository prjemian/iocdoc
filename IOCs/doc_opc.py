
'''
Example documentation of a Windows IOC from DESY

:see: http://www-csr.bessy.de/control/SoftDist/OPCsupport/
'''

import os
import sys

sys.path.append(os.path.join('..', 'src'))

import iocdoc


def main():
    ioc_name = 'OPC_SoftIOC'
    st_cmd = os.path.join(ioc_name, 'demo', 'st.cmd')
    doc_path = os.path.join('docs', ioc_name)
    iocdoc.describe_ioc.describe(ioc_name, st_cmd, doc_path, True)


if __name__ == '__main__':
    main()

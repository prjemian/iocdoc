
# Copyright (c) 2011 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
Source code for the iocdoc package
'''

# '''
# Will it be necessary to add this next line at the top of every file?
# # -*- coding: iso-8859-1 -*- 
# '''

from . import describe_ioc
from . import reports

__package_name__        = u'iocdoc'

from _version import git_release
__version__ = u'0.0.2'
__release__ = git_release(__package_name__, __version__)

__description__         = u'Document the configuration of an EPICS IOC'
__long_description__    = __description__

__author__              = u'Pete R. Jemian'
__email__               = u'jemian@anl.gov'
__institution__         = u"Advanced Photon Source, Argonne National Laboratory"
__settings_orgName__    = u'Advanced_Photon_Source'
__author_name__         = __author__
__author_email__        = __email__

__copyright__           = u'2011-2016, UChicago Argonne, LLC'
# __license_url__         = u''
__license__             = u'UChicago Argonne, LLC OPEN SOURCE LICENSE (see LICENSE file)'
__url__                 = u'http://iocdoc.readthedocs.org'
__download_url__        = u'https://github.com/prjemian/iocdoc.git'
__keywords__            = ['APS', 'EPICS', 'IOC']
#__requires__            = ['PyQt4', 'lxml', 'pyRestTable']
__requires__            = ['lxml', 'pyRestTable']
__documentation_mocks__ = ['lxml', 'pyRestTable']       # do NOT mock PyQt4 here, big problems if you do

__classifiers__ = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: Free To Use But Restricted',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering',
            'Topic :: Utilities',
                     ]

# as shown in the About box ...
__credits__ = u'author: ' + __author__
__credits__ += u'\nemail: ' + __email__
__credits__ += u'\ninstitution: ' + __institution__
__credits__ += u'\nURL: ' + __url__


IOCDOC
######

Overview
********

:version: |version|
:published: |today|

IOCDOC: Document the configuration of an EPICS IOC

In EPICS, an IOC is the server, coordinating hardware actions 
with software configuration, command, and control.

This project arose from a user request: 
*What does my EPICS system provide? Tell me about all the PVs.*

Operation of an IOC begins with a command to a executable, compiled 
for the host computer architecture, and a startup script, often called
``st.cmd`` by convention.  All necessary configuration information is 
provided in the startup script or through the environment variables
from the host operating system when the startup script is launched.

It is possible, by parsing the startup script, to document the implementation
of the IOC and that is the goal of this package.  Reference to well-known
IOC commands (such as ``dbLoadRecords``), packages (such as ``synApps``), 
and the chosen EPICS base version will be provided.

Output is in the form of a set of HTML pages for human consumption
and a set of XML files for machine processing.  Reference to any 
additional HTML documentation provided in the IOC's directory structure 
will be included.

Contents:

.. toctree::
   :maxdepth: 1
   :glob:
   
   readme
   src/*
   changes
   license

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


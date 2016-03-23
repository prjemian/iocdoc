# vxWorks startup script

sysVmeMapShow

# For devIocStats
#!epicsEnvSet("ENGINEER", "staff")
#!epicsEnvSet("LOCATION", "495ID")
putenv("ENGINEER=staff")
putenv("LOCATION=495ID-C")
putenv("GROUP=BL")

cd ""
< ../nfsCommands
< cdCommands

putenv("TOP=../..")
putenv("STARTUP=$(TOP)/iocBoot/ioc495idc")
putenv("ALIVE=$(TOP)")
putenv("AUTOSAVE=$(TOP)")
putenv("DEVIOCSTATS=$(TOP)")
putenv("IP330=$(TOP)")
putenv("MCA=$(TOP)")
putenv("MOTOR=$(TOP)")
putenv("OPTICS=$(TOP)")
putenv("SSCAN=$(TOP)")
putenv("STD=$(TOP)")

# How to set and get the clock rate (in Hz.  Default is 60 Hz)
#sysClkRateSet(100)
#sysClkRateGet()

################################################################################
cd topbin

# If the VxWorks kernel was built using the project facility, the following must
# be added before any C++ code is loaded (see SPR #28980).
sysCplusEnable=1

### Load synApps EPICS software
### doesn't work for tornado 2.2.2 ### ld < 495idc.munch
load("495idc.munch")
cd startup

# Increase size of buffer for error logging from default 1256
errlogInit(20000)

# need more entries in wait/scan-record channel-access queue?
recDynLinkQsize = 1024

# Specify largest array CA will transport
# Note for N sscanRecord data points, need (N+1)*8 bytes, else MEDM
# plot doesn't display
putenv "EPICS_CA_MAX_ARRAY_BYTES=64008"

# set the protocol path for streamDevice
epicsEnvSet("STREAM_PROTOCOL_PATH", ".")

################################################################################
# Tell EPICS all about the record types, device-support modules, drivers,
# etc. in the software we just loaded (495idc.munch)
dbLoadDatabase("$(TOP)/dbd/ioc495idcVX.dbd")
ioc495idcVX_registerRecordDeviceDriver(pdbbase)

### save_restore setup
# We presume a suitable initHook routine was compiled into 495idc.munch.
# See also create_monitor_set(), after iocInit() .
< cmds/save_restore.cmd

# Industry Pack support
< cmds/industryPack.cmd

# VME devices
< cmds/vme.cmd

# IAI X-Sel support - ONLY UNCOMMENT WHEN DET EBRICK IS OFFLINE
#< cmds/IAI.cmd
#dbLoadRecords("$(TOP)/databases/asynRecordAliases.db","P=495idc:,R=port09,PA=495idcDET:,RA=port09")
#dbLoadRecords("$(TOP)/databases/iai_controlsAliases.db","P=495idc:,R=IAI:,PA=495idcDET:,RA=IAI:")
#dbLoadRecords("$(TOP)/databases/detBaseAliases.db","P=495idc:,H=base:,PA=495idcDET:,HA=base:")
#dbLoadRecords("$(TOP)/databases/detRobotAliases.db","P=495idc:,H=robot:,PA=495idcDET:,HA=robot:")

# Motors
dbLoadTemplate("templates/omsMotors")
dbLoadTemplate("$(STARTUP)/templates/motor.substitutions")
iocshCmd "epicsThreadSleep(5.0)"
dbLoadTemplate("$(STARTUP)/templates/softMotor.substitutions")
# Create PV aliases so old medm screens can be used
dbLoadRecords("$(TOP)/databases/motorAliases.db")

# Slits
#< cmds/slits.cmd
# Create PV aliases so old medm screens can be used
#dbLoadRecords("$(TOP)/databases/slitAliases.db")

# pf4 filters
dbLoadTemplate("$(STARTUP)/templates/filter.substitutions")

# digitelPump support - ONLY UNCOMMENT WHEN NES EBRICK IS OFFLINE
#< cmds/digitelPump.cmd
# Create PV aliases so old medm screens can be used
#dbLoadRecords("$(TOP)/databases/digitelPumpAliases.db","P=495idc:,PUMP=IP01,PA=495idcNES:,PUMPA=IP01")
#dbLoadRecords("$(TOP)/databases/digitelPumpAliases.db","P=495idc:,PUMP=IP02,PA=495idcNES:,PUMPA=IP02")

# table records
dbLoadTemplate("$(STARTUP)/templates/table.substitutions")

# Load database records for Femto amplifiers/photodiode
#!dbLoadRecords("$(STD)/stdApp/Db/femto.db","P=495idc:,H=fem01:,F=seq01:")
# Create PV aliases so old medm screens can be used
#!dbLoadRecords("$(TOP)/databases/femtoAliases.db","P=495idc:,H=fem01:,F=seq01:,PA=495idcnpi:,HA=fem01:,FA=seq01:")

### Allstop, alldone
dbLoadRecords("$(MOTOR)/databases/motorUtil.db", "P=495idc:")
# Create PV aliases so old medm screens can be used
dbLoadRecords("$(TOP)/databases/allstopAliases.db")

### Scan-support software
# crate-resident scan.  This executes 1D, 2D, 3D, and 4D scans, and caches
# 1D data, but it doesn't store anything to disk.  (See 'saveData' below for that.)
putenv "SDB=$(SSCAN)/databases/standardScans.db"
dbLoadRecords("$(SDB)","P=495idc:,MAXPTS1=8000,MAXPTS2=1000,MAXPTS3=10,MAXPTS4=10,MAXPTSH=8000")
dbLoadRecords("$(TOP)/databases/saveData.db","P=495idc:")
dbLoadRecords("$(TOP)/databases/scanProgress.db","P=495idc:scanProgress:")
# Create PV aliases so old medm screens can be used
dbLoadRecords("$(TOP)/databases/sscanAliases.db")

#< cmds/user.cmd
# Create PV aliases so old medm screens can be used
#dbLoadRecords("$(TOP)/databases/userAliases.db")
#dbLoadRecords("$(TOP)/databases/placeholderAliases.db")

# Miscellaneous PV's, such as burtResult
dbLoadRecords("$(STD)/databases/misc.db","P=495idc:")

# devIocStats
dbLoadRecords("$(DEVIOCSTATS)/databases/iocAdminVxWorks.db","IOC=495idc")

# alive
dbLoadRecords("$(ALIVE)/databases/alive.db", "P=495idc:,RHOST=10.10.10.10")

###############################################################################
# Set shell prompt (otherwise it is left at mv167 or mv162)
shellPromptSet "ioc495idc> "
iocLogDisable=0
iocInit
###############################################################################

# Stop pump support from polling
dbpf "495idc:IP01.SCAN", "0"
dbpf "495idc:IP02.SCAN", "0"

# write all the PV names to a local file
dbl > all.dbl

### Startup State Notation Language (SNL) programs
# NOTE: Command line limited to 128 characters

# new filterDrive seq program
seq &filterDrive,"NAME=filterDrive,P=495idc:,R=filter:,NUM_FILTERS=4"

# femto
#s = "name=fem1,P=495idc:,H=fem01:,F=seq01:,G1=495idc:Unidig1:Bo9,
#     G2=495idc:Unidig1:Bo10,G3=495idc:Unidig11:Bo,NO=495idc:Unidig1:Bo13"
#!seq femto, s

# This SNL programs reads the MCS
seq(&SIS38XX_SNL, "P=495idc:3820:, R=mca, NUM_SIGNALS=8, FIELD=READ")

# Implements for scanProgress.db
seq &scanProgress, "S=495idc:, P=495idc:scanProgress:"

### Start up the autosave task and tell it what to do.
# The task is actually named "save_restore".

# Note that you can reload these sets after creating them: e.g., 
# reload_monitor_set("auto_settings.req",30,"P=495idc:")
#
# save positions every five seconds
create_monitor_set("auto_positions.req",5,"P=495idc:")
# save other things every thirty seconds
create_monitor_set("auto_settings.req",30,"P=495idc:")

### Start the saveData task.  If you start this task, scan records mentioned
# in saveData.req will *always* write data files.  There is no programmable
# disable for this software.
saveData_Init("saveData.req", "P=495idc:")

# Diagnostic: CA links in all records
#dbcar(0,1)

# motorUtil (allstop & alldone)
motorUtilInit("495idc:")

# print the time our boot was finished
date

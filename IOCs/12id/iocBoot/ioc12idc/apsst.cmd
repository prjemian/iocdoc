# vxWorks startup script

sysVmeMapShow

# for vxStats
#putenv "engineer=not me"
#putenv "location=Earth"
engineer="not me"
location="Earth"

#for new daylight saving time 
putenv "TIMEZONE=CUS::360:031102:110402"


cd ""
< ../nfsCommands
< cdCommands

# How to set and get the clock rate
#sysClkRateSet(100)
#sysClkRateGet()

################################################################################
cd topbin

# If the VxWorks kernel was built using the project facility, the following must
# be added before any C++ code is loaded (see SPR #28980).
sysCplusEnable=1

# If using a PowerPC CPU with more than 32MB of memory, and not building with longjump, then
# allocate enough memory here to force code to load in lower 32 MB.
##mem = malloc(1024*1024*96)

### Load synApps EPICS software
### doesn't work for tornado 2.2.2 ### ld < 12idc.munch
ld(0,0,"12idc.munch")
cd startup

# Increase size of buffer for error logging from default 1256
errlogInit(20000)

# override address, interrupt vector, etc. information in module_types.h
#module_types()

# need more entries in wait/scan-record channel-access queue?
recDynLinkQsize = 1024

# Specify largest array CA will transport
# Note for N sscanRecord data points, need (N+1)*8 bytes, else MEDM
# plot doesn't display
putenv "EPICS_CA_MAX_ARRAY_BYTES=64008"

# set the protocol path for streamDevice
#epicsEnvSet("STREAM_PROTOCOL_PATH", ".")

################################################################################
# Tell EPICS all about the record types, device-support modules, drivers,
# etc. in the software we just loaded (12idc.munch)
dbLoadDatabase("$(TOP)/dbd/ioc12idcVX.dbd")
ioc12idcVX_registerRecordDeviceDriver(pdbbase)

# user-assignable ramp/tweak
#*dbLoadRecords("$(STD)/stdApp/Db/ramp_tweak.db","P=12idc:,Q=rt1")

### save_restore setup
# We presume a suitable initHook routine was compiled into 12idc.munch.
# See also create_monitor_set(), after iocInit() .
< save_restore.cmd

# Industry Pack support
< industryPack.cmd

# serial support
< serial.cmd

# gpib support
#< gpib.cmd

# VME devices
< vme.cmd

# CAMAC hardware
#<camac.cmd

# Motors
#dbLoadTemplate("basic_motor.substitutions")
dbLoadTemplate("motor.substitutions")
dbLoadTemplate("softMotor.substitutions")
#dbLoadTemplate("pseudoMotor.substitutions")

### Allstop, alldone
dbLoadRecords("$(MOTOR)/db/motorUtil.db", "P=12idc:")

### streamDevice example
#dbLoadRecords("$(TOP)/12idcApp/Db/streamExample.db","P=12idc:,PORT=serial1")

### Insertion-device control
#dbLoadRecords("$(STD)/stdApp/Db/IDctrl.db","P=12idc:,xx=02us")

### Scan-support software
# crate-resident scan.  This executes 1D, 2D, 3D, and 4D scans, and caches
# 1D data, but it doesn't store anything to disk.  (See 'saveData' below for that.)
dbLoadTemplate("standardScans.substitutions")
dbLoadRecords("$(SSCAN)/sscanApp/Db/saveData.db","P=12idc:")

# A set of scan parameters for each positioner.  This is a convenience
# for the user.  It can contain an entry for each scannable thing in the
# crate.
dbLoadTemplate("scanParms.substitutions")

### Slits
#dbLoadRecords("$(OPTICS)/opticsApp/Db/2slit.db","P=12idc:,SLIT=Slit1V,mXp=m5,mXn=m6")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/2slit.db","P=12idc:,SLIT=Slit1H,mXp=m7,mXn=m8")

# X-ray Instrumentation Associates Huber Slit Controller
# supported by a customized version of the SNL program written by Pete Jemian
# (Uses asyn record loaded separately)
#dbLoadRecords("$(OPTICS)/opticsApp/Db/xia_slit.db", "P=12idc:, HSC=hsc1:")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/xia_slit.db", "P=12idc:, HSC=hsc2:")

### 2-post mirror
#dbLoadRecords("$(OPTICS)/opticsApp/Db/2postMirror.db","P=12idc:,Q=M1,mDn=m8,mUp=m7,LENGTH=0.3")

### User filters
#dbLoadRecords("$(OPTICS)/opticsApp/Db/filterMotor.db","P=12idc:,Q=fltr1:,MOTOR=m1,LOCK=fltr_1_2:")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/filterMotor.db","P=12idc:,Q=fltr2:,MOTOR=m2,LOCK=fltr_1_2:")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/filterLock.db","P=12idc:,Q=fltr2:,LOCK=fltr_1_2:,LOCK_PV=12idc:DAC1_1.VAL")

### Optical tables
#tableRecordDebug=1
#putenv "DIR=$(OPTICS)/opticsApp/Db"
#dbLoadRecords("$(DIR)/table.db","P=12idc:,Q=Table1,T=table1,M0X=m1,M0Y=m2,M1Y=m3,M2X=m4,M2Y=m5,M2Z=m6,GEOM=SRI")

# Io calculation
#dbLoadRecords("$(OPTICS)/opticsApp/Db/Io.db","P=12idc:Io:")

### Monochromator support ###
# Kohzu and PSL monochromators: Bragg and theta/Y/Z motors
# standard geometry (geometry 1)
#dbLoadRecords("$(OPTICS)/opticsApp/Db/kohzuSeq.db","P=12idc:,M_THETA=m9,M_Y=m10,M_Z=m11,yOffLo=17.4999,yOffHi=17.5001")
# modified geometry (geometry 2)
#dbLoadRecords("$(OPTICS)/opticsApp/Db/kohzuSeq.db","P=12idc:,M_THETA=m9,M_Y=m10,M_Z=m11,yOffLo=4,yOffHi=36")

# Spherical grating monochromator
#dbLoadRecords("$(OPTICS)/opticsApp/Db/SGM.db","P=12idc:,N=1,M_x=m7,M_rIn=m6,M_rOut=m8,M_g=m9")

# 4-bounce high-resolution monochromator
#dbLoadRecords("$(OPTICS)/opticsApp/Db/hrSeq.db","P=12idc:,N=1,M_PHI1=m9,M_PHI2=m10")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/hrSeq.db","P=12idc:,N=2,M_PHI1=m11,M_PHI2=m12")

### Orientation matrix, four-circle diffractometer (see seq program 'orient' below)
#dbLoadRecords("$(OPTICS)/opticsApp/Db/orient.db", "P=12idc:,O=1,PREC=6")
#dbLoadTemplate("orient_xtals.substitutions")

# Coarse/Fine stage
#dbLoadRecords("$(OPTICS)/opticsApp/Db/CoarseFineMotor.db","P=12idc:cf1:,PM=12idc:,CM=m7,FM=m8")

# Load single element Canberra AIM MCA and ICB modules
#< canberra_1.cmd

# Load 13 element detector software
#< canberra_13.cmd

# Load 3 element detector software
#< canberra_3.cmd

### Stuff for user programming ###
dbLoadRecords("$(CALC)/calcApp/Db/userCalcs10.db","P=12idc:")
dbLoadRecords("$(CALC)/calcApp/Db/userCalcOuts10.db","P=12idc:")
dbLoadRecords("$(CALC)/calcApp/Db/userStringCalcs10.db","P=12idc:")
aCalcArraySize=2000
dbLoadRecords("$(CALC)/calcApp/Db/userArrayCalcs10.db","P=12idc:,N=2000")
dbLoadRecords("$(CALC)/calcApp/Db/userTransforms10.db","P=12idc:")
dbLoadRecords("$(CALC)/calcApp/Db/userAve10.db","P=12idc:")
# string sequence (sseq) records
dbLoadRecords("$(STD)/stdApp/Db/userStringSeqs10.db","P=12idc:")
# 4-step measurement
#dbLoadRecords("$(STD)/stdApp/Db/4step.db", "P=12idc:")
# interpolation
#dbLoadRecords("$(CALC)/calcApp/Db/interp.db", "P=12idc:,N=2000")
# array test
#dbLoadRecords("$(CALC)/calcApp/Db/arrayTest.db", "P=12idc:,N=2000")

# pvHistory (in-crate archive of up to three PV's)
#dbLoadRecords("$(STD)/stdApp/Db/pvHistory.db","P=12idc:,N=1,MAXSAMPLES=1440")

# software timer
#dbLoadRecords("$(STD)/stdApp/Db/timer.db","P=12idc:,N=1")

# Slow feedback
#dbLoadTemplate "pid_slow.substitutions"

# Miscellaneous PV's, such as burtResult
#dbLoadRecords("$(STD)/stdApp/Db/misc.db","P=12idc:")
#dbLoadRecords("$(STD)/stdApp/Db/VXstats.db","P=12idc:")
# vxStats
dbLoadTemplate("vxStats.substitutions")

### Queensgate piezo driver
#dbLoadRecords("$(IP)/ipApp/Db/pzt_3id.db","P=12idc:")
#dbLoadRecords("$(IP)/ipApp/Db/pzt.db","P=12idc:,PORT=")

### Queensgate Nano2k piezo controller
#dbLoadRecords("$(STD)/stdApp/Db/Nano2k.db","P=12idc:,S=s1")





### Load database records for Femto amplifiers
#dbLoadRecords("$(STD)/stdApp/Db/femto.db","P=12idc:,H=fem01:,F=seq01:")

### Load database records for dual PF4 filters
#dbLoadRecords("$(OPTICS)/opticsApp/Db/pf4common.db","P=12idc:,H=pf4:,A=A,B=B")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/pf4bank.db","P=12idc:,H=pf4:,B=A")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/pf4bank.db","P=12idc:,H=pf4:,B=B")

### BM12A Beamline Koyo PLC Modbus

#<modbus.cmd


###############################################################################
# Set shell prompt (otherwise it is left at mv167 or mv162) 
shellPromptSet "iocvxWorks> "
iocLogDisable=0
iocInit

### Startup State Notation Language (SNL) programs
# NOTE: Command line limited to 128 characters

#seq &kohzuCtl, "P=12idc:, M_THETA=m9, M_Y=m10, M_Z=m11, GEOM=2, logfile=kohzuCtl.log"
### Example of specifying offset limits
##taskDelay(300)
##dbpf 12idc:kohzu_yOffsetAO.DRVH 17.51
##dbpf 12idc:kohzu_yOffsetAO.DRVL 17.49

#seq &hrCtl, "P=12idc:, N=1, M_PHI1=m9, M_PHI2=m10, logfile=hrCtl1.log"

# Keithley 2000 series DMM
# channels: 10, 20, or 22;  model: 2000 or 2700
#seq &Keithley2kDMM,("P=12idc:, Dmm=D1, channels=22, model=2700")
#seq &Keithley2kDMM,("P=12idc:, Dmm=D2, channels=10, model=2000")

# Bunch clock generator
#seq &getFillPat, "unit=12idc"

# X-ray Instrumentation Associates Huber Slit Controller
# supported by a SNL program written by Pete Jemian and modified (TMM) for use with the
# sscan record
#seq  &xia_slit, "name=hsc1, P=12idc:, HSC=hsc1:, S=12idc:asyn_6"

# Orientation-matrix
#seq &orient, "P=12idc:orient1:,PM=12idc:,mTTH=m13,mTH=m14,mCHI=m15,mPHI=m16"

# Io calculation
#seq &Io, "P=12idc:Io:,MONO=12idc:BraggEAO,VSC=12idc:scaler1"

# Start Femto amplifier sequence programs
#putenv "FBO=12idc:Unidig1Bo"
#seq &femto,"name=fem1,P=12idc:,H=fem01:,F=seq01:,G1=$(FBO)6,G2=$(FBO)7,G3=$(FBO)8,NO=$(FBO)10"

# Start PF4 filter sequence program
#        name = what user will call it
#        P    = prefix of database and sequencer
#        H    = hardware (i.e. pf4)
#        B    = bank indicator (i.e. A,B)
#        M    = Monochromatic-beam energy PV
#        B1   = Filter control bit 0 PV
#        B2   = Filter control bit 1 PV
#        B3   = Filter control bit 2 PV
#        B4   = Fitler control bit 3 PV
#putenv "BO=12idc:Unidig1Bo"
#seq &pf4,"name=pf1,P=12idc:,H=pf4:,B=A,M=12idc:BraggEAO,B1=$(BO)3,B2=$(BO)4,B3=$(BO)5,B4=$(BO)6"
#seq &pf4,"name=pf2,P=12idc:,H=pf4:,B=B,M=12idc:BraggEAO,B1=$(BO)7,B2=$(BO)8,B3=$(BO)9,B4=$(BO)10"

### Start up the autosave task and tell it what to do.
# The task is actually named "save_restore".

# test starting the save_restore task without loading any save sets
#create_monitor_set("dummy.req",0,"")

# Note that you can reload these sets after creating them: e.g., 
# reload_monitor_set("auto_settings.req",30,"P=12idc:")
#
# save positions every five seconds
create_monitor_set("auto_positions.req",5,"P=12idc:")
# save other things every thirty seconds
create_monitor_set("auto_settings.req",30,"P=12idc:")
# You can have a save set triggered by a PV, and specify the name of the file it will write to with a PV
#create_triggered_set(<request file>,<trigger PV>,<PV from which file name should be read>)
#create_triggered_set("trigSet.req","12idc:userStringCalc1.SVAL","P=12idc:,SAVENAMEPV=12idc:userStringCalc1.SVAL")

### Start the saveData task.  If you start this task, scan records mentioned
# in saveData.req will *always* write data files.  There is no programmable
# disable for this software.
saveData_Init("saveData.req", "P=12idc:")

# If memory allocated at beginning free it now
##free(mem)

dbcar(0,1)

# motorUtil (allstop & alldone)
motorUtilInit("12idc:")

dbl >autosave/pv.logs




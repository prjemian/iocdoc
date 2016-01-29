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
### doesn't work for tornado 2.2.2 ### ld < 12ida1.munch
ld(0,0,"12ida1.munch")
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
# etc. in the software we just loaded (12ida1.munch)
dbLoadDatabase("$(TOP)/dbd/ioc12ida1VX.dbd")
ioc12ida1VX_registerRecordDeviceDriver(pdbbase)

dbLoadTemplate("test.template")
dbLoadTemplate("test.substitutions")
dbLoadRecords("test.db","P=startup:,S=prj,DTYP=Asyn Scaler,FREQ=50000000,OUT=@asyn(mcaSIS3820/1 0)", startup)

dbLoadRecords("$(TOP)/12ida1App/Db/test.db","P=prj:,S=s,DTYP=Asyn Scaler,FREQ=50000000,OUT=@asyn(mcaSIS3820/1 0)")

# user-assignable ramp/tweak
#dbLoadRecords("$(STD)/stdApp/Db/ramp_tweak.db","P=12ida1:,Q=rt1")

### save_restore setup
# We presume a suitable initHook routine was compiled into 12ida1.munch.
# See also create_monitor_set(), after iocInit() .
< save_restore.cmd

# Industry Pack support
< industryPack.cmd

#?? IP serial support
#< ip_serial.cmd

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
dbLoadRecords("$(MOTOR)/db/motorUtil.db", "P=12ida1:")

### streamDevice example
#dbLoadRecords("$(TOP)/12ida1App/Db/streamExample.db","P=12ida1:,PORT=serial1")

### Insertion-device control
#dbLoadRecords("$(STD)/stdApp/Db/IDctrl.db","P=12ida1:,xx=02us")

### Scan-support software
# crate-resident scan.  This executes 1D, 2D, 3D, and 4D scans, and caches
# 1D data, but it doesn't store anything to disk.  (See 'saveData' below for that.)
dbLoadTemplate("standardScans.substitutions")
dbLoadRecords("$(SSCAN)/sscanApp/Db/saveData.db","P=12ida1:")

# A set of scan parameters for each positioner.  This is a convenience
# for the user.  It can contain an entry for each scannable thing in the
# crate.
dbLoadTemplate("scanParms.substitutions")

### Slits
#White beam
#dbLoadRecords("$(OPTICS)/opticsApp/Db/2slit.db","P=12ida1:,SLIT=WBSV,mXp=m1,mXn=m2")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/2slit.db","P=12ida1:,SLIT=WBSH,mXp=m4,mXn=m3")

#Mono beam
dbLoadRecords("$(OPTICS)/opticsApp/Db/2slit.db","P=12ida1:,SLIT=MBSV,mXp=m5,mXn=m6")
dbLoadRecords("$(OPTICS)/opticsApp/Db/2slit.db","P=12ida1:,SLIT=MBSH,mXp=m8,mXn=m7")

#Defining Slit
dbLoadRecords("$(OPTICS)/opticsApp/Db/2slit.db","P=12ida1:,SLIT=BDSV,mXp=m29,mXn=m30")
dbLoadRecords("$(OPTICS)/opticsApp/Db/2slit.db","P=12ida1:,SLIT=BDSH,mXp=m32,mXn=m31")


# X-ray Instrumentation Associates Huber Slit Controller
# supported by a customized version of the SNL program written by Pete Jemian
# (Uses asyn record loaded separately)
#dbLoadRecords("$(OPTICS)/opticsApp/Db/xia_slit.db", "P=12ida1:, HSC=hsc1:")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/xia_slit.db", "P=12ida1:, HSC=hsc2:")

### 2-post mirror
#dbLoadRecords("$(OPTICS)/opticsApp/Db/2postMirror.db","P=12ida1:,Q=M1,mDn=m8,mUp=m7,LENGTH=0.3")

### User filters
#dbLoadRecords("$(OPTICS)/opticsApp/Db/filterMotor.db","P=12ida1:,Q=fltr1:,MOTOR=m1,LOCK=fltr_1_2:")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/filterMotor.db","P=12ida1:,Q=fltr2:,MOTOR=m2,LOCK=fltr_1_2:")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/filterLock.db","P=12ida1:,Q=fltr2:,LOCK=fltr_1_2:,LOCK_PV=12ida1:DAC1_1.VAL")

### Optical tables (both 180rotation)
#tableRecordDebug=1
putenv "DIR=$(OPTICS)/opticsApp/Db"
str = malloc(300)
strcpy str, "P=12ida1:,Q=HMTable,T=HMtable,M0X=na,M0Y=m19,M1Y=m18,M2X=na,M2Y=m17,M2Z=na,GEOM=NEWPORT"
dbLoadRecords("$(DIR)/table.db",str)
strcpy str,"P=12ida1:,Q=VMTable,T=VMtable,M0X=na,M0Y=m26,M1Y=m24,M2X=na,M2Y=m25,M2Z=na,GEOM=NEWPORT"
dbLoadRecords("$(DIR)/table.db",str)

# Io calculation
#dbLoadRecords("$(OPTICS)/opticsApp/Db/Io.db","P=12ida1:Io:")

### Monochromator support ###
# Kohzu and PSL monochromators: Bragg and theta/Y/Z motors
# standard geometry (geometry 1)
#dbLoadRecords("$(OPTICS)/opticsApp/Db/kohzuSeq.db","P=12ida1:,M_THETA=m9,M_Y=m10,M_Z=m11,yOffLo=17.4999,yOffHi=17.5001")
# modified geometry (geometry 2)
#dbLoadRecords("$(OPTICS)/opticsApp/Db/kohzuSeq.db","P=12ida1:,M_THETA=m9,M_Y=m10,M_Z=m11,yOffLo=4,yOffHi=36")


dbLoadRecords("$(TOP)/12ida1App/Db/SB_DCM.db","P=12ida1:,MTH1=m9,MTH2=m11,MZ2=m14")

# Spherical grating monochromator
#dbLoadRecords("$(OPTICS)/opticsApp/Db/SGM.db","P=12ida1:,N=1,M_x=m7,M_rIn=m6,M_rOut=m8,M_g=m9")

# 4-bounce high-resolution monochromator
#dbLoadRecords("$(OPTICS)/opticsApp/Db/hrSeq.db","P=12ida1:,N=1,M_PHI1=m9,M_PHI2=m10")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/hrSeq.db","P=12ida1:,N=2,M_PHI1=m11,M_PHI2=m12")

### Orientation matrix, four-circle diffractometer (see seq program 'orient' below)
#dbLoadRecords("$(OPTICS)/opticsApp/Db/orient.db", "P=12ida1:,O=1,PREC=6")
#dbLoadTemplate("orient_xtals.substitutions")

# Coarse/Fine stage
#dbLoadRecords("$(OPTICS)/opticsApp/Db/CoarseFineMotor.db","P=12ida1:cf1:,PM=12ida1:,CM=m7,FM=m8")

# Load single element Canberra AIM MCA and ICB modules
#< canberra_1.cmd

# Load 13 element detector software
#< canberra_13.cmd

# Load 3 element detector software
#< canberra_3.cmd

### Stuff for user programming ###
dbLoadRecords("$(CALC)/calcApp/Db/userCalcs10.db","P=12ida1:")
dbLoadRecords("$(CALC)/calcApp/Db/userCalcOuts10.db","P=12ida1:")
dbLoadRecords("$(CALC)/calcApp/Db/userStringCalcs10.db","P=12ida1:")
aCalcArraySize=2000
dbLoadRecords("$(CALC)/calcApp/Db/userArrayCalcs10.db","P=12ida1:,N=2000")
dbLoadRecords("$(CALC)/calcApp/Db/userTransforms10.db","P=12ida1:")
dbLoadRecords("$(CALC)/calcApp/Db/userAve10.db","P=12ida1:")
# string sequence (sseq) records
dbLoadRecords("$(STD)/stdApp/Db/userStringSeqs10.db","P=12ida1:")
# 4-step measurement
#dbLoadRecords("$(STD)/stdApp/Db/4step.db", "P=12ida1:")
# interpolation
#dbLoadRecords("$(CALC)/calcApp/Db/interp.db", "P=12ida1:,N=2000")
# array test
#dbLoadRecords("$(CALC)/calcApp/Db/arrayTest.db", "P=12ida1:,N=2000")

# pvHistory (in-crate archive of up to three PV's)
#dbLoadRecords("$(STD)/stdApp/Db/pvHistory.db","P=12ida1:,N=1,MAXSAMPLES=1440")

# software timer
#dbLoadRecords("$(STD)/stdApp/Db/timer.db","P=12ida1:,N=1")

# Slow feedback
#dbLoadTemplate "pid_slow.substitutions"

# Miscellaneous PV's, such as burtResult
#dbLoadRecords("$(STD)/stdApp/Db/misc.db","P=12ida1:")
#dbLoadRecords("$(STD)/stdApp/Db/VXstats.db","P=12ida1:")
# vxStats
dbLoadTemplate("vxStats.substitutions")

### Queensgate piezo driver
#dbLoadRecords("$(IP)/ipApp/Db/pzt_3id.db","P=12ida1:")
#dbLoadRecords("$(IP)/ipApp/Db/pzt.db","P=12ida1:,PORT=")

### Queensgate Nano2k piezo controller
#dbLoadRecords("$(STD)/stdApp/Db/Nano2k.db","P=12ida1:,S=s1")



### Load database records for Femto amplifiers
#dbLoadRecords("$(STD)/stdApp/Db/femto.db","P=12ida1:,H=fem01:,F=seq01:")

### Load database records for dual PF4 filters
#dbLoadRecords("$(OPTICS)/opticsApp/Db/pf4common.db","P=12ida1:,H=pf4:,A=A,B=B")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/pf4bank.db","P=12ida1:,H=pf4:,B=A")
#dbLoadRecords("$(OPTICS)/opticsApp/Db/pf4bank.db","P=12ida1:,H=pf4:,B=B")

## modbus PLC stuff

<modbus.cmd

###############################################################################
# Set shell prompt (otherwise it is left at mv167 or mv162)
shellPromptSet "iocvxWorks> "
iocLogDisable=0
iocInit

### Startup State Notation Language (SNL) programs
# NOTE: Command line limited to 128 characters

#seq &kohzuCtl, "P=12ida1:, M_THETA=m9, M_Y=m10, M_Z=m11, GEOM=2, logfile=kohzuCtl.log"
### Example of specifying offset limits
##taskDelay(300)
##dbpf 12ida1:kohzu_yOffsetAO.DRVH 17.51
##dbpf 12ida1:kohzu_yOffsetAO.DRVL 17.49

#seq &hrCtl, "P=12ida1:, N=1, M_PHI1=m9, M_PHI2=m10, logfile=hrCtl1.log"

# Keithley 2000 series DMM
# channels: 10, 20, or 22;  model: 2000 or 2700
#seq &Keithley2kDMM,("P=12ida1:, Dmm=D1, channels=22, model=2700")
#seq &Keithley2kDMM,("P=12ida1:, Dmm=D2, channels=10, model=2000")

# Bunch clock generator
#seq &getFillPat, "unit=12ida1"

# X-ray Instrumentation Associates Huber Slit Controller
# supported by a SNL program written by Pete Jemian and modified (TMM) for use with the
# sscan record
#seq  &xia_slit, "name=hsc1, P=12ida1:, HSC=hsc1:, S=12ida1:asyn_6"



# Start Femto amplifier sequence programs
#putenv "FBO=12ida1:Unidig1Bo"
#seq &femto,"name=fem1,P=12ida1:,H=fem01:,F=seq01:,G1=$(FBO)6,G2=$(FBO)7,G3=$(FBO)8,NO=$(FBO)10"

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
#putenv "BO=12ida1:Unidig1Bo"
#seq &pf4,"name=pf1,P=12ida1:,H=pf4:,B=A,M=12ida1:BraggEAO,B1=$(BO)3,B2=$(BO)4,B3=$(BO)5,B4=$(BO)6"
#seq &pf4,"name=pf2,P=12ida1:,H=pf4:,B=B,M=12ida1:BraggEAO,B1=$(BO)7,B2=$(BO)8,B3=$(BO)9,B4=$(BO)10"

### Start up the autosave task and tell it what to do.
# The task is actually named "save_restore".

# test starting the save_restore task without loading any save sets
#create_monitor_set("dummy.req",0,"")

# Note that you can reload these sets after creating them: e.g., 
# reload_monitor_set("auto_settings.req",30,"P=12ida1:")
#
# save positions every five seconds
create_monitor_set("auto_positions.req",5,"P=12ida1:")
# save other things every thirty seconds
create_monitor_set("auto_settings.req",30,"P=12ida1:")
# You can have a save set triggered by a PV, and specify the name of the file it will write to with a PV
#create_triggered_set(<request file>,<trigger PV>,<PV from which file name should be read>)
#create_triggered_set("trigSet.req","12ida1:userStringCalc1.SVAL","P=12ida1:,SAVENAMEPV=12ida1:userStringCalc1.SVAL")

### Start the saveData task.  If you start this task, scan records mentioned
# in saveData.req will *always* write data files.  There is no programmable
# disable for this software.
saveData_Init("saveData.req", "P=12ida1:")

# If memory allocated at beginning free it now
##free(mem)

dbcar(0,1)

# motorUtil (allstop & alldone)
motorUtilInit("12ida1:")

# dbl

dbl >autosave/pv.log





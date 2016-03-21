## Connections
drvAsynIPPortConfigure("CTSRC09", "6.7.8.9:7009", 0, 0, 0)

#
## Port 9 - IA X-Sel Motor Controller
asynOctetSetInputEos("CTSRC09", -1, "\r\n")
asynOctetSetOutputEos("CTSRC09", -1, "\r\n")
#
## Port Asyn records
dbLoadRecords("$(ASYN)/db/asynRecord.db","P=495idc:,R=port09,PORT=CTSRC09,ADDR=0,OMAX=0,IMAX=0")

# IAI X-Sel driver setup
#   (1) controllers
iocshCmd "drvIaXselAsynSetup(1)"

# This delay is required to avoid interrupt-level exceptions
iocshCmd "epicsThreadSleep(1.0)"

# IAI X-Sel driver config
#   (1) Controller number (begins/w 0)
#   (2) Asyn interface port name
#   (3) Asyn motor port name
#   (4) Asyn addr (GPIB only)
#   (5) Number of axes
#   (6) Poll time in msec
#   (7) Comm delay in msec
iocshCmd "drvIaXselAsynConfig(0,IAIF,CTSRC09,0,4,500,100)"

# Asyn-based Motor Record support
#   (1) Asyn port
#   (2) Driver name
#   (3) Controller index
#   (4) Max. number of axes
drvAsynMotorConfigure("IA1","motorIaXsel",0,4)

## motor records in motor.substitutions in the st.cmd file

## IAI controls
dbLoadRecords("$(TOP)/495idcApp/Db/iai_controls.db","P=495idc:,R=IAI:,PORT=IAIF")

## IAI Detector
dbLoadRecords("$(TOP)/495idcApp/Db/detBase.db","P=495idc:,H=base:")
dbLoadRecords("$(TOP)/495idcApp/Db/detRobot.db","P=495idc:,H=robot:")

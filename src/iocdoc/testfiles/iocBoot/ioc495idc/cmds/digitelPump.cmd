## Connections
drvAsynIPPortConfigure("CTSRC01", "6.7.8.9:7001", 0, 0, 0)
#
## Port 1 - GVMPC - Gamma Vaccum Digitel Multiple Pump Control
asynOctetSetInputEos("CTSRC01", -1, "\r")
asynOctetSetOutputEos("CTSRC01", -1, "\r")
dbLoadRecords("$(VAC)/vacApp/Db/digitelPump.db","P=495idc:,PUMP=IP01,PORT=CTSRC01,ADDR=5,DEV=MPC,STN=1")
dbLoadRecords("$(VAC)/vacApp/Db/digitelPump.db","P=495idc:,PUMP=IP02,PORT=CTSRC01,ADDR=5,DEV=MPC,STN=2")

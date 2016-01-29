
#Cyclades terminal server ports configuration

# cyberstar x2000 detector  9600 N18N
#drvAsynIPPortConfigure("TS01", "164.54.111.17:7001", 0, 0, 0)
#asynOctetSetInputEos("TS01", -1, "\n")
#asynOctetSetOutputEos("TS01", -1, "\n")

# cyberstar x2000 detector  9600 N18N
#drvAsynIPPortConfigure("TS02", "164.54.111.17:7002", 0, 0, 0)
#asynOctetSetInputEos("TS02", -1, "\n")
#asynOctetSetOutputEos("TS02", -1, "\n")

# cyberstar x2000 detector  9600 N18N
#drvAsynIPPortConfigure("TS03", "164.54.111.17:7003", 0, 0, 0)
#asynOctetSetInputEos("TS03", -1, "\n")
#asynOctetSetOutputEos("TS03", -1, "\n")

# PicoMotor 19200 N18N
#asynOctetSetInputEos("TS04", -1, ">")
#asynOctetSetOutputEos("TS04", -1, "\r")

# Starrett Indicator 9600 N18N
#drvAsynIPPortConfigure("TS04", "164.54.111.17:7004", 0, 0, 0)
#asynOctetSetInputEos("TS04", -1, "\r")
#asynOctetSetOutputEos("TS04", -1, "\r")

# Starrett Indicator 9600 N18N
#drvAsynIPPortConfigure("TS05", "164.54.111.17:7005", 0, 0, 0)
#asynOctetSetInputEos("TS05", -1, "\r")
#asynOctetSetOutputEos("TS05", -1, "\r")

# Starrett Indicator 9600 N18N
#drvAsynIPPortConfigure("TS06", "164.54.111.17:7006", 0, 0, 0)
#asynOctetSetInputEos("TS06", -1, "\r")
#asynOctetSetOutputEos("TS06", -1, "\r")

#drvAsynIPPortConfigure("TS07", "164.54.111.17:7007", 0, 0, 0)
#asynOctetSetInputEos("TS07", -1, "\r")
#asynOctetSetOutputEos("TS07", -1, "\r")

#drvAsynIPPortConfigure("TS08", "164.54.111.17:7008", 0, 0, 0)
#asynOctetSetInputEos("TS08", -1, "\r")
#asynOctetSetOutputEos("TS08", -1, "\r")

#drvAsynIPPortConfigure("TS09", "164.54.111.17:7009", 0, 0, 0)
#asynOctetSetInputEos("TS09", -1, "\r")
#asynOctetSetOutputEos("TS09", -1, "\r")

#drvAsynIPPortConfigure("TS10", "164.54.111.17:7010", 0, 0, 0)
#asynOctetSetInputEos("TS10", -1, "\r")
#asynOctetSetOutputEos("TS10", -1, "\r")

#drvAsynIPPortConfigure("TS11", "164.54.111.17:7011", 0, 0, 0)
#asynOctetSetInputEos("TS11", -1, "\r")
#asynOctetSetOutputEos("TS11", -1, "\r")

#drvAsynIPPortConfigure("TS12", "164.54.111.17:7012", 0, 0, 0)
#asynOctetSetInputEos("TS12", -1, "\r")
#asynOctetSetOutputEos("TS12", -1, "\r")

#drvAsynIPPortConfigure("TS13", "164.54.111.17:7013", 0, 0, 0)
#asynOctetSetInputEos("TS13", -1, "\r")
#asynOctetSetOutputEos("TS13", -1, "\r")

#drvAsynIPPortConfigure("TS14", "164.54.111.17:7014", 0, 0, 0)
#asynOctetSetInputEos("TS14", -1, "\r")
#asynOctetSetOutputEos("TS14", -1, "\r")

#drvAsynIPPortConfigure("TS15", "164.54.111.17:7015", 0, 0, 0)
#asynOctetSetInputEos("TS15", -1, "\r")
#asynOctetSetOutputEos("TS15", -1, "\r")

#drvAsynIPPortConfigure("TS16", "164.54.111.17:7016", 0, 0, 0)
#asynOctetSetInputEos("TS16", -1, "\r")
#asynOctetSetOutputEos("TS16", -1, "\r")

#Serial Over IP StarTech Type device
drvAsynIPPortConfigure("TS01", "164.54.122.31:4098", 0, 0, 0)
asynOctetSetInputEos("TS01", -1, "\r")
asynOctetSetOutputEos("TS01", -1, "\r")

drvAsynIPPortConfigure("TS02", "164.54.122.31:4097", 0, 0, 0)
asynOctetSetInputEos("TS02", -1, "\r")
asynOctetSetOutputEos("TS02", -1, "\r")

drvAsynIPPortConfigure("TS03", "164.54.122.31:4096", 0, 0, 0)
asynOctetSetInputEos("TS03", -1, "\r")
asynOctetSetOutputEos("TS03", -1, "\r")

drvAsynIPPortConfigure("TS04", "164.54.122.44:4097", 0, 0, 0)
asynOctetSetInputEos("TS04", -1, "\r")
asynOctetSetOutputEos("TS04", -1, "\r")


#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts01,PORT=TS01,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts02,PORT=TS02,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts03,PORT=TS03,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts04,PORT=TS04,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts05,PORT=TS05,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts06,PORT=TS06,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts07,PORT=TS07,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts08,PORT=TS08,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts09,PORT=TS09,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts10,PORT=TS10,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts11,PORT=TS11,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts12,PORT=TS12,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts13,PORT=TS13,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts14,PORT=TS14,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts15,PORT=TS15,ADDR=0,OMAX=256,IMAX=256")
#dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts16,PORT=TS16,ADDR=0,OMAX=256,IMAX=256")

dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts01,PORT=TS01,ADDR=0,OMAX=256,IMAX=256")
dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts02,PORT=TS02,ADDR=0,OMAX=256,IMAX=256")
dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts03,PORT=TS03,ADDR=0,OMAX=256,IMAX=256")
dbLoadRecords("$(ASYN)/db/asynRecord.db","P=12ida1:,R=ts04,PORT=TS04,ADDR=0,OMAX=256,IMAX=256")

dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP1,PORT=TS01,ADDR=0,DEV=D500,STN=2")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP2,PORT=TS02,ADDR=0,DEV=D500,STN=2")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP3,PORT=TS03,ADDR=0,DEV=D500,STN=2")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP4,PORT=TS04,ADDR=0,DEV=D500,STN=2")


#devices support

#PMNC87xxSetup(1,4,10)
#PMNC87xxConfig(0,"TS04")



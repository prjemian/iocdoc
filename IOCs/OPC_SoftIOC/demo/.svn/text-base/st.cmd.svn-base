dbLoadDatabase("../dbd/iocShell.dbd",0,0)
iocShell_registerRecordDeviceDriver(pdbbase)
# registerRecordDeviceDriver(pdbbase)  <= old command, won't work with epics base 3.14.6 and higher!!!
epicsEnvSet(IOCSH_PS1,"TrainingIoc> ")
opcSetServer("localhost","MMIOPC.Simulator")
opcSetGroup("myGroup3seconds","3000")                     # very slow, scanning every 3 seconds
#dbLoadRecords("./cceTest.db")

dbLoadRecords("./EpicsDemo.db")

opcSetGroup("myGroup6seconds","6000")                     # very slow, scanning every 6 seconds
#dbLoadRecords("./DemoRecord2.db")

dbLoadRecords ("./alarmTest.db","name=A,sec=1,max=181,high=60,hihi=120,hopr=200")
dbLoadRecords ("./alarmTest.db","name=B,sec=.5,max=13,high=7,hihi=11,hopr=20")
dbLoadRecords ("./alarmTest.db","name=C,sec=.1,max=1777,high=500,hihi=1200,hopr=2000")

dbLoadRecords("./TrainingOnCall.db")

dbLoadRecords("./Ctrl_PID.vdb")

dbLoadRecords ("ioc_common.db", "APPL=TrainIoc")

#dbLoadRecords ("./qxbpm.db", "P=como:")

iocInit()


dbpf TrainIoc:valid,"0"

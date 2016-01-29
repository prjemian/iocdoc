
# BEGIN serial.cmd ------------------------------------------------------------

# Initialize Octal UART stuff
# tyGSOctalDrv(int maxModules)
tyGSOctalDrv(2)

# tyGSOctalModuleInit(char *name, char *type, int intVec, int carrier, int slot)
# name    - name by which you want to refer to this IndustryPack module
# type    - one of "232", "422", "485" -- the serial hardware standard the module implements
# intVec  - interrupt vector 
# carrier - number of IP carrier (Carriers are numbered in the order in which they were
#           defined in ipacAddXYZ() calls.)
# slot    - location of module on carrier -- 0..3 for slot A..slot D
tyGSOctalModuleInit("UART_0", "232", 0x80, 0, 0)
tyGSOctalModuleInit("UART_1", "232", 0x81, 0, 1)

# int tyGSAsynInit(char *port, char *moduleName, int channel, int baud,
# char parity, int sbits, int dbits, char handshake, 
# char *inputEos, char *outputEos)
tyGSAsynInit("serial1",  "UART_0", 0, 9600,'N',1,8,'N',"\r","\r")  /* MPC1 */
tyGSAsynInit("serial2",  "UART_0", 1, 9600,'N',1,8,'N',"\r","\r")  /* MPC2*/
tyGSAsynInit("serial3",  "UART_0", 2, 9600,'N',1,8,'N',"\r","\r")  /* MPC3 */
tyGSAsynInit("serial4",  "UART_0", 3, 9600,'N',1,8,'N',"\r","\r")  /* MPC4*/
tyGSAsynInit("serial5",  "UART_0", 4, 9600,'N',1,8,'N',"\r","\r")  /* MPC5 */
tyGSAsynInit("serial6",  "UART_0", 5, 9600,'N',1,8,'N',"\r","\r") /*MPC6 */
tyGSAsynInit("serial7",  "UART_0", 6, 9600,'N',2,7,'N',"\r\n","\r\n")  /* GP307-1 */
tyGSAsynInit("serial8",  "UART_0", 7, 9600,'N',2,7,'N',"\r\n","\r\n")      /* GP307-2 */

#tyGSAsynInit("serial9",  "UART_1", 0, 9600,'N',2,8,'N',"\r","\r")  /* SRS570 */
#tyGSAsynInit("serial10",  "UART_1", 1,19200,'N',1,8,'N',"\r\n","\r")  /* Keithley 2000 */
tyGSAsynInit("serial9",  "UART_1", 0, 9600,'N',2,7,'N',"\r\n","\r\n")  /* GP307-3 */
tyGSAsynInit("serial10",  "UART_1", 1, 9600,'N',2,7,'N',"\r\n","\r\n")      /* GP307-4 */


tyGSAsynInit("serial11",  "UART_1", 2, 9600,'E',2,7,'N',"\r","")  /* Heidenhai ND261/281 */
tyGSAsynInit("serial12",  "UART_1", 3, 9600,'N',1,8,'N',"\n","\n")  /* MPC */
tyGSAsynInit("serial13",  "UART_1", 4,19200,'N',1,8,'N',"\r","\r")  /* ACS MCB-4B */
tyGSAsynInit("serial14",  "UART_1", 5, 9600,'N',1,8,'N',"\r\n","\r") /* XIA slit */
tyGSAsynInit("serial15",  "UART_1", 6,38400,'N',1,8,'N',"\r","\r")  /* Newport MM4000 */
tyGSAsynInit("serial16",  "UART_1", 7,19200,'N',1,8,'N',"","")      /* Love controllers */
# Newport MM4000 driver setup parameters:
#     (1) maximum # of controllers,
#     (2) motor task polling rate (min=1Hz, max=60Hz)
#MM4000Setup(1, 10)

# Newport MM4000 driver configuration parameters:
#     (1) controller
#     (2) asyn port name (e.g. serial1 or gpib1)
#     (3) GPIB address (0 for serial)
#MM4000Config(0, "serial7", 0)

# Newport PM500 driver setup parameters:
#     (1) maximum number of controllers in system
#     (2) motor task polling rate (min=1Hz,max=60Hz)
#PM500Setup(1, 10)

# Newport PM500 configuration parameters:
#     (1) controller
#     (2) asyn port name (e.g. serial1 or gpib1)
#PM500Config(0, "serial3")

# McClennan PM304 driver setup parameters:
#     (1) maximum number of controllers in system
#     (2) motor task polling rate (min=1Hz, max=60Hz)
#PM304Setup(1, 10)

# McClennan PM304 driver configuration parameters:
#     (1) controller being configured
#     (2) MPF serial server name (string)
#     (3) Number of axes on this controller
#PM304Config(0, "serial4", 1)

# ACS MCB-4B driver setup parameters:
#     (1) maximum number of controllers in system
#     (2) motor task polling rate (min=1Hz, max=60Hz)
#MCB4BSetup(1, 10)

# ACS MCB-4B driver configuration parameters:
#     (1) controller being configured
#     (2) asyn port name (string)
#MCB4BConfig(0, "serial5")

##### Pico Motors (Ernest Williams MHATT-CAT)
##### Motors (see picMot.substitutions in same directory as this file) ####
#dbLoadTemplate("picMot.substitutions")

# Load asynRecord records on all ports
dbLoadTemplate("asynRecord.substitutions")

# send impromptu message to serial device, parse reply
# (was serial_OI_block)
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=1,PORT=serial1,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=2,PORT=serial2,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=3,PORT=serial3,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=4,PORT=serial4,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=5,PORT=serial5,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=6,PORT=serial6,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=7,PORT=serial7,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=8,PORT=serial8,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=9,PORT=serial9,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=10,PORT=serial10,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=11,PORT=serial11,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=12,PORT=serial12,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=13,PORT=serial13,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=14,PORT=serial14,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=15,PORT=serial15,ADDR=0,OMAX=100,IMAX=100")
dbLoadRecords("$(IP)/ipApp/Db/deviceCmdReply.db","P=12ida1:,N=16,PORT=serial16,ADDR=0,OMAX=100,IMAX=100")


# Stanford Research Systems SR570 Current Preamplifier
#dbLoadRecords("$(IP)/ipApp/Db/SR570.db", "P=12ida1:,A=A1,PORT=serial1")

# Lakeshore DRC-93CA Temperature Controller
#dbLoadRecords("$(IP)/ipApp/Db/LakeShoreDRC-93CA.db", "P=12ida1:,Q=TC1,PORT=serial4")

# Huber DMC9200 DC Motor Controller
#dbLoadRecords("$(IP)/ipApp/Db/HuberDMC9200.db", "P=12ida1:,Q=DMC1:,PORT=serial5")

# Oriel 18011 Encoder Mike
#dbLoadRecords("$(IP)/ipApp/Db/eMike.db", "P=12ida1:,M=em1,PORT=serial3")

# Keithley 2000 DMM
#dbLoadRecords("$(IP)/ipApp/Db/Keithley2kDMM_mf.db","P=12ida1:,Dmm=D1,PORT=serial1")

# Oxford Cyberstar X1000 Scintillation detector and pulse processing unit
#dbLoadRecords("$(IP)/ipApp/Db/Oxford_X1k.db","P=12ida1:,S=s1,PORT=serial4")

# Oxford ILM202 Cryogen Level Meter (Serial)
#dbLoadRecords("$(IP)/ipApp/Db/Oxford_ILM202.db","P=12ida1:,S=s1,PORT=serial5")

# Elcomat autocollimator
#dbLoadRecords("$(IP)/ipApp/Db/Elcomat.db", "P=12ida1:,PORT=serial8")

# Eurotherm temp controller
#dbLoadRecords("$(IP)/ipApp/Db/Eurotherm.db","P=12ida1:,PORT=serial7")

# MKS vacuum gauges
#dbLoadRecords("$(IP)/ipApp/Db/MKS.db","P=12ida1:,PORT=serial2,CC1=cc1,CC2=cc3,PR1=pr1,PR2=pr3")

# PI Digitel 500/1500 pump
#dbLoadRecords("$(IP)/ipApp/Db/Digitel.db","12ida1:,PUMP=ip1,PORT=serial3")


# PI MPC ion pump
#dbLoadRecords("$(IP)/ipApp/Db/MPC.db","P=12ida1:,PUMP=ip2,PORT=serial4,PA=0,PN=1")

dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP1,PORT=serial1,ADDR=5,DEV=MPC,STN=1")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP2,PORT=serial1,ADDR=5,DEV=MPC,STN=2")

dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP3,PORT=serial2,ADDR=5,DEV=MPC,STN=1")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP4,PORT=serial2,ADDR=5,DEV=MPC,STN=2")

dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP5,PORT=serial3,ADDR=5,DEV=MPC,STN=1")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP6,PORT=serial3,ADDR=5,DEV=MPC,STN=2")

dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP7,PORT=serial4,ADDR=5,DEV=MPC,STN=1")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP8,PORT=serial4,ADDR=5,DEV=MPC,STN=2")

dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP9,PORT=serial5,ADDR=5,DEV=MPC,STN=1")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP10,PORT=serial5,ADDR=5,DEV=MPC,STN=2")

dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP11,PORT=serial6,ADDR=5,DEV=MPC,STN=1")
dbLoadRecords("$(VAC)/db/digitelPump.db","P=12ida1:,PUMP=IP12,PORT=serial6,ADDR=5,DEV=MPC,STN=2")



#GP 307 Vacuum Gauge
#dbLoadRecords("$(VAC)/db/vs.db", "P=12ida1:,GAUGE=VS1,PORT=serial7,ADDR=0,DEV=GP307,STN=0")


# PI MPC TSP (titanium sublimation pump)
#dbLoadRecords("$(IP)/ipApp/Db/TSP.db","P=12ida1:,TSP=tsp1,PORT=serial4,PA=0")

# Heidenhain ND261 encoder (for PSL monochromator)
#dbLoadRecords("$(TOP)/12ida1App/Db/heidND261.db", "P=12ida1:,PORT=serial11,DESC=Mono_Encoder")

# Love Controllers
#devLoveDebug=1
#loveServerDebug=1
##dbLoadRecords("$(IP)/ipApp/Db/love.db", "P=12ida1:,Q=Love_0,C=0,PORT=PORT2,ADDR=1")

# END serial.cmd --------------------------------------------------------------

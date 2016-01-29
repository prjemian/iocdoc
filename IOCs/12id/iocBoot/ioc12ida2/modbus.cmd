#modbus.cmd


# Use the following commands for TCP/IP
#drvAsynIPPortConfigure(const char *portName, 
#                       const char *hostInfo,
#                       unsigned int priority, 
#                       int noAutoConnect,
#                       int noProcessEos);
drvAsynIPPortConfigure("440","164.54.122.122:502",0,1,1)

#modbusInterposeConfig(const char *portName, 
#                      int slaveAddress, 
#                      modbusLinkType linkType,
#                      int timeoutMsec)
modbusInterposeConfig("440",0,0,5000)


#       numbers (no leading zero) or hex numbers can also be used.

# The 440 has bit access to the Xn inputs at Modbus offset 4000 (octal)
# Read 40 bits (X0-X47).  Function code=2. ## 50 Octal
drvModbusAsynConfigure("K1_Xn_Bit",      "440", 2,  04000, 050,    0,  100, "Koyo")


# The 440 has bit access to the Yn outputs at Modbus offset 4000 (octal)
# Read 32 bits (Y0-Y37).  Function code=1. ## 40 octal
drvModbusAsynConfigure("K1_Yn_In_Bit",   "440", 1,  04000, 040,    0,  100, "Koyo")

# The 440 has bit access to the Yn outputs at Modbus offset 4000 (octal)
# Write 32 bits (Y0-Y37).  Function code=5.
drvModbusAsynConfigure("K1_Yn_Out_Bit",  "440", 5,  04000, 040,    0,  1, "Koyo")


# The 440 has bit access to the Cn bits at Modbus offset 6000 (octal)
# Access 1024 bits (C0-C1777) as inputs.  Function code=1.
drvModbusAsynConfigure("K1_Cn_In_Bit",   "440", 1,  06000, 02000,   0,  100, "Koyo")



# Enable ASYN_TRACEIO_HEX on octet server
asynSetTraceIOMask("440",0,4)
# Enable ASYN_TRACE_ERROR and ASYN_TRACEIO_DRIVER on octet server
#asynSetTraceMask("440",0,9)

# Enable ASYN_TRACEIO_HEX on modbus server
#asynSetTraceIOMask("K1_Yn_In_Bit",0,4)
# Enable all debugging on modbus server
#asynSetTraceMask("K1_Yn_In_Bit",0,255)
# Dump up to 512 bytes in asynTrace
asynSetTraceIOTruncateSize("K1_Yn_In_Bit",0,512)


dbLoadTemplate("modbus.substitutions")



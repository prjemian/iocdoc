TOP=../..

include $(TOP)/configure/CONFIG

ca_DIR           = $(EPICS_BASE_LIB)
Com_DIR          = $(EPICS_BASE_LIB)
gdd_DIR          = $(EPICS_BASE_LIB)
opcDevIoc_DIR	= $(TOP)\\lib\\win32-x86

#=============================
# opc-device support library

DBDINSTALL += opc.dbd
SHARED_LIBRARIES = NO
LIBOBJS += drvOpc devOpc opcConsoleCmd Opc Creator Server Group Item errDbg
LIBRARY_IOC = opcDevIoc
opcDevIoc_OBJS = $(LIBOBJS)

USR_CXXFLAGS = /D "_WIN32_DCOM"
USR_INCLUDES = -I "D:\Programme\Softing\OPCToolbox\include" -I "D:\Programme\Softing\OPCToolbox\opc"
USR_LDFLAGS += /libpath:"D:\Programme\Softing\OPCToolbox\lib\vc6"

#=============================
# iocShell with opc support

PROD_IOC = iocShell

# <name>.dbd will be created from <name>Include.dbd
DBD += iocShell.dbd
#DBD += base.dbd opc.dbd


# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
iocShell_SRCS += iocShell_registerRecordDeviceDriver.cpp
iocShell_SRCS_DEFAULT += iocShellMain.cpp
iocShell_SRCS_vxWorks += -nil-

#The following adds support from base/src/vxWorks
iocShell_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary


# Use win32 object libs for registered support
iocShell_LIBS_win32 += recIocObj
iocShell_LIBS_win32 += softDevIocObj
iocShell_LIBS_win32 += testDevIocObj
iocShell_LIBS_win32 += opcDevIocObj
iocShell_LIBS_DEFAULT += recIoc
iocShell_LIBS_DEFAULT += softDevIoc
iocShell_LIBS_DEFAULT += testDevIoc
iocShell_LIBS_DEFAULT += opcDevIoc

iocShell_LIBS += iocsh
iocShell_LIBS += miscIoc
iocShell_LIBS += rsrvIoc
iocShell_LIBS += dbtoolsIoc
iocShell_LIBS += asIoc
iocShell_LIBS += dbIoc
iocShell_LIBS += registryIoc
iocShell_LIBS += dbStaticIoc
iocShell_LIBS += ca
iocShell_LIBS += opcDevIoc
iocShell_LIBS += Com
iocShell_LIBS += gdd

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE


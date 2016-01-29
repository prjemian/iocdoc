TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

# For Kate Feng's implementation of devScaler.c, which uses Till
# Straumann's basicIoOps.h to bridge any mismatch between endianness
# of Joerger scaler hardware and endianness of processor.
#USR_CFLAGS += -DHAS_IOOPS_H

#==================================================
# build a support library that some other application can use

#LIBRARY_IOC += 12idbSupport

# 12idbRecord.h will be created from 12idbRecord.dbd
#DBDINC += 12idbRecord
# install support-library .dbd into <top>/dbd
#DBD += 12idbSupport.dbd

# The following are compiled and added to the Support library
#12idbSupport_SRCS += 12idbRecord.c

#12idbSupport_LIBS += $(EPICS_BASE_IOC_LIBS)

#=============================
# build an ioc application

PROD_IOC_DEFAULT = 12idb
PROD_IOC_solaris = 12idb

# <name>.dbd will be created from <name>Include.dbd
ifeq ($(OS_CLASS), WIN32)
DBD  += ioc12idbWin32.dbd
else
ifeq ($(EPICS_HOST_ARCH), cygwin-x86)
DBD  += ioc12idbCygwin.dbd
else
DBD  += ioc12idb.dbd
DBD  += ioc12idbVX.dbd
DBD  += ioc12idbLinux.dbd
DBD  += ioc12idb_solaris.dbd
endif
endif

# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
12idb_SRCS_DEFAULT  += ioc12idb_registerRecordDeviceDriver.cpp          12idbMain.cpp
12idb_SRCS_vxWorks  += ioc12idbVX_registerRecordDeviceDriver.cpp
12idb_SRCS_Linux    += ioc12idbLinux_registerRecordDeviceDriver.cpp     12idbMain.cpp
12idb_SRCS_WIN32    += ioc12idbWin32_registerRecordDeviceDriver.cpp     12idbMain.cpp
12idb_SRCS_cygwin32 += ioc12idbCygwin_registerRecordDeviceDriver.cpp    12idbMain.cpp
12idb_SRCS_solaris  += ioc12idb_solaris_registerRecordDeviceDriver.cppa 12idbMain.cpp
12idb_SRCS_vxWorks  += -nil-

#12idb_Common_LIBS += 12idbSupport
12idb_Common_LIBS += vac modbus
12idb_Common_LIBS += mca
12idb_Common_LIBS += calc
12idb_Common_LIBS += busy
12idb_Common_LIBS += sscan
12idb_Common_LIBS += autosave
12idb_Common_LIBS += optics
12idb_Common_LIBS += vme
12idb_Common_LIBS += std
12idb_Common_LIBS += ip
#12idb_Common_LIBS += brukerCCD
#12idb_Common_LIBS += marCCD
#12idb_Common_LIBS += roperCCD

#12idb_Common_LIBS += Acs Faulhaber Ims Mclennan Micos MicroMo NewFocus
#12idb_Common_LIBS += Newport PI Parker
12idb_Common_LIBS += softMotor motorSimSupport motor

12idb_Common_LIBS += asyn
12idb_Common_LIBS += stream streamSynApps
12idb_Common_LIBS += seqDev seq pv
12idb_Common_LIBS += $(EPICS_BASE_IOC_LIBS)

#12idb_vxWorks_LIBS += allenBradley
12idb_vxWorks_LIBS += mcaSIS
#12idb_vxWorks_LIBS += mcaCanberra
12idb_vxWorks_LIBS += ip330
12idb_vxWorks_LIBS += ipUnidig
12idb_vxWorks_LIBS += dac128V
#12idb_vxWorks_LIBS += quadEM
#12idb_vxWorks_LIBS += camac devCamac
#12idb_vxWorks_LIBS += dxp handel
#12idb_vxWorks_LIBS += love
12idb_vxWorks_LIBS += vxStats
12idb_vxWorks_LIBS += TyGSOctal Ipac
12idb_vxWorks_LIBS += oms 
#12idb_vxWorks_LIBS +=DeltaTau

#The following adds support from base/src/vxWorks
12idb_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

#12idb_Linux_LIBS  += dxp handel
# If libnet IS installed on your HOST Linux system;
# uncomment the following line.
ifeq ($(LINUX_NET_INSTALLED), YES)
12idb_Linux_LIBS  += mcaCanberra
endif

12idb_cygwin_LIBS += dxp handel

12idb_WIN32_LIBS += dxp handel

#12idb_solaris_LIBS += genSub
#12idb_solaris_LIBS += mca
12idb_solaris_LIBS += calc
12idb_solaris_LIBS += busy
12idb_solaris_LIBS += sscan
12idb_solaris_LIBS += autosave
12idb_solaris_LIBS += optics
#12idb_solaris_LIBS += vme
12idb_solaris_LIBS += std
#12idb_solaris_LIBS += ip
#12idb_solaris_LIBS += brukerCCD
#12idb_solaris_LIBS += marCCD
#12idb_solaris_LIBS += roperCCD
12idb_solaris_LIBS += motor softMotor motorSimSupport
12idb_solaris_LIBS += asyn
12idb_solaris_LIBS += seqDev seq pv
12idb_solaris_LIBS += $(EPICS_BASE_IOC_LIBS)


12idb_LIBS_DEFAULT = $(12idb_Common_LIBS)
12idb_LIBS_vxWorks = $(12idb_vxWorks_LIBS) $(12idb_Common_LIBS)
12idb_LIBS_Linux   = $(12idb_Linux_LIBS)   $(12idb_Common_LIBS)
12idb_LIBS_solaris = $(12idb_solaris_LIBS)
12idb_LIBS_cygwin32 = $(12idb_cygwin_LIBS) $(12idb_Common_LIBS)
12idb_LIBS_WIN32    = $(12idb_WIN32_LIBS)  $(12idb_Common_LIBS)

# If the host has libnet and libpcap for mca/Canberra support
# uncomment the following line.
ifeq ($(LINUX_NET_INSTALLED), YES)
12idb_SYS_LIBS_Linux += net pcap
endif
# For USB support on Saturn
ifeq ($(LINUX_USB_INSTALLED), YES)
12idb_SYS_LIBS_Linux += usb
endif
12idb_SYS_LIBS_vxWorks += -nil-

# This is needed by dxp on cygwin and WIN32
12idb_SYS_LIBS_cygwin32 += DLPORTIO PlxApi setupapi
12idb_LIBS_WIN32        += DLPORTIO PlxApi
12idb_SYS_LIBS_WIN32    += setupapi
# This is needed by saveData and asyn VXI-11 on cygwin
12idb_SYS_LIBS_cygwin32 += rpc


#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

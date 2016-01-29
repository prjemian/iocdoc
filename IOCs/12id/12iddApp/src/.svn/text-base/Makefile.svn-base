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

#LIBRARY_IOC += 12iddSupport

# 12iddRecord.h will be created from 12iddRecord.dbd
#DBDINC += 12iddRecord
# install support-library .dbd into <top>/dbd
#DBD += 12iddSupport.dbd

# The following are compiled and added to the Support library
#12iddSupport_SRCS += 12iddRecord.c

#12iddSupport_LIBS += $(EPICS_BASE_IOC_LIBS)

#=============================
# build an ioc application

PROD_IOC_DEFAULT = 12idd
PROD_IOC_solaris = 12idd

# <name>.dbd will be created from <name>Include.dbd
ifeq ($(OS_CLASS), WIN32)
DBD  += ioc12iddWin32.dbd
else
ifeq ($(EPICS_HOST_ARCH), cygwin-x86)
DBD  += ioc12iddCygwin.dbd
else
DBD  += ioc12idd.dbd
DBD  += ioc12iddVX.dbd
DBD  += ioc12iddLinux.dbd
DBD  += ioc12idd_solaris.dbd
endif
endif

# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
12idd_SRCS_DEFAULT  += ioc12idd_registerRecordDeviceDriver.cpp          12iddMain.cpp
12idd_SRCS_vxWorks  += ioc12iddVX_registerRecordDeviceDriver.cpp
12idd_SRCS_Linux    += ioc12iddLinux_registerRecordDeviceDriver.cpp     12iddMain.cpp
12idd_SRCS_WIN32    += ioc12iddWin32_registerRecordDeviceDriver.cpp     12iddMain.cpp
12idd_SRCS_cygwin32 += ioc12iddCygwin_registerRecordDeviceDriver.cpp    12iddMain.cpp
12idd_SRCS_solaris  += ioc12idd_solaris_registerRecordDeviceDriver.cppa 12iddMain.cpp
12idd_SRCS_vxWorks  += -nil-

#12idd_Common_LIBS += 12iddSupport
12idd_Common_LIBS += vac modbus
12idd_Common_LIBS += mca
12idd_Common_LIBS += calc
12idd_Common_LIBS += busy
12idd_Common_LIBS += sscan
12idd_Common_LIBS += autosave
12idd_Common_LIBS += optics
12idd_Common_LIBS += vme
12idd_Common_LIBS += std
12idd_Common_LIBS += ip
#12idd_Common_LIBS += brukerCCD
#12idd_Common_LIBS += marCCD
#12idd_Common_LIBS += roperCCD

#12idd_Common_LIBS += Acs Faulhaber Ims Mclennan Micos MicroMo NewFocus
#12idd_Common_LIBS += Newport PI Parker
12idd_Common_LIBS += softMotor motorSimSupport motor

12idd_Common_LIBS += asyn
12idd_Common_LIBS += stream streamSynApps
12idd_Common_LIBS += seqDev seq pv
12idd_Common_LIBS += $(EPICS_BASE_IOC_LIBS)

#12idd_vxWorks_LIBS += allenBradley
12idd_vxWorks_LIBS += mcaSIS
#12idd_vxWorks_LIBS += mcaCanberra
12idd_vxWorks_LIBS += ip330
12idd_vxWorks_LIBS += ipUnidig
12idd_vxWorks_LIBS += dac128V
#12idd_vxWorks_LIBS += quadEM
#12idd_vxWorks_LIBS += camac devCamac
#12idd_vxWorks_LIBS += dxp handel
#12idd_vxWorks_LIBS += love
12idd_vxWorks_LIBS += vxStats
12idd_vxWorks_LIBS += TyGSOctal Ipac
12idd_vxWorks_LIBS += oms 
#12idd_vxWorks_LIBS +=DeltaTau

#The following adds support from base/src/vxWorks
12idd_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

#12idd_Linux_LIBS  += dxp handel
# If libnet IS installed on your HOST Linux system;
# uncomment the following line.
ifeq ($(LINUX_NET_INSTALLED), YES)
12idd_Linux_LIBS  += mcaCanberra
endif

12idd_cygwin_LIBS += dxp handel

12idd_WIN32_LIBS += dxp handel

#12idd_solaris_LIBS += genSub
#12idd_solaris_LIBS += mca
12idd_solaris_LIBS += calc
12idd_solaris_LIBS += busy
12idd_solaris_LIBS += sscan
12idd_solaris_LIBS += autosave
12idd_solaris_LIBS += optics
#12idd_solaris_LIBS += vme
12idd_solaris_LIBS += std
#12idd_solaris_LIBS += ip
#12idd_solaris_LIBS += brukerCCD
#12idd_solaris_LIBS += marCCD
#12idd_solaris_LIBS += roperCCD
12idd_solaris_LIBS += motor softMotor motorSimSupport
12idd_solaris_LIBS += asyn
12idd_solaris_LIBS += seqDev seq pv
12idd_solaris_LIBS += $(EPICS_BASE_IOC_LIBS)


12idd_LIBS_DEFAULT = $(12idd_Common_LIBS)
12idd_LIBS_vxWorks = $(12idd_vxWorks_LIBS) $(12idd_Common_LIBS)
12idd_LIBS_Linux   = $(12idd_Linux_LIBS)   $(12idd_Common_LIBS)
12idd_LIBS_solaris = $(12idd_solaris_LIBS)
12idd_LIBS_cygwin32 = $(12idd_cygwin_LIBS) $(12idd_Common_LIBS)
12idd_LIBS_WIN32    = $(12idd_WIN32_LIBS)  $(12idd_Common_LIBS)

# If the host has libnet and libpcap for mca/Canberra support
# uncomment the following line.
ifeq ($(LINUX_NET_INSTALLED), YES)
12idd_SYS_LIBS_Linux += net pcap
endif
# For USB support on Saturn
ifeq ($(LINUX_USB_INSTALLED), YES)
12idd_SYS_LIBS_Linux += usb
endif
12idd_SYS_LIBS_vxWorks += -nil-

# This is needed by dxp on cygwin and WIN32
12idd_SYS_LIBS_cygwin32 += DLPORTIO PlxApi setupapi
12idd_LIBS_WIN32        += DLPORTIO PlxApi
12idd_SYS_LIBS_WIN32    += setupapi
# This is needed by saveData and asyn VXI-11 on cygwin
12idd_SYS_LIBS_cygwin32 += rpc


#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

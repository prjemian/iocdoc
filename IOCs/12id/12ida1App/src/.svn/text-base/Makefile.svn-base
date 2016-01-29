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

#LIBRARY_IOC += 12ida1Support

# 12ida1Record.h will be created from 12ida1Record.dbd
#DBDINC += 12ida1Record
# install support-library .dbd into <top>/dbd
#DBD += 12ida1Support.dbd

# The following are compiled and added to the Support library
#12ida1Support_SRCS += 12ida1Record.c

#12ida1Support_LIBS += $(EPICS_BASE_IOC_LIBS)

#=============================
# build an ioc application

PROD_IOC_DEFAULT = 12ida1
PROD_IOC_solaris = 12ida1

# <name>.dbd will be created from <name>Include.dbd
ifeq ($(OS_CLASS), WIN32)
DBD  += ioc12ida1Win32.dbd
else
ifeq ($(EPICS_HOST_ARCH), cygwin-x86)
DBD  += ioc12ida1Cygwin.dbd
else
DBD  += ioc12ida1.dbd
DBD  += ioc12ida1VX.dbd
DBD  += ioc12ida1Linux.dbd
DBD  += ioc12ida1_solaris.dbd
endif
endif

# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
12ida1_SRCS_DEFAULT  += ioc12ida1_registerRecordDeviceDriver.cpp          12ida1Main.cpp
12ida1_SRCS_vxWorks  += ioc12ida1VX_registerRecordDeviceDriver.cpp
12ida1_SRCS_Linux    += ioc12ida1Linux_registerRecordDeviceDriver.cpp     12ida1Main.cpp
12ida1_SRCS_WIN32    += ioc12ida1Win32_registerRecordDeviceDriver.cpp     12ida1Main.cpp
12ida1_SRCS_cygwin32 += ioc12ida1Cygwin_registerRecordDeviceDriver.cpp    12ida1Main.cpp
12ida1_SRCS_solaris  += ioc12ida1_solaris_registerRecordDeviceDriver.cppa 12ida1Main.cpp
12ida1_SRCS_vxWorks  += -nil-

#12ida1_Common_LIBS += 12ida1Support
12ida1_Common_LIBS += vac modbus
12ida1_Common_LIBS += mca
12ida1_Common_LIBS += calc
12ida1_Common_LIBS += busy
12ida1_Common_LIBS += sscan
12ida1_Common_LIBS += autosave
12ida1_Common_LIBS += optics
12ida1_Common_LIBS += vme
12ida1_Common_LIBS += std
12ida1_Common_LIBS += ip
#12ida1_Common_LIBS += brukerCCD
#12ida1_Common_LIBS += marCCD
#12ida1_Common_LIBS += roperCCD

#12ida1_Common_LIBS += Acs Faulhaber Ims Mclennan Micos MicroMo NewFocus
#12ida1_Common_LIBS += Newport PI Parker
12ida1_Common_LIBS += softMotor motorSimSupport motor

12ida1_Common_LIBS += asyn
12ida1_Common_LIBS += stream streamSynApps
12ida1_Common_LIBS += seqDev seq pv
12ida1_Common_LIBS += $(EPICS_BASE_IOC_LIBS)

#12ida1_vxWorks_LIBS += allenBradley
12ida1_vxWorks_LIBS += mcaSIS
#12ida1_vxWorks_LIBS += mcaCanberra
12ida1_vxWorks_LIBS += ip330
12ida1_vxWorks_LIBS += ipUnidig
12ida1_vxWorks_LIBS += dac128V
#12ida1_vxWorks_LIBS += quadEM
#12ida1_vxWorks_LIBS += camac devCamac
#12ida1_vxWorks_LIBS += dxp handel
#12ida1_vxWorks_LIBS += love
12ida1_vxWorks_LIBS += vxStats
12ida1_vxWorks_LIBS += TyGSOctal Ipac
12ida1_vxWorks_LIBS += oms 
#12ida1_vxWorks_LIBS +=DeltaTau

#The following adds support from base/src/vxWorks
12ida1_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

#12ida1_Linux_LIBS  += dxp handel
# If libnet IS installed on your HOST Linux system;
# uncomment the following line.
ifeq ($(LINUX_NET_INSTALLED), YES)
12ida1_Linux_LIBS  += mcaCanberra
endif

12ida1_cygwin_LIBS += dxp handel

12ida1_WIN32_LIBS += dxp handel

#12ida1_solaris_LIBS += genSub
#12ida1_solaris_LIBS += mca
12ida1_solaris_LIBS += calc
12ida1_solaris_LIBS += busy
12ida1_solaris_LIBS += sscan
12ida1_solaris_LIBS += autosave
12ida1_solaris_LIBS += optics
#12ida1_solaris_LIBS += vme
12ida1_solaris_LIBS += std
#12ida1_solaris_LIBS += ip
#12ida1_solaris_LIBS += brukerCCD
#12ida1_solaris_LIBS += marCCD
#12ida1_solaris_LIBS += roperCCD
12ida1_solaris_LIBS += motor softMotor motorSimSupport
12ida1_solaris_LIBS += asyn
12ida1_solaris_LIBS += seqDev seq pv
12ida1_solaris_LIBS += $(EPICS_BASE_IOC_LIBS)


12ida1_LIBS_DEFAULT = $(12ida1_Common_LIBS)
12ida1_LIBS_vxWorks = $(12ida1_vxWorks_LIBS) $(12ida1_Common_LIBS)
12ida1_LIBS_Linux   = $(12ida1_Linux_LIBS)   $(12ida1_Common_LIBS)
12ida1_LIBS_solaris = $(12ida1_solaris_LIBS)
12ida1_LIBS_cygwin32 = $(12ida1_cygwin_LIBS) $(12ida1_Common_LIBS)
12ida1_LIBS_WIN32    = $(12ida1_WIN32_LIBS)  $(12ida1_Common_LIBS)

# If the host has libnet and libpcap for mca/Canberra support
# uncomment the following line.
ifeq ($(LINUX_NET_INSTALLED), YES)
12ida1_SYS_LIBS_Linux += net pcap
endif
# For USB support on Saturn
ifeq ($(LINUX_USB_INSTALLED), YES)
12ida1_SYS_LIBS_Linux += usb
endif
12ida1_SYS_LIBS_vxWorks += -nil-

# This is needed by dxp on cygwin and WIN32
12ida1_SYS_LIBS_cygwin32 += DLPORTIO PlxApi setupapi
12ida1_LIBS_WIN32        += DLPORTIO PlxApi
12ida1_SYS_LIBS_WIN32    += setupapi
# This is needed by saveData and asyn VXI-11 on cygwin
12ida1_SYS_LIBS_cygwin32 += rpc


#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

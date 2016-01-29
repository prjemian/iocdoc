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

#LIBRARY_IOC += 12idcSupport

# 12idcRecord.h will be created from 12idcRecord.dbd
#DBDINC += 12idcRecord
# install support-library .dbd into <top>/dbd
#DBD += 12idcSupport.dbd

# The following are compiled and added to the Support library
#12idcSupport_SRCS += 12idcRecord.c

#12idcSupport_LIBS += $(EPICS_BASE_IOC_LIBS)

#=============================
# build an ioc application

PROD_IOC_DEFAULT = 12idc
PROD_IOC_solaris = 12idc

# <name>.dbd will be created from <name>Include.dbd
ifeq ($(OS_CLASS), WIN32)
DBD  += ioc12idcWin32.dbd
else
ifeq ($(EPICS_HOST_ARCH), cygwin-x86)
DBD  += ioc12idcCygwin.dbd
else
DBD  += ioc12idc.dbd
DBD  += ioc12idcVX.dbd
DBD  += ioc12idcLinux.dbd
DBD  += ioc12idc_solaris.dbd
endif
endif

# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
12idc_SRCS_DEFAULT  += ioc12idc_registerRecordDeviceDriver.cpp          12idcMain.cpp
12idc_SRCS_vxWorks  += ioc12idcVX_registerRecordDeviceDriver.cpp
12idc_SRCS_Linux    += ioc12idcLinux_registerRecordDeviceDriver.cpp     12idcMain.cpp
12idc_SRCS_WIN32    += ioc12idcWin32_registerRecordDeviceDriver.cpp     12idcMain.cpp
12idc_SRCS_cygwin32 += ioc12idcCygwin_registerRecordDeviceDriver.cpp    12idcMain.cpp
12idc_SRCS_solaris  += ioc12idc_solaris_registerRecordDeviceDriver.cppa 12idcMain.cpp
12idc_SRCS_vxWorks  += -nil-

#12idc_Common_LIBS += 12idcSupport
12idc_Common_LIBS += vac modbus
12idc_Common_LIBS += mca
12idc_Common_LIBS += calc
12idc_Common_LIBS += busy
12idc_Common_LIBS += sscan
12idc_Common_LIBS += autosave
12idc_Common_LIBS += optics
12idc_Common_LIBS += vme
12idc_Common_LIBS += std
12idc_Common_LIBS += ip
#12idc_Common_LIBS += brukerCCD
#12idc_Common_LIBS += marCCD
#12idc_Common_LIBS += roperCCD

#12idc_Common_LIBS += Acs Faulhaber Ims Mclennan Micos MicroMo NewFocus
#12idc_Common_LIBS += Newport PI Parker
12idc_Common_LIBS += softMotor motorSimSupport motor

12idc_Common_LIBS += asyn
12idc_Common_LIBS += stream streamSynApps
12idc_Common_LIBS += seqDev seq pv
12idc_Common_LIBS += $(EPICS_BASE_IOC_LIBS)

#12idc_vxWorks_LIBS += allenBradley
12idc_vxWorks_LIBS += mcaSIS
#12idc_vxWorks_LIBS += mcaCanberra
12idc_vxWorks_LIBS += ip330
12idc_vxWorks_LIBS += ipUnidig
12idc_vxWorks_LIBS += dac128V
#12idc_vxWorks_LIBS += quadEM
#12idc_vxWorks_LIBS += camac devCamac
#12idc_vxWorks_LIBS += dxp handel
#12idc_vxWorks_LIBS += love
12idc_vxWorks_LIBS += vxStats
12idc_vxWorks_LIBS += TyGSOctal Ipac
12idc_vxWorks_LIBS += oms 
#12idc_vxWorks_LIBS +=DeltaTau

#The following adds support from base/src/vxWorks
12idc_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

#12idc_Linux_LIBS  += dxp handel
# If libnet IS installed on your HOST Linux system;
# uncomment the following line.
ifeq ($(LINUX_NET_INSTALLED), YES)
12idc_Linux_LIBS  += mcaCanberra
endif

12idc_cygwin_LIBS += dxp handel

12idc_WIN32_LIBS += dxp handel

#12idc_solaris_LIBS += genSub
#12idc_solaris_LIBS += mca
12idc_solaris_LIBS += calc
12idc_solaris_LIBS += busy
12idc_solaris_LIBS += sscan
12idc_solaris_LIBS += autosave
12idc_solaris_LIBS += optics
#12idc_solaris_LIBS += vme
12idc_solaris_LIBS += std
#12idc_solaris_LIBS += ip
#12idc_solaris_LIBS += brukerCCD
#12idc_solaris_LIBS += marCCD
#12idc_solaris_LIBS += roperCCD
12idc_solaris_LIBS += motor softMotor motorSimSupport
12idc_solaris_LIBS += asyn
12idc_solaris_LIBS += seqDev seq pv
12idc_solaris_LIBS += $(EPICS_BASE_IOC_LIBS)


12idc_LIBS_DEFAULT = $(12idc_Common_LIBS)
12idc_LIBS_vxWorks = $(12idc_vxWorks_LIBS) $(12idc_Common_LIBS)
12idc_LIBS_Linux   = $(12idc_Linux_LIBS)   $(12idc_Common_LIBS)
12idc_LIBS_solaris = $(12idc_solaris_LIBS)
12idc_LIBS_cygwin32 = $(12idc_cygwin_LIBS) $(12idc_Common_LIBS)
12idc_LIBS_WIN32    = $(12idc_WIN32_LIBS)  $(12idc_Common_LIBS)

# If the host has libnet and libpcap for mca/Canberra support
# uncomment the following line.
ifeq ($(LINUX_NET_INSTALLED), YES)
12idc_SYS_LIBS_Linux += net pcap
endif
# For USB support on Saturn
ifeq ($(LINUX_USB_INSTALLED), YES)
12idc_SYS_LIBS_Linux += usb
endif
12idc_SYS_LIBS_vxWorks += -nil-

# This is needed by dxp on cygwin and WIN32
12idc_SYS_LIBS_cygwin32 += DLPORTIO PlxApi setupapi
12idc_LIBS_WIN32        += DLPORTIO PlxApi
12idc_SYS_LIBS_WIN32    += setupapi
# This is needed by saveData and asyn VXI-11 on cygwin
12idc_SYS_LIBS_cygwin32 += rpc


#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

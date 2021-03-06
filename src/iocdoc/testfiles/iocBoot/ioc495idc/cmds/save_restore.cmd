
# BEGIN save_restore.cmd ------------------------------------------------------

# Debug-output level
save_restoreSet_Debug(0)

### save_restore setup
#
# This file does not require modification for standard use, but...

# If you want save_restore to manage its own NFS mount, specify the name and
# IP address of the file server to which save files should be written, and
# call set_savefile_path() with a path as the server sees it.  This currently
# is supported only on vxWorks.
# If the NFS mount from nfsCommands is used, call set_savefile_path() with a
# path as mounted by that file
# That is, do this...
#set_savefile_path(startup, "autosave")
# ... or this...
save_restoreSet_NFSHost("s26dserv", "164.54.128.3")
set_savefile_path("/xorApps/epics/synApps_5_7/ioc/495idc/iocBoot/ioc495idc", "autosave")

# status PVs: default is to use them
#save_restoreSet_UseStatusPVs(1)

save_restoreSet_status_prefix("495idc:")
#!dbLoadRecords("$(AUTOSAVE)/databases/save_restoreStatus.db", "P=495idc:, DEAD_SECONDS=5")

# Ok to save/restore save sets with missing values (no CA connection to PV)?
save_restoreSet_IncompleteSetsOk(1)

# Save dated backup files?
save_restoreSet_DatedBackupFiles(1)

# Number of sequenced backup files to write
save_restoreSet_NumSeqFiles(12)

# Time interval between sequenced backups
save_restoreSet_SeqPeriodInSeconds(43200)

# Ok to retry connecting to PVs whose initial connection attempt failed?
save_restoreSet_CAReconnect(1)

# Time interval in seconds between forced save-file writes.  (-1 means forever).
# This is intended to get save files written even if the normal trigger mechanism is broken.
save_restoreSet_CallbackTimeout(-1)

###
# specify what save files should be restored.  Note these files must be
# in the directory specified in set_savefile_path(), or, if that function
# has not been called, from the directory current when iocInit is invoked
set_pass0_restoreFile("auto_positions.sav")
set_pass0_restoreFile("auto_settings.sav")
set_pass1_restoreFile("auto_settings.sav")

###
# specify directories in which to search for included request files
# Note that the vxWorks variables (e.g., 'startup') are from cdCommands
set_requestfile_path(startup, "")
set_requestfile_path(startup, "autosave")
set_requestfile_path("area_detector", "ADApp/Db")
set_requestfile_path(autosave, "asApp/Db")
set_requestfile_path(busy, "busyApp/Db")
set_requestfile_path(calc, "calcApp/Db")
set_requestfile_path(camac, "camacApp/Db")
set_requestfile_path(dac128v, "dac128VApp/Db")
set_requestfile_path(dxp, "dxpApp/Db")
set_requestfile_path(ip, "ipApp/Db")
set_requestfile_path(ip330, "ip330App/Db")
set_requestfile_path(ipunidig, "ipUnidigApp/Db")
set_requestfile_path(love, "loveApp/Db")
set_requestfile_path(mca, "mcaApp/Db")
set_requestfile_path(meascomp, "measCompApp/Db")
set_requestfile_path(modbus, "modbusApp/Db")
set_requestfile_path(motor, "motorApp/Db")
set_requestfile_path(optics, "opticsApp/Db")
set_requestfile_path(quadem, "quadEMApp/Db")
set_requestfile_path(softglue, "softGlueApp/Db")
set_requestfile_path(sscan, "sscanApp/Db")
set_requestfile_path(std, "stdApp/Db")
set_requestfile_path(vac, "vacApp/Db")
set_requestfile_path(vme, "vmeApp/Db")
set_requestfile_path(top, "495idcApp/Db")

# END save_restore.cmd --------------------------------------------------------

## Load Xradia motor records
# Currently this only loads the _able and _ableput records, because the motor record is commented
# out of xradia_motor.db.  The motors records reside in the IOC provided by xradia on a Windows machine.
dbLoadTemplate("templates/xradia_motor.substitutions")

## Load Xradia motor records for seamless motion
dbLoadTemplate("templates/xradia_seamless_motion.substitutions")

## Load Xradia seamless motion motor tweak controls
dbLoadRecords("$(TOP)/495idcApp/Db/xradia_seamless_motion_tweak.db","P=495idcnpi:,XY=X")
dbLoadRecords("$(TOP)/495idcApp/Db/xradia_seamless_motion_tweak.db","P=495idcnpi:,XY=Y")

## Allow stopping of coarse motors, 1-24
dbLoadRecords("$(TOP)/495idcApp/Db/coarse_com_24.db","P=495idcnpi:,R=coarse:")

## Allow NPI hybrid motions to be stopped
dbLoadRecords("$(TOP)/495idcApp/Db/all_com_2.db","P=495idcnpi:,R=hybridX:,M1=m10,M2=m34")
dbLoadRecords("$(TOP)/495idcApp/Db/all_com_2.db","P=495idcnpi:,R=hybridY:,M1=m11,M2=m35")

### How to handle aliases when motors reside in a different ioc?

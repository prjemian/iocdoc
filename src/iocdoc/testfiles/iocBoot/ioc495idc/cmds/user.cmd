### Stuff for user programming ###
dbLoadRecords("$(CALC)/calcApp/Db/userCalcs10.db","P=495idc:1:")
dbLoadRecords("$(CALC)/calcApp/Db/userCalcs10.db","P=495idc:2:")
dbLoadRecords("$(CALC)/calcApp/Db/userCalcs10.db","P=495idc:3:")
dbLoadRecords("$(CALC)/calcApp/Db/userCalcOuts10.db","P=495idc:")
dbLoadRecords("$(CALC)/calcApp/Db/userStringCalcs10.db","P=495idc:1:")
dbLoadRecords("$(CALC)/calcApp/Db/userStringCalcs10.db","P=495idc:2:")
dbLoadRecords("$(CALC)/calcApp/Db/userArrayCalcs10.db","P=495idc:,N=2000")
dbLoadRecords("$(CALC)/calcApp/Db/userStringSeqs10.db","P=495idc:")
dbLoadRecords("$(CALC)/calcApp/Db/userTransforms10.db","P=495idc:1:")
dbLoadRecords("$(CALC)/calcApp/Db/userTransforms10.db","P=495idc:2:")
dbLoadRecords("$(CALC)/calcApp/Db/userAve10.db","P=495idc:")

# Placeholder PVs
dbLoadTemplate("templates/placeholders.substitutions")

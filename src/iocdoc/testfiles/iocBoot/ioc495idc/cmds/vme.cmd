
# BEGIN vme.cmd ---------------------------------------------------------------

# OMS MAXv driver setup parameters: 
#     (1)number of cards in array.
#     (2)VME Address Type (16,24,32).
#     (3)Base Address on 4K (0x1000) boundary.
#     (4)interrupt vector (0=disable or  64 - 255).
#     (5)interrupt level (1 - 6).
#     (6)motor task polling rate (min=1Hz,max=60Hz).
#drvMAXvdebug=4
MAXvSetup(2, 16, 0x5000,     180, 5, 10)

# OMS MAXv configuration string:
#     (1) number of card being configured (0-14).
#     (2) configuration string; axis type (PSO/PSE/PSM) MUST be set here.
#         For example, set which TTL signal level defines
#         an active limit switch.  Set X,Y,Z,T to active low and set U,V,R,S
#         to active high.  Set all axes to open-loop stepper (PSO). See MAXv
#         User's Manual for LL/LH and PSO/PSE/PSM commands.
#     (3) SSI based absolute encoder bit flag. Bit #0 for Axis X, bit #1 for
#         Axis Y, etc.. Set a bit flag to '1' for absolute encoder values; '0'
#         for the standard incremental encoder values.
config0="AX LL PSO; AY LL PSO; AZ LL PSO; AT LL PSO; AU LL PSO; AV LL PSO; AR LL PSO; AS LL PSO;"
MAXvConfig(0, config0, 0x00)
MAXvConfig(1, config0, 0x00)

# Struck 3820 MCS setup
#iocsh "cmds/st_SIS3820.iocsh"
# Create PV aliases so old medm screens can be used
#!dbLoadRecords("$(TOP)/495idcApp/Db/scalerAliases.db","P=495idc:,S=scaler1,PA=495idcDET:,SA=scaler1")

# Acromag AVME9440 setup parameters:
# devAvem9440Config (ncards,a16base,intvecbase)
devAvme9440Config(1,0x0400,0x78)

# Acromag general purpose Digital I/O
#dbLoadRecords("$(VME)/vmeApp/Db/Acromag_16IO.db", "P=495idc:, A=1, C=0")

# END vme.cmd -----------------------------------------------------------------

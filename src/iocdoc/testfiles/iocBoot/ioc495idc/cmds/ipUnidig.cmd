
# BEGIN ipUnidig.cmd ----------------------------------------------------------

# Initialize Greenspring IP-Unidig
# initIpUnidig(char *portName,
#              int carrier,
#              int slot,
#              int msecPoll,
#              int intVec,
#              int risingMask,
#              int fallingMask)
# portName  = name to give this asyn port
# carrier     = IPAC carrier number (0, 1, etc.)
# slot        = IPAC slot (0,1,2,3, etc.)
# msecPoll    = polling time for input bits that don't use interrupts in msec.
# intVec      = interrupt vector
# risingMask  = mask of bits to generate interrupts on low to high (24 bits)
# fallingMask = mask of bits to generate interrupts on high to low (24 bits)
#
initIpUnidig("Unidig1", 0, 2, 2000, 116, 0xffffff, 0xffffff)

# IP-Unidig binary I/O
dbLoadTemplate "ipUnidig.substitutions"

# END ipUnidig.cmd ------------------------------------------------------------

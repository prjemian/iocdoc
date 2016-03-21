
# BEGIN industryPack.cmd ------------------------------------------------------

# This configures the Industry Pack Support

# First carrier
# slot a: Ip330 (A/D converter)
# slot b: Dac128V (D/A converter)
# slot c: IpUnidig (digital I/O)
# slot d: IP-EP201 (FPGA)

###############################################################################
# Initialize IP carrier
# ipacAddCarrier(ipac_carrier_t *pcarrier, char *cardParams)
#   pcarrier   - pointer to carrier driver structure
#   cardParams - carrier-specific init parameters

# Select for Tews TVME-200 (also sold by SBS as VIPC626) version IP carrier.
# Config string is hex values of the six rotary switches on the board.
# In this example, the card is at a16 address 0x3000 ("30"), uses the interrupt
# assignment ("1"), uses the 32-bit address space for module memory
# ("f"), and maps that memory to A32 address 0xa000000 ("a0")
ipacAddTVME200("302fa0")
#ipacAddTVME200("342fa2")

# Print out report of IP modules
ipacReport(2)

# Analog I/O (Acromag IP330 ADC)
< cmds/ip330.cmd

# Systran DAC128V
< cmds/dac128V.cmd

# SBS IpUnidig digital I/O
#!< cmds/ipUnidig.cmd

# user programmable glue electronics (requires Acromag IP-EP20x)
#!< cmds/softGlue.cmd

# END industryPack.cmd --------------------------------------------------------

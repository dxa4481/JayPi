import RPIO

RPIO.setmode(RPIO.BOARD)

pins = range(2,12)

RPIO.setup()

"""
    Once you have found the JTAG pins you can define
    the following to allow for the boundary scan and
    irenum functions to be run. Define the values
    as the index for the pins[] array of the found
    jtag pin:
"""
TCK = 0
TMS = 1
TDO = 2
TDI = 3
TRST = 4

#Pattern used for scan() and loopback() tests
pattern_len = 64

pattern = [0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1]

MAX_DEV_NR = 8
IDCODE_LEN = 32

SCAN_LEN = 1890
IR_LEN = 5

IR_IDCODE= [0, 1, 1, 0, 0]
IR_SAMPLE = [1, 0, 1, 0, 0]

IR_PRELOAD = IR_SAMPLE

TAP_RESET = [1, 1, 1, 1, 1]

TAP_SHIFTDR = [1, 1, 1, 1, 1, 0, 1, 0, 0]
TAP_SHIFTIR = [1, 1, 1, 1, 1, 0, 1, 1, 0, 0]

IGNOREPIN = 65535

VERBOSE = False
DELAY = False
DELAYUS = 5000
PULLUP = 255
DEBUGTAP = False

pinslen = len(pins)

def tap_state(tap_state, tck, tms):
    if DEBUGTAP:
        print "tap_state: tms set to: "
    for tap in tap_state:
        if (DELAY):
            sleep(0.000005)
        RPIO.output(tck, 0)
        RPIO.output(tms, tap)
        if DEBUGTAP:
            print(tap)
        RPIO.output(tck, True)

def pulse_tms(tck, tms, s_tms):
    if(tck == IGNOREPIN):
        return
    RPIO.output(tck, 0)
    RPIO.output(tms, s_tms)
    RPIO.output(tck, 1)

def pulse_tdi(tck, tdi, s_tdi):
    if(DELAY):
        sleep(0.000005)
    if(tck != IGNOREPIN):
        RPIO.output(tck, 0)
        RPIO.output(tdi, s_tdi)
        RPIO.output(tck, 1)
    else:
        RPIO.output(tdi, s_tdi)

def pulse_tdo(tck, tdo):
    if(DELAY):
        sleep(0.000005)
    RPIO.output(tck, 0)
    tdo_read = RPIO.input(tdo)
    RPIO.output(tck, 1)
    return tdo_read

def init_pins(tck=IGNOREPIN, tms=IGNOREPIN, tdi=IGNOREPIN, ntrst=IGNOREPIN):
    for i in range(pinslen):
        RPIO.setup(pins[i], RPIO.IN)
        #Figure out pullup on RPI
        #if(PULLUP):
        #    RPIO

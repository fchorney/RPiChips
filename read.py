#!/usr/bin/env python

import time
from sys import argv
from RPiChips.TLC0838 import TLC0838

adc = TLC0838(0, 0)

if len(argv) > 1:
    channel = int(argv[1])
else:
    channel = 0

print adc

try:
    while 1:
        ch = adc.read(channel)

        print ch

        time.sleep(1)
except KeyboardInterrupt:
    pass

adc.close()

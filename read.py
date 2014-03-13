#!/usr/bin/env python

import time
from RPiChips.TLC0838 import TLC0838

adc = TLC0838(0, 0)

try:
    while 1:
        ch0 = adc.read(0)

        print ch0.msbf
        print ch0.lsbf

        time.sleep(2)
except KeyboardInterrupt:
    pass

adc.close()

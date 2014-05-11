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
previous = ''

try:
    t = time.time()
    samples = 0
    while time.time() - t < 1.0:
        ch = adc.read(channel)
        current = "%s:%s" % (ch.int, ch.vcc)

        samples += 1

        print current

except KeyboardInterrupt:
    pass

print "Total Time:    ", time.time() - t
print "Total Samples: ", samples

adc.close()

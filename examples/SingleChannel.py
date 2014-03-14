#!/usr/bin/env python

import time

from sys import argv
from RPiChips.TLC0838 import TLC0838

def main():
    adc = TLC0838(0, 0)

    if len(argv) > 1:
        channel = int(argv[1])
    else:
        channel = 0

    print adc

    try:
        while 1:
            ch = adc.read(channel)

            print "%s:%s" % (ch.int, ch.vcc)

    except KeyboardInterrupt:
        pass

    adc.close()

if __name__ == '__main__':
    main()

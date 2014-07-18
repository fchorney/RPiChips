RPiChips
========

Python code for various chips

MAX532
------

## Chip Diagram
```
                                             +-----U-----+
               Tied to VOUTA -->        RFBA | 1      16 | VDD          <-- +12v
                 12v or -12v -->       VREFA | 2      15 | LDAC         <-- Digital Ground (3 Wire Interface) / GPIO (4 Wire Interface)
                Analog Out A -->       VOUTA | 3      14 | CS           <-- CE0
               Analog Ground -->       AGNDA | 4      13 | DIN          <-- MOSI
               Analog Ground -->       AGNDB | 5      12 | DOUT         <-- MISO
                Analog Out B -->       VOUTB | 6      11 | SCLK         <-- SCLK
                 12v ot -12v -->       VREFB | 7      10 | DGND         <-- Digital Ground
               Tied to VOUTB -->        RFBB | 8       9 | VSS          <-- -12v
                                             +-----------+
```

## Examples
### Coming Soon...

TLC0838
-------

## Chip Diagram
```
                                             +-----U-----+
                ANLG SRC/GND -->         CH0 | 1      20 | Vcc          <-- 5v5
                ANLG SRC/GND -->         CH1 | 2      19 | NC           <-- NC
                ANLG SRC/GND -->         CH2 | 3      18 | CS           <-- CE0
                ANLG SRC/GND -->         CH3 | 4      17 | DI           <-- MOSI
                ANLG SRC/GND -->         CH4 | 5      16 | CLK          <-- SCLK
                ANLG SRC/GND -->         CH5 | 6      15 | SARS         <-- LED
                ANLG SRC/GND -->         CH6 | 7      14 | DO           <-- MISO
                ANLG SRC/GND -->         CH7 | 8      13 | SE           <-- GND
                         GND -->         COM | 9      12 | REF          <-- 5v5
                         GND -->    DGTL GND | 10     11 | ANLG GND     <-- GND
                                             +-----------+
```

## Examples
#### SingleChannel.py

This script takes a single argument for the channel you want to convert and display. If no channel is given, channel 0 is desplayed by default.
Script assumes Bus 0 and CE0 with a voltage reference of 5v.

```
    ~# ./SingleChannel.py 1
    TLC0838<bus='0', ce='0', vref='5.0', spi='<SpiDev object at 0xb6cc0440>'>
    255:5.0
```


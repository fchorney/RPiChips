import spidev

CHANNEL_BYTES = {
    0: 0x80,
    1: 0xC0,
    2: 0x90,
    3: 0xD0,
    4: 0xA0,
    5: 0xE0,
    6: 0xB0,
    7: 0xF0
}
START_BYTE = 0x01
PADDING_BYTE = 0x00
HEX_SCALE = 16
BINARY_SCALE = 8
BYTE_MAX = 256

class TLC0838():
    def __init__(self, bus=0, ce=0, voltage=5.0):
        self.bus = bus
        self.ce = ce
        self.voltage = voltage

        try:
            self.spi = spidev.SpiDev()
            self.spi.open(bus, ce)
        except Exception as e:
            print "Could Not Open SPI(%s, %s)" % (bus, ce)
            raise

    def close(self):
        self.spi.close()

    def read_all(self):
        SPEED = 250000
        DELAY = 440
        data = {}
        for ch_key in CHANNEL_BYTES.keys():
            instruction = [START_BYTE, CHANNEL_BYTES[ch_key], PADDING_BYTE]
            response = self.spi.xfer2(instruction, SPEED, DELAY)

            # Convert response to binary
            bin_str = ""
            for idx in range(0, len(response)):
                bin_str += bin(
                    int(str(response[idx]), HEX_SCALE)
                )[2:].zfill(BINARY_SCALE)

            # Our data resides within the 13th to the 21st bit
            binary_raw = bin_str[13:21]
            decimal_raw = int(binary_raw, 2)
            hex_raw = hex(decimal_raw)

            # Get Voltage
            voltage = (float(decimal_raw) / float(BYTE_MAX) * self.voltage)

            data[ch_key] = {
                'raw': {
                    'binary': binary_raw,
                    'decimal': decimal_raw,
                    'hexidecimal': hex_raw
                },
                'binary_string': bin_str,
                'bus': self.bus,
                'ce': self.ce,
                'reference voltage': self.voltage,
                'voltage': voltage
            }

        return data

    def read(self, channel):
        return self.read_all()[channel]

    def read_voltage(self, channel):
        data = self.read(channel)['voltage']

        return "%s:%s:%s - %s" % (self.bus, self.ce, channel, data)


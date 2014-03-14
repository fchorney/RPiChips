import spidev

class TLC0838Reading():
    def __init__(self, binary_string, vref):
        self.raw_bin = binary_string
        self.vref = vref
        self.bin = binary_string[9:17]
        self.int = int(self.bin, 2)
        self.hex = hex(self.int)
        self.vcc = (float(self.int) / 255.0 * self.vref)

    def __str__(self):
        args = (
            self.raw_bin, self.vref,
            self.bin, self.int, self.hex, self.vcc
        )
        return (
            "TLC0838Reading<raw_bin='%s', vref='%s', bin='%s', " +
            "int='%s', hex='%s', vcc='%s'>"
        ) % args

class TLC0838():
    # Single Channel Address
    SCADDR = {
        0: 0x08,
        1: 0x0C,
        2: 0x09,
        3: 0x0D,
        4: 0x0A,
        5: 0x0E,
        6: 0x0B,
        7: 0x0F
    }

    # Differential Channel Address
    DCADDR = {
        0: 0x00,
        1: 0x04,
        2: 0x01,
        3: 0x05,
        4: 0x02,
        5: 0x06,
        6: 0x03,
        7: 0x07
    }

    # Constants
    PADDING_BYTE = 0x00
    START_BYTE = 0x10

    # SPI Interface Constants
    SPI_SPEED = 250000
    SPI_DELAY = 440

    def __init__(self, bus, ce, vref=5.0):
        self.bus = bus
        self.ce = ce
        self.vref = vref

        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(bus, ce)

    def __str__(self):
        args = (
            self.bus, self.ce, self.vref, self.spi
        )
        return "TLC0838<bus='%s', ce='%s', vref='%s', spi='%s'>" % args

    def close(self):
        self.spi.close()

    def read(self, channel, differential=False):
        inst = self._make_instruction(channel, differential=differential)
        resp = self.spi.xfer2(inst, TLC0838.SPI_SPEED, TLC0838.SPI_DELAY)

        # Combine response into single binary string
        binary_string = ''
        for byte in resp:
            binary_string += bin(byte)[2:].zfill(8)

        result = TLC0838Reading(binary_string, self.vref)
        return result

    def _make_instruction(self, channel, differential=False):
        # Figure out if we want single channel or differential channel
        addrs = TLC0838.SCADDR if not differential else TLC0838.DCADDR
        # Combine start byte with channel byte
        addr_byte = TLC0838.START_BYTE | addrs[channel]
        # Return instruction, start/channel byte plus 2 padding bytes
        return [addr_byte, TLC0838.PADDING_BYTE, TLC0838.PADDING_BYTE]

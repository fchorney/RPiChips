import spidev

class MAX532():
    # Special Values
    MIN_VALUE = 0b000000000000 # 0
    MAX_VALUE = 0b111111111111 # 4095


    # SPI Interface Constants
    SPI_SPEED = 4000
    SPI_DELAY = 100


    def __init__(self, bus, ce, vref = 12.0):
        self.bus = bus
        self.ce = ce
        self.output_a = MAX532.MIN_VALUE
        self.output_b = MAX532.MIN_VALUE
        self.vref = vref

        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(bus, ce)
        self.set_output()


    def __str__(self):
        args = (
            self.bus, self.ce, self.vref, self.spi
        )
        return "MAX532<bus='%s', ce='%s', vref='%s', spi='%s'>" % args


    def close(self):
        self.spi.close()


    def value_to_voltage(self, value):
        return (float(value) / float(MAX532.MAX_VALUE) * self.vref)


    def voltage_to_value(self, voltage):
        if voltage > self.vref:
            voltage = self.vref
        if voltage < 0:
            voltage = 0

        return int((float(voltage) / float(self.vref) * MAX532.MAX_VALUE))


    def clamp_outputs(self):
        if self.output_a > MAX532.MAX_VALUE:
            self.output_a = MAX532.MAX_VALUE
        if self.output_a < MAX532.MIN_VALUE:
            self.output_a = MAX532.MIN_VALUE

        if self.output_b > MAX532.MAX_VALUE:
            self.output_b = MAX532.MAX_VALUE
        if self.output_b < MAX532.MIN_VALUE:
            self.output_b = MAX532.MIN_VALUE


    def create_packet(self):
        a = (self.output_b >> 4)
        b = ((self.output_b & 0xF) << 4) + (self.output_a >> 8)
        c = (self.output_a & 0xFF)

        return [a, b, c]


    def set_output(self, output_a=None, output_b=None):
        if output_a is not None:
            self.output_a = output_a
        if output_b is not None:
            self.output_b = output_b

        # Clamp output values
        self.clamp_outputs()

        # Create output packet
        packet = self.create_packet()
        print "Out  A: %s" % hex(self.output_a)
        print "Out  B: %s" % hex(self.output_b)
        print "Packet: %s" % packet
        print "   Hex: [%02X, %02X, %02X]" % (packet[0],packet[1],packet[2])
        print "Results: A = %sv, B = %sv" % ((float(self.output_a) / MAX532.MAX_VALUE) *
                self.vref, (float(self.output_b) / MAX532.MAX_VALUE) * self.vref)

        # Send packet
        resp = self.spi.xfer2(packet, MAX532.SPI_SPEED, MAX532.SPI_DELAY)

        return resp

import pigpio
import time

class DY08:
    """
    Handles controlling Solight DY08 sockets.
    """

    def __init__(self, pi, pin):
        """
        Constructs the instance. Args:
        * pi - connection to pigpio daemon
        * pin - BCM pin number of GPIO
        """

        pi.set_mode(pin, pigpio.OUTPUT)
        self.pi = pi
        self.pin = pin

    def send(self, address, action):
        """
        Transmits the command. Args:
        * address - 37 bit address of the socket.
        * action - 1 - turn on or 0 - turn off
        """

        def add_bit(wf, pin, bit, pulse_lengths):
            if bit == 0:
                wf.append(pigpio.pulse(1 << pin, 0, pulse_lengths[0]))
                wf.append(pigpio.pulse(0, 1 << pin, pulse_lengths[1]))
            else:
                wf.append(pigpio.pulse(1 << pin, 0, pulse_lengths[1]))
                wf.append(pigpio.pulse(0, 1 << pin, pulse_lengths[0]))

        def add_byte(wf, pin, byte, pulse_lengths):
            for _ in range(8):
                add_bit(wf, pin, byte & 128, pulse_lengths)
                byte <<= 1

        def add_bytes(wf, pin, data, repeat_count, header_length, pulse_lengths):
            for _ in range(repeat_count):
                wf.append(pigpio.pulse(1 << pin, 0, pulse_lengths[0]))
                wf.append(pigpio.pulse(0, 1 << pin, header_length))
                for byte in data:
                    add_byte(wf, pin, byte, pulse_lengths)

        self.pi.wave_clear()
        wf = []

        address = address & ((2 ** 37) - 1)

        first = [0x90, 0x24, 0x20 | (address >> 32)]
        second = [(address >> 24) & 0xFF, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]

        if action != 0:
            first = [first[0] ^ 0x0E, first[1] ^ 0x49, first[2] ^ 0x90]
            second = [second[0] ^ 0xC3, second[1] ^ 0x21, second[2] ^ 0x62, second[3] ^ 0x40]

        add_bytes(wf, self.pin, first, 5, 2388, (400, 1100))
        add_bytes(wf, self.pin, second, 4, 7292, (570, 1500))

        wf.append(pigpio.pulse(0, 1 << self.pin, 59400))

        self.pi.wave_add_generic(wf)
        wid = self.pi.wave_create()

        self.pi.wave_send_once(wid)
        while self.pi.wave_tx_busy():
            time.sleep(0.2)

        self.pi.wave_tx_stop()
        self.pi.write(self.pin, 0)

if __name__ == "__main__":
    dy08 = DY08(pigpio.pi(), 17)

    while True:
        dy08.send(42, 1);
        time.sleep(1)
        dy08.send(42, 0);
        time.sleep(1)

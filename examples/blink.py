#!/usr/bin/python

import time
import pigpio
from dy08 import DY08

def main():
    dy08 = DY08(pigpio.pi(), 17)

    socket = 42

    while True:
        dy08.send(socket, 1);
        time.sleep(1)
        dy08.send(socket, 0);
        time.sleep(1)

if __name__ == "__main__":
    main()

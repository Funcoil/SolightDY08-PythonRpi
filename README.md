Python Solight DY08 library for Raspberry Pi
============================================

This library allows you to control [Solight DY08](http://shop.solight.sk/solight-dialkovo-ovladane-zasuvky-set-2--1-2-zasuvky-1-ovladac-learning-code-detail-1FZ1000201.aspx) sockets from Raspberry Pi.

How to use it
-------------

Connect cheap [433 MHz transmitter](https://www.robotshop.com/en/seeedstudio-433mhz-low-cost-transmitter-receiver-pair.html) to any GPIO pin (e.g. 17)

```
sudo apt-get install pigpio-python
sudo pigpiod
```

```python
import time
import pigpio
from dy08 import DY08

pi = pigpio.pi()
dy08 = DY08(pi, 17)

while True:
	dy08.send(42, 1)
	time.sleep(1)
	dy08.send(42, 0)
	time.sleep(1)
```

...

Profit! :D

License
-------

MITNFA

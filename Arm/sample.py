import time
from glob import glob

from pydobot import Dobot
import serial.tools.list_ports


ports = list(serial.tools.list_ports.comports())
if len(ports) == 0:
    print('no port found for Dobot Magician')
    exit(1)
	
for p in ports:
	print(p.device)

print(ports[0].device)
device = Dobot(port=ports[0].device)

time.sleep(0.5)
device.speed(10)
device.go(135.0, 0.0, 0.0)
device.close()
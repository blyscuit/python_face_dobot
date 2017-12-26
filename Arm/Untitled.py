import time
from glob import glob

from pydobot import Dobot

available_ports = glob('/dev/cu*usb*')  # mask for OSX Dobot port
if len(available_ports) == 0:
	print('no port found for Dobot Magician')
	exit(1)
print(available_ports)
device = Dobot(port=available_ports[0],verbose=True)
device.speed(10)
#device = Dobot(port=available_ports[0])
#print(device.MODE_PTP_MOVJ_XYZ)
#time.sleep(0.5)
#device.speed(100)
device._set_ptp_cmd(250.0, 10.0, 25.0, 1.0, 1)
time.sleep(2)
device.go(200.0, 100.0, 25.0)
#device.go(250.0, 0.0, 0.0)
time.sleep(2)
device.close()
import time
from glob import glob

from pydobot import Dobots

class dbot:

    PORT = 'COM7'

    z_min = -58.0
    z_release = -55.0
    #z_mid = 0.0

    hide = [135.0, 0.0, 0.0]
    tray = [0.0, 250.0, z_release]

    def __init__(self):
        device = Dobot(port=PORT)

    def hide(self):
        device.go(*hide)
        time.sleep(5)

    def pickUp(self, x, y):
        device.go(x, y, z_min)
        time.sleep(5)
        device.suck(True)
        time.sleep(1)
        device.go(x, y, 0.0)
        time.sleep(5)
    
    def place(self)
        device.go(*tray)
        time.sleep(5)
        device.suck(False)
        time.sleep(1)
        device.go(*tray[:2], 0.0)
        time.sleep(5)

    time.sleep(0.5)
    device.speed(10)
    #will have to 
    """device.go(*hide)"""

    #time.sleep(2)
    #device.go(250.0, 0.0, 50.0)
    time.sleep(2)
    device.close()


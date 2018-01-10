import time
from glob import glob
from pydobot import Dobot

class dbot:

    PORT = 'COM7'

    z_min = -58.0
    z_release = -55.0
    #z_mid = 0.0

    hide = [135.0, 0.0, 0.0]
    tray = [0.0, 250.0, z_release]

    def __init__(self):
        self.device = Dobot(port = dbot.PORT)
        self.setSpeed(10)
        time.sleep(2)

    def hide(self):
        self.device.go(*dbot.hide)
        time.sleep(5)

    def pickUp(self, x, y):
        self.device.go(x, y, dbot.z_min)
        time.sleep(5)
        self.device.suck(True)
        time.sleep(1)
        self.device.go(x, y, 0.0)
        time.sleep(5)
    
    def place(self):
        self.device.go(*dbot.tray)
        time.sleep(5)
        self.device.suck(False)
        time.sleep(1)
        self.device.go(*dbot.tray[:2], z=0.0)
        time.sleep(5)

    def goCalib(self,x ,y):
        self.device.go(x,y,0)
        time.sleep(5)
    
    def setSpeed(self, speed):
        self.device.speed(speed)
    
    def closeDevice(self):
        self.device.close()
        time.sleep(0.5)
    #will have to 
    """device.go(*hide)"""

    #time.sleep(2)
    #device.go(250.0, 0.0, 50.0)



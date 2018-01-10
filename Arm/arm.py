import time
from CoordTransformer import coordclass
from glob import glob
from pydobot import Dobot

class dbot:

    PORT = 'COM7'

    z_min = -58.0
    z_release = -55.0
    #z_mid = 0.0

    hide_pos = [135.0, 0.0, 0.0]
    tray = [0.0, 250.0, z_release]

    def __init__(self):
        self.device = Dobot(port = dbot.PORT)
        self.setSpeed(10)
        time.sleep(2)

    def hide(self):
        print('Hiding start')
        self.device.go(*dbot.hide_pos)
        time.sleep(5)
        print('Hiding finished')

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
        print('Calib start')
        self.device.go(x,y,0)
        time.sleep(5)
        print('Hiding finish')
    
    def setSpeed(self, speed):
        self.device.speed(speed)
    
    def closeDevice(self):
        print('Closing start')
        self.device.close()
        time.sleep(0.5)
        print('Closing finish')
    #will have to 
    """device.go(*hide)"""

    #time.sleep(2)
    #device.go(250.0, 0.0, 50.0)

d = dbot()
cd = coordclass(1.5, 206.4, 0.0, 480, 360)
target = cd.getCoordinates((405, 533))
d.hide()
d.goCalib(target[0], target[1])
d.closeDevice()




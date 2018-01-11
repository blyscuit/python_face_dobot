import time
import math
from robot_arm.CoordTransformer import coordClass
from glob import glob
from pydobot import Dobot

class dbot:

    has_obj = False

    PORT = 'COM7'

    z_min = -65.0
    z_hover = -60.0
    #z_mid = 0.0

    hide_pos = [135.0, 0.0, 0.0]
    tray = [0.0, -250.0, z_hover]

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
        print('PickUp start')
        self.device.go(x, y, 0.0)
        time.sleep(5)
        print('PickUp lower')
        self.device.go(x, y, dbot.z_min)
        time.sleep(3)
        print('PickUp suck')
        self.device.suck(True)
        time.sleep(1)
        print('PickUp lift')
        self.device.go(x, y, 0.0)
        time.sleep(3)
        print('PickUp finished')
        dbot.has_obj = True
    
    def place(self):
        if dbot.has_obj:
            print('Place start')
            self.device.go(*dbot.tray[:2], z=0.0)
            time.sleep(5)
            print('Place lower')
            self.device.go(*dbot.tray)
            time.sleep(3)
            print('Place release')
            self.device.suck(False)
            time.sleep(1)
            print('Place raise')
            self.device.go(*dbot.tray[:2], z=0.0)
            time.sleep(3)
            print('Place finished')
            dbot.has_obj = False
        else:
            print('No object to place')
            time.sleep(1)

    def hide(self):
        print('Hiding start')
        self.device.go(*dbot.hide_pos)
        time.sleep(5)
        print('Hiding finished')

    def hover(self, x, y):
        print('Hover start')
        self.device.go(x, y, 0.0)
        time.sleep(5)
        print('Hover lower')
        self.device.go(x, y, dbot.z_hover)
        time.sleep(3)
        print('Hover lift')
        self.device.go(x, y, 0.0)
        time.sleep(3)
        print('Hover finished')

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

'''
d = dbot()
cd = coordClass(1.0 / 1.5, 206.4, 0.0, 360, 480)
target = cd.getCoordinates((405, 533))
d.hide()
d.goCalib(target[0], target[1])
d.closeDevice()
'''




import math
import numpy as np
#import cv2

class coordClass:
    #Assume that the calibration position of objects posted is at (50,CamY),(250,Camy),(CamX,150),(CamX,-150) in real world coords
    #
    """
        mm/px = ration
        x1 = calibration values px val at W(0,150)
        x2 = calibration values px val at W(0,-150)
        y1 = calibration values px val at W(50,0)
        y2 = calibration values px val at W(250,0)
        camX = x coordinates of the camera relative to world frame
        camY = y coordinates of the cmarea relative to the world frame
        cenX = center Pixel x coordinate
        cenY = center Pixel y coordinate
    """

    '''
    Robot +X = Image +X
    Robot +Y = Image -Y
    '''
    
    #safety measures
    r_max = 300.0
    r_min = 200.0

    def __init__(self, mmPxRate, camX, camY, cenX, cenY):
    #def __init__(self, mmPxRate, x1, x2, y1, y2, camX, camY, cenX, cenY):
        #x+ up, x- down, y+ left, y- right
        self.px_to_mm = mmPxRate
        """
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        """
        self.rob_cen_mm = (float(camX), float(camY))
        self.cam_cen_px = (float(cenX), float(cenY))

    def is_in_range(self, obj_cen_mm):
        r = math.sqrt((obj_cen_mm[0] ** 2) + (obj_cen_mm[1] ** 2))
        if r >= coordClass.r_min and r <= coordClass.r_max:
            return True
        return False

    def getCoordinates(self, obj_cen_px):

        cam_to_obj_px = np.subtract(obj_cen_px, self.cam_cen_px)
        obj_mm = [self.rob_cen_mm[0] + (0.5 * cam_to_obj_px[0] * self.px_to_mm), self.rob_cen_mm[1] + (-0.5 * cam_to_obj_px[1] * self.px_to_mm)]
        obj_x_normalize_mm = -20.0 * ((0.5 * cam_to_obj_px[0] * self.px_to_mm) / 100.0)
        obj_y_normalize_mm = -10.0 * ((-0.5 * cam_to_obj_px[1] * self.px_to_mm) / 200.0)
        print(obj_y_normalize_mm)
        obj_mm[0] += obj_x_normalize_mm
        obj_mm[1] += obj_y_normalize_mm
        return tuple(obj_mm)

        '''
        #for testing will consider the centroid as a tuple. However for actual implement will get x and y
        xPx = float(centroid[0])
        yPx = float(centroid[1])
        """
        realY2 = ((self.camX-250)/(self.mmPxRate))+self.cenY
        realY1 = ((self.camX-50)/(self.mmPxRate))+self.cenY
        realX1 = ((self.camX-150)/(self.mmPxRate))+self.cenX
        realX2 = ((self.camX+150)/(self.mmPxRate))+self.cenX
        """
        """
        xScaling = ((realX1/self.x1)+(realX2/self.x2))/2.0
        yScaling = ((realY1/self.y1)+(realY2/self.y2))/2.0
        """
        

        #xCoord = (-1*self.mmPxRate*yScaling*(yPx-self.cenY))+self.camX
        #yCoord = (-1*self.mmPxRate*xScaling*(xPx-self.cenX))+self.camY
        """
        ignore scaling for now

        scaling1 = (165.0-float(self.camY))/(-1.0*self.mmPxRate*(79.0-self.cenY))+self.camY
        scaling2 = (-146.0-self.camY)/(-1.0*self.mmPxRate*(377.0-self.cenY))+self.camY
        scaling = (scaling1+scaling2)/2.0
        """

        #print('scaling is: ', scaling)
        print('centroid is: ', centroid)
        print("cenY is : ", self.cenY)
        print("camY is : ", self.camY)

        print(self.mmPxRate)
        xCoord = (self.mmPxRate*(xPx-self.cenX))+self.camX
        #no idea why?
        yCoord = 1.568*((-1.0*self.mmPxRate*(yPx-self.cenY))+self.camY)

        yAdjust = 20.0 * self.mmPxRate * ((self.cenY - yPx) / self.cenY)
        print("yAdj is : ", yAdjust)

        yCoord += yAdjust
        #find the undistorted terms using the values with the calibration points
        return (xCoord, yCoord)
        '''
    
'''
cd = coordClass(1.0 / 1.5, 206.4, 0.0, 320, 240)
print('upper is: ',cd.getCoordinates((334,79)))
print('lower is: ',cd.getCoordinates((330,377)))
'''
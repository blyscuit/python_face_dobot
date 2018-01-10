import math
import cv2
class CoordTransformer:
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
    def __init__(self, mmPxRate, camX, camY, cenX, cenY):
    #def __init__(self, mmPxRate, x1, x2, y1, y2, camX, camY, cenX, cenY):
        #x+ up, x- down, y+ left, y- right
        self.mmPxRate = mmPxRate
        """
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        """
        self.camX = camX
        self.camY = camY
        self.cenX = cenX
        self.cenY = cenY

    def getCoordinates(self, centroid):
        #for testing will consider the centroid as a tuple. However for actual implement will get x and y
        """
        yPx = centroid.y
        xPx = centroid.x
        """
        xPx = centroid[0]
        yPx = centroid[1]

        realY2 = ((self.camX-250)/(self.mmPxRate))+self.cenY
        realY1 = ((self.camX-50)/(self.mmPxRate))+self.cenY
        realX1 = ((self.camX-150)/(self.mmPxRate))+self.cenX
        realX2 = ((self.camX+150)/(self.mmPxRate))+self.cenX
        """
        xScaling = ((realX1/self.x1)+(realX2/self.x2))/2.0
        yScaling = ((realY1/self.y1)+(realY2/self.y2))/2.0
        """
        

        #xCoord = (-1*self.mmPxRate*yScaling*(yPx-self.cenY))+self.camX
        #yCoord = (-1*self.mmPxRate*xScaling*(xPx-self.cenX))+self.camY
        yCoord = (-1*self.mmPxRate*(xPx-self.cenX))+self.camY
        xCoord = (-1*self.mmPxRate*(yPx-self.cenY))+self.camX
        #find the undistorted terms using the values with the calibration points
        return (xCoord, yCoord)

    

#ct = CoordTransformer(1.05, 0,0,0,0, 50, 250, 320, 300)
#print(ct.getCoordinates((200,200)))
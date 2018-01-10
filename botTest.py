import centroid.center_of_shape as cam
from robot_arm.CoordTransformer import coordClass
from robot_arm.arm import dbot

db = dbot()
db.hide()
db.closeDevice()

im_url = 'http://192.168.0.155:4747/mjpegfeed?960x720'

shapes = cam.scan(im_url, False)

cc = coordClass(1.0 / 1.5, 206.4, 10.0, 360, 480)

for s in shapes:
    s['coord'] = cc.getCoordinates(s['center'])
    #db.pickUp(*c)
    #db.place()

print(shapes)

#db.closeDevice()
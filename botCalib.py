import centroid.center_of_shape as cam
from robot_arm.CoordTransformer import coordClass
from robot_arm.arm import dbot

db = dbot()
db.hide()

im_url = 'http://192.168.0.155:4747/mjpegfeed?960x720'

shapes = cam.scan(im_url, False)
cc = coordClass( 1.5, 206.4, 12.5, 480.0, 360.0)

for s in shapes:
    print(s['color'])
    s['coord'] = cc.getCoordinates(s['center'])
    print(s['center'])
    print(s['coord'])
    #print('dobotLevel is: ', s['coord'][0])
    db.hover(*s['coord'])
    #db.pickUp(*s['coord'])
    #db.place()

print(shapes)

db.closeDevice()
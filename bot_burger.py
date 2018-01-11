import centroid.center_of_shape as cam
from robot_arm.CoordTransformer import coordClass
from robot_arm.arm import dbot

def make_burger(ingredient_list):
    db = dbot()
    db.hide()

    im_url = 'http://192.168.0.155:4747/mjpegfeed?960x720'

    shapes = cam.scan(im_url, False)
    cc = coordClass( 1.5, 206.4, 0.0, 480.0, 360.0)

    ingredients = list()

    for s in shapes:
        print(s['color'])
        s['coord'] = cc.getCoordinates(s['center'])
        print(s['center'])
        print(s['coord'])
        if cc.is_in_range(s['coord']):
            ingredients.append(s)

    print(shapes)

    for i in reversed(ingredient_list):
        obj = {}
        for j in ingredients:
            if j['color'] is i:
                obj = j
                db.pickUp(*j['coord'])
                db.place()
                break
        if len(obj) != 0:
            ingredients.remove(obj)
        else:
            print('Out of ingredients')
            return False
            break

    db.hide()
    db.closeDevice()
    return True

'''
sample_burger = ['red', 'green', 'blue']
make_burger(sample_burger)
'''
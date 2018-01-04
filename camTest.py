import numpy as np
import cv2

'''
DroidCam
Make sure PC and Android are in the same network
Run the app on Android
Take note of IP and port displayed in the app
You can try to open the camera stream with your browser on PC
'''

cap = cv2.VideoCapture('http://192.168.137.176:4747/mjpegfeed?960x720')
        

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
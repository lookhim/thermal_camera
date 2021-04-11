import cv2
import numpy as np
from pylepton import Lepton

from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 90
rawCapture = PiRGBArray(camera, size=(640, 40))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    ### camera
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
             
    # show the frame
    cv2.imshow("Frame", image)
                  
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    ### thermal camera
    with Lepton("/dev/spidev0.0") as l:
        a,_= l.capture()

    cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
   
    np.right_shift(a, 8, a) # fit data into 8 bits
    cv2.imwrite('out.jpg', np.uint8(a)) # write it!

    frame = cv2.imread('out.jpg', cv2.IMREAD_COLOR)
  
    ratioImage= 5

    dst2 = cv2.resize(frame, dsize=(0, 0), fx=ratioImage, fy=ratioImage, interpolation=cv2.INTER_LINEAR)
    dst2color = cv2.applyColorMap(dst2, cv2.COLORMAP_JET)
    
    cv2.imshow('Thermal', dst2color)
     
    # if the `q` key was pressed, break from the loop
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()


# Changes I Made To Make This Project Better

import cv2
import numpy as np;
from gpiozero import AngularServo
from time import sleep
# We use this package to remove the jitter from servo motor, in order to make sure there's smooth turning of the motor.
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()

cap= cv2.VideoCapture(0) # Opening the camera
left=AngularServo(26, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000,  pin_factory=factory)
right=AngularServo(25, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000,  pin_factory=factory)

while True:
    ret, frame = cap.read() # Reading first frame
    
    if ret == False:
        break
    cv2.imshow('Imagetest',frame)
    k = cv2.waitKey(1)
    if k != -1:
       break
    #Converting Image to Grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(grayscale,127,255,0)
 
    # calculate moments of binary image
    M = cv2.moments(thresh)
 
    # calculate x,y coordinate of center
    if M["m00"]==0:
        print("no headlight detected")
        left.angle=0
        right.angle=0
        sleep(0.1)
        continue
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print(grayscale.shape)
    print(cX)
    print(cY)
    if 0<cX<=280:
        print("Headlight is on right")
        right.angle=0.285*cX/2
        left.angle=0
        sleep(0.1)
    elif 280<cX<=360:
        print("Headon Collison Detected- Apply Brakes!!!!!!!!!!!!!!")
        left.angle=0
        right.angle=0
        sleep(0.1)
    elif 360<cX<640:
        print("Headlight is on left")
        left.angle=(-90+0.285*(cX-280))/2
        right.angle=0
        sleep(0.1)
    # put text and highlight the center
    cv2.circle(grayscale, (cX, cY), 5, (0, 0, 0), -1)
    cv2.putText(grayscale, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow('Grayscale', grayscale)
    

cap.release()
cv2.destroyAllWindows()



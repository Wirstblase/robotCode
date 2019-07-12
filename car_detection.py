#import libraries of python opencv
import cv2
import time
import serial
import os
import sys
import select
import numpy as np
import thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import socket

#create VideoCapture object and read from video file
#cap = cv2.VideoCapture('cars.mp4')

camera = PiCamera()
camera.resolution=(640,480)
camera.framerate=30
time.sleep(0.1)
rawCapture=PiRGBArray(camera, size=(640,480)) # OPENCV
time.sleep(0.1)

'''
from pivideostream import PiVideoStream
cap = PiVideoStream(resolution=(320,240),framerate=30)
'''

#use trained cars XML classifiers
car_cascade = cv2.CascadeClassifier('cars.xml')

#read until video is completed
for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):  #default = bgr
    
    image=frame.array

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #detect cars in the video
    cars = car_cascade.detectMultiScale(gray, 1.1, 3)
    
    #cv2.imshow("Frame",gray)
    
    #to draw arectangle in each cars 
    for (x,y,w,h) in cars:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)   
        
    cv2.imshow('video', image)
         
    key=cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
      
#release the videocapture object
cap.release()
#close all the frames
cv2.destroyAllWindows()

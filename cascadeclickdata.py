import os
import cv2
import pickle
import numpy as np
import time

# Rectangle is displayed and whole image as well as rectangle is captured now
# Next up is to turn it to black-white pixels

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

framerate = cap.get(5)
count = 0

img_count=0

start_time = time.time()
rr = "p"
os.chdir("C:/Users/Sarvesh/Desktop/HaarCascade/p")
filecount=len(os.listdir(os.getcwd()))

def hand_hist():
    histpath='C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/hist'
    with open(histpath, "rb") as f:
        hist = pickle.load(f)
    return hist

def getframe():

    ret,frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.rectangle(frame,(400,120),(560,320),(0,255,0),3)
    cv2.imshow('frame', frame)

    #since it considers the boundary as max contour hence this removal of boundary pixels
    #since dont know why there is a white border appearing
    frame2 = frame[125:315,405:555]
    frame2=cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame2', frame2)
    return frame2
    


    
    
        

while True:
    gradient=getframe()
    if cv2.waitKey(10) & 0xFF == ord('s'):
        cv2.imwrite(filename='img'+rr+str(int(filecount))+'.jpg',img=gradient)
        print("{} written!".format(filecount))
        filecount+=1
        print(filecount)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
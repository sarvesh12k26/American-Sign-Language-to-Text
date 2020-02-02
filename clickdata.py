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
rr = "switch"
os.chdir("C:/Users/Sarvesh/Desktop/BE-Project/switch")
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
    cont=frame2
    hist=hand_hist()
    cv2.putText(frame,"ASL GESTURES", (50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(250,0,0),2, cv2.LINE_AA)
    
    imghsv=cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    dst=cv2.calcBackProject([imghsv],[0,1],hist,[0,180,0,256],1)
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
    cv2.filter2D(dst,-1,disc,dst)
    blur = cv2.GaussianBlur(dst, (5,5), 0)
    blur = cv2.medianBlur(blur, 7)
    kernel1 = np.ones((5,5),np.uint8)
    blur = cv2.morphologyEx(blur,cv2.MORPH_DILATE,kernel1)

    
    cv2.imshow("Output",dst)
    cv2.imshow("Output1",blur)

    contours, hierarchy = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    back_img=np.ones((cont.shape[0],cont.shape[1]),dtype="uint8")
    back_img=back_img*255
    if len(contours) == 0:
        print("Not Detected")
    else:
        # Given the way we are using the program, the largest external contour should be the hand (largest by area)
        # This will be our segment
        # if max(contours) is True:
        #     contours.remove(max(contours))
        hand_segment = max(contours, key=cv2.contourArea)
        cv2.drawContours(back_img, [hand_segment], -1, (0, 0, 0),-1)
        cont=cv2.cvtColor(cont,cv2.COLOR_BGR2GRAY)
        cv2.bitwise_or(cont,back_img,dst=back_img)
        cv2.imshow("bi",back_img)

        frame2=back_img
        kernel2 = np.ones(shape=(3,3),dtype=np.float32)/4
        frame2=cv2.filter2D(frame2,-1,kernel2)
        cv2.imshow('filter',frame2)
        # frame2=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        kernel3 = np.ones((3,3),np.uint8)
        edgedhand = cv2.morphologyEx(frame2,cv2.MORPH_GRADIENT,kernel3)
        cv2.imshow('image1',edgedhand)

        return edgedhand
        

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
import numpy as np
import cv2

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.rectangle(frame,(400,120),(560,320),(0,255,0),3)
    cv2.imshow('frame', frame)

    frame2 = frame[120:320,400:560]
    cv2.imshow('frame2', frame2)

    ##HaarCascade Testing
    hand_cascade=cv2.CascadeClassifier('cascade5.xml')

    ###detect palm
    hand_img=frame2.copy()
    hand_img=cv2.cvtColor(hand_img,cv2.COLOR_BGR2GRAY)
    hand_rects=hand_cascade.detectMultiScale(hand_img)

    max_x , max_y, max_x1, max_y1 = 1000,1000,0,0

    for(x,y,w,h) in hand_rects:
        if x < max_x:
            max_x = x
        if y < max_y:
            max_y = y
        if x+w > max_x1:
            max_x1 = x+w
        if y+h > max_y1:
            max_y1 = y+h
        # cv2.rectangle(hand_img,(x,y),(x+w,y+h),(255,255,255),2)


    cv2.rectangle(hand_img,(max_x,max_y),(max_x1,max_y1),(255,255,0),3)

    cv2.imshow('output',hand_img)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
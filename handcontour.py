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

    frame2 = frame[123:317,403:557]

    ###Filter 2D blurring
    kernel = np.ones(shape=(3,3),dtype=np.float32)/4
    # kernel[1,1]=kernel[1,1]*4
    frame2=cv2.filter2D(frame2,-1,kernel)

    # frame2=cv2.GaussianBlur(frame2,(11,11),5,5)
    cv2.imshow('image',frame2)

    ###Morphology Gradient
    frame2=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    kernel1 = np.ones((9,9),np.uint8)
    gradient = cv2.morphologyEx(frame2,cv2.MORPH_GRADIENT,kernel1)
    

    ###Trying to find hand contours
    '''
    Extremely inaccurate
    need to find a lot better implementation
    '''
    contours, hierarchy = cv2.findContours(gradient, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt=contours[max_index]

    x,y,w,h = cv2.boundingRect(cnt)
    print(x,y,w,h)
    cv2.rectangle(gradient,(x,y),(x+w,y+h),255,2)    
    cv2.imshow('image1',gradient)
    # cv2.imshow('largest contour ',final1)


    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    
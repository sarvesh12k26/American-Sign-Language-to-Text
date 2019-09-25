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

    kernel = np.ones(shape=(3,3),dtype=np.float32)/4
    frame2=cv2.filter2D(frame2,-1,kernel)
    cv2.imshow('image',frame2)

    frame2=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    kernel1 = np.ones((9,9),np.uint8)
    gradient = cv2.morphologyEx(frame2,cv2.MORPH_GRADIENT,kernel1)
    cv2.imshow('image1',gradient)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


###############
# img = cv2.imread('gesture2.jpg')
# cv2.imshow('image',img)
# cv2.waitKey(0)

# kernel = np.ones(shape=(3,3),dtype=np.float32)/4

# img=cv2.filter2D(img,-1,kernel)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # img = cv2.threshold(img, 175, 255, cv2.THRESH_BINARY)[1]
# kernel1 = np.ones((9,9),np.uint8)
# gradient = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel1)
# # img = cv2.GaussianBlur(img,(9,9),10)

# cv2.imshow('image1',gradient)
# cv2.waitKey(0)
    
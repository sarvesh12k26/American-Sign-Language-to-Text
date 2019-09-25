import numpy as np
import cv2

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

accumulated_weight = 0.5

roi_top = 120
roi_bottom = 320
roi_right = 560
roi_left = 400

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.rectangle(frame,(400,120),(560,320),(0,255,0),3)
    cv2.imshow('frame', frame)

    frame2 = frame[120:320,400:560]
    frame3=frame2
    ###These next two lines can be tweaked for more noise removal
    kernel = np.ones(shape=(3,3),dtype=np.float32)/4
    frame2=cv2.filter2D(frame2,-1,kernel)
    # frame2=cv2.medianBlur(frame2,5)
    cv2.imshow('image',frame2)

    frame2=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray',frame2)
    kernel1 = np.ones((7,7),np.uint8)
    gradient=frame2
    # gradient = cv2.morphologyEx(frame2,cv2.MORPH_GRADIENT,kernel1)
    ret,gradient = cv2.threshold(gradient, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU);
    ###These next two lines can be tweaked for foreground features
    gradient=cv2.morphologyEx(gradient,cv2.MORPH_CLOSE,kernel1)
    ###This line can be commented if background noise is less and hence would get more foreground features
    gradient=cv2.erode(gradient,kernel*10,iterations=1)

    contours, hierarchy = cv2.findContours(gradient.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("Gone for a duck")
    else:
        # Given the way we are using the program, the largest external contour should be the hand (largest by area)
        # This will be our segment
        hand_segment = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame3, [hand_segment], -1, (255, 255, 255),2)
        print("A Hundred to Savour")

    cv2.imshow('image1',gradient)
    cv2.imshow('test',frame3)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    
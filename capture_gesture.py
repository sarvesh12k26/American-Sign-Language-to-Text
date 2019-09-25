import os
import cv2

# Rectangle is displayed and whole image as well as rectangle is captured now
# Next up is to turn it to black-white pixels

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

count = 0

#Reference Frame
ret,first= cap.read()
frame = cv2.flip(first,1)
frame_rect = frame[120:320,400:560]
first_gray=cv2.cvtColor(frame_rect, cv2.COLOR_BGR2GRAY)

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.rectangle(frame,(400,120),(560,320),(0,255,0),3)
    cv2.imshow('frame', frame)

    frame2 = frame[120:320,400:560]
    im_gray=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    #This is the code for background elimination
    #Uses the first frame as reference to subtract
    #Not working great though need further work
    backSub = cv2.GaussianBlur(im_gray, (21,21), 0)
    difference = cv2.absdiff(backSub, first_gray)
    thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
    # thresh = cv2.dilate(thresh, None, iterations=2)
    cv2.imshow('thresh',thresh)

    # if(count%24==0):
        # this writes the whole image
        # cv2.imwrite("frame%d.jpg" % count, frame)
        # this would write only the rectangular region
        # cv2.imwrite("rect%d.jpg" % count, im_bw)
        # this writes the background masked image
        # cv2.imwrite("masked%d.jpg" % count, fgMask)
    count+=1

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
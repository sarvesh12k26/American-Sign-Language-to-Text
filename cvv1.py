
#Work with code in inverted commas
import cv2
import numpy as np

# Connects to your computer's default camera
cap = cv2.VideoCapture(0)


# Automatically grab width and height from video feed
# (returns float which we need to convert to integer for later on!)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    
    # Capture frame-by-frame
    ret, frame = cap.read()

    temp = frame.copy()
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ############$$$$$
    cv2.rectangle(gray,pt1=(100,75),pt2=(275,325),color=(0,0,255),thickness=3)

    temp = gray[75:326,100:276]

    #temp = cv2.blur(temp,ksize=(5,5))
    #temp = cv2.GaussianBlur(temp, (5, 5), 0)
    

    #ret, temp = cv2.threshold(temp,165,255,cv2.THRESH_BINARY)
    '''
    #This is  Sobel uncomment this piece of code
    sobelX = cv2.Sobel(temp, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(temp, cv2.CV_64F, 0, 1)

    sobelX = np.uint8(np.absolute(sobelX))
    sobelY = np.uint8(np.absolute(sobelY))
    sobelCombined = cv2.bitwise_xor(sobelX, sobelY)

    '''
    #ret, sobelCombined = cv2.threshold(sobelCombined,75,255,cv2.THRESH_BINARY)

    '''
    #This is Canny edge detection
    tui=0.33
    med = np.median(temp) 
    lower = int(max(0, (1.0 - tui) * med))
    upper = int(min(255, (1.0 + tui) * med))
    edged = cv2.Canny(temp, lower, upper)

    '''
    #edges = cv2.Canny(image=temp, threshold1=lower , threshold2=upper)
    
    #temp = cv2.blur(temp,ksize=(1,1))
    
    #atg = cv2.adaptiveThreshold(temp,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,15,6)
    
    #Change variable apropriatley
    #Result Frame
    cv2.imshow('frame2',edged)
    
    ############$$$$$
    # Display the resulting frame
    cv2.imshow('frame',gray)
    
    # This command let's us quit with the "q" button on a keyboard.
    # Simply pressing X on the window won't work!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy the windows
cap.release()
cv2.destroyAllWindows()

import os
import cv2
import pickle
import numpy as np
from keras.models import model_from_json
import NLPmodule as nlpmod

# Rectangle is displayed and whole image as well as rectangle is captured now
# Next up is to turn it to black-white pixels

# deserialize model and load weights
json_file1=open("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/classifier_new3_mod1.json",'r')
loaded_model_json=json_file1.read()
json_file1.close()

classifier1 = model_from_json(loaded_model_json)
classifier1.load_weights("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/asl_new3_mod1.h5")

# Used for numbers only
# classifier2.load_weights("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/asl_new_mod2.h5")

# deserialize model and load weights for numbers
json_file2=open("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/classifier_new2_mod2.json",'r')
loaded_model_json2=json_file2.read()
json_file2.close()

classifier2 = model_from_json(loaded_model_json2)
classifier2.load_weights("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/asl_new2_mod2.h5")


# CV2 process starts
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

count = 0

# 0 for letters; 1 for numbers
mode = 0
pred_text=''
pred_word=''
pred_list=[]
letter_lookup={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z',26:' ',27:'&',28:'#'}
number_lookup={0:'1',1:'2',2:'3',3:'4',4:'5',5:'6',6:'7',7:'8',8:'9',9:'0',10:'#'}
def hand_hist():
    with open("hist", "rb") as f:
        hist = pickle.load(f)
    return hist

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.rectangle(frame,(400,120),(560,320),(0,255,0),3)
    cv2.imshow('frame', frame)

    #since it considers the boundary as max contour hence this removal of boundary pixels
    #since dont know why there is a white border appearing
    frame2 = frame[125:315,405:555]
    cont=frame2
    hist=hand_hist()

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
        # print("Not Detected")
        pred_list = []
    else:
        
        hand_segment = max(contours, key=cv2.contourArea)
        cv2.drawContours(back_img, [hand_segment], -1, (0, 0, 0),-1)
        cont=cv2.cvtColor(cont,cv2.COLOR_BGR2GRAY)
        cv2.bitwise_or(cont,back_img,dst=back_img)
        cv2.imshow("bi",back_img)
        
        ### Code when lighting is great
        frame2=back_img
        kernel2 = np.ones(shape=(3,3),dtype=np.float32)/4
        frame2=cv2.filter2D(frame2,-1,kernel2)
        cv2.imshow('filter',frame2)
        # frame2=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        kernel3 = np.ones((3,3),np.uint8)
        gradient = cv2.morphologyEx(frame2,cv2.MORPH_GRADIENT,kernel3)
        cv2.imshow('image1',gradient)

        # predict character using the classifier model
        gradient2=cv2.resize(gradient,(128,128))
        gradient2=gradient2.reshape(1,128,128,1)
        
        if mode == 0:       
            out=classifier1.predict_classes(gradient2)
            pred_var = letter_lookup[int(out)]
            print(pred_var)
            pred_list.append(pred_var)

        elif mode == 1:
            out=classifier2.predict_classes(gradient2)
            pred_var = number_lookup[int(out)]
            print(pred_var)
            pred_list.append(pred_var)

        if len(pred_list) == 75:
            max_char = max(pred_list, key=pred_list.count)
            print(pred_list)
            # if mode == 0:
            #     max_char = letter_lookup[max_ind]
            # elif mode == 1:
            #     max_char = number_lookup[max_ind]

            if max_char == '#':
                mode = (mode + 1) % 2
                print('#################....... MODE CHANGE .......##############')
            else:
                if max_char == ' ':
                    if not pred_word.isnumeric():
                        pred_word = nlpmod.correction(pred_word.lower())
                        print('Correction Done')
                    pred_text+=pred_word
                    pred_text+=' '
                    pred_word=''
                    print('Corrected : ............'+pred_text+'............')
                else:
                    pred_word += max_char
                    print('..........'+pred_word+'...........')
                    pred_list = []



    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
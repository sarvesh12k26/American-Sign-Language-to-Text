from utils import detector_utils as detector_utils
import cv2, os, pickle
import tensorflow as tf
import datetime
import numpy as np
from keras.models import model_from_json
import NLPmodule as nlpmod
from spellchecker import SpellChecker

spell = SpellChecker()

detection_graph, sess = detector_utils.load_inference_graph()

# deserialize model and load weights
json_file1=open("C:/Users/Sarvesh/Desktop/JavaPracIMP/ASL-Final/classifier_new3_mod1.json",'r')
loaded_model_json=json_file1.read()
json_file1.close()

classifier1 = model_from_json(loaded_model_json)
classifier1.load_weights("C:/Users/Sarvesh/Desktop/JavaPracIMP/ASL-Final/asl_new6_mod1.h5")

# deserialize model and load weights for numbers
json_file2=open("C:/Users/Sarvesh/Desktop/JavaPracIMP/ASL-Final/classifier_new2_mod2.json",'r')
loaded_model_json2=json_file2.read()
json_file2.close()

classifier2 = model_from_json(loaded_model_json2)
classifier2.load_weights("C:/Users/Sarvesh/Desktop/JavaPracIMP/ASL-Final/asl_new3_mod2.h5")

count = 0
# 0 for letters; 1 for numbers
mode = 0
pred_text=''
pred_word=''
pred_list=[]

def hand_hist():
    with open("hist", "rb") as f:
        hist = pickle.load(f)
    return hist

def aslrun(frame2):
    letter_lookup={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z',26:' ',27:'&',28:'#'}
    number_lookup={0:'1',1:'2',2:'3',3:'4',4:'5',5:'6',6:'7',7:'8',8:'9',9:'0',10:'#'}

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

    _, contours, hierarchy = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    back_img=np.ones((cont.shape[0],cont.shape[1]),dtype="uint8")
    back_img=back_img*255

    if len(contours) == 0:
        print("Not Detected")
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

        elif mode == 1:
            out=classifier2.predict_classes(gradient2)
            pred_var = number_lookup[int(out)]

        return pred_var

def nlpcode(pred_var,mode,pred_text,pred_word,pred_list):
    if mode == 0:
        print(pred_var)
        pred_list.append(pred_var)

    elif mode == 1:
        print(pred_var)
        pred_list.append(pred_var)

    if len(pred_list) == 30:
        max_char = max(pred_list, key=pred_list.count)
        print(pred_list)
        if max_char == '#':
            mode = (mode + 1) % 2
            print('#################....... MODE CHANGE .......##############')
        else:
            if max_char == ' ':
                if not pred_word.isnumeric():
                    # pred_word = nlpmod.correction(pred_word.lower())
                    pred_word = spell.correction(pred_word.lower())
                    print('Correction Done')
                pred_text+=pred_word
                pred_text+=' '
                pred_word=''
                print('Corrected : ............'+pred_text+'............')
            else:
                pred_word += max_char
                print('..........'+pred_word+'...........')
                pred_list = []
        pred_list = []

    return mode,pred_text,pred_word,pred_list


if __name__ == '__main__':

    score_thresh = 0.4
    fps = 1
    video_source = 0
    width = 480
    height = 640
    display = 1
    print(video_source)

    mode = 0
    pred_text=''
    pred_word=''
    pred_list=[]

    cap = cv2.VideoCapture(video_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    start_time = datetime.datetime.now()
    num_frames = 0
    im_width, im_height = (cap.get(3), cap.get(4))
    # max number of hands we want to detect/track
    num_hands_detect = 1

    cv2.namedWindow('Single-Threaded Detection', cv2.WINDOW_NORMAL)

    while True:
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        ret, image_np = cap.read()

        image_np = cv2.flip(image_np, 1)
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            image_np_copy = image_np
        except:
            print("Error converting to RGB")

        # actual detection
        boxes, scores = detector_utils.detect_objects(image_np, detection_graph, sess)

        # draw bounding boxes
        (bottom,top,left,right) = detector_utils.draw_box_on_image(num_hands_detect, score_thresh, scores, boxes, im_width, im_height, image_np)
        # print(bottom,top,left,right)

        # Calculate Frames per second (FPS)
        num_frames += 1
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = num_frames / elapsed_time

        if (display > 0):
            # Display FPS on frame
            if (fps > 0):
                detector_utils.draw_fps_on_image("FPS : " + str(int(fps)), image_np)

            if(bottom!=0 and top!=0 and left!=0 and right!=0):
                bottom=int(bottom);top=int(top);left=int(left);right=int(right)
                bottom+=5;top-=10;left-=10;right+=10;
                frame2 = image_np[top:bottom,left:right]
                frame2 = cv2.cvtColor(frame2,cv2.COLOR_RGB2BGR)
                cv2.imshow('temp',frame2)

                p1 = (int(left), int(top))
                p2 = (int(right), int(bottom))
                cv2.rectangle(image_np_copy, p1, p2, (77, 255, 9), 3, 1)
                pred_var = aslrun(frame2)

                # Now comes the further NLP code
                mode, pred_text, pred_word, pred_list = nlpcode(pred_var,mode,pred_text,pred_word,pred_list)

            cv2.imshow('Single-Threaded Detection', cv2.cvtColor(image_np_copy, cv2.COLOR_RGB2BGR))

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        else:
            print("frames processed: ",  num_frames,
                  "elapsed time: ", elapsed_time, "fps: ", str(int(fps)))

cap.release()
cv2.destroyAllWindows()

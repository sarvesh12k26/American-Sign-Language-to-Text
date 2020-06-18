# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'capture.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from utils import detector_utils as detector_utils
import cv2
import datetime
import sys
import pickle
import numpy as np
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QFont
from spellchecker import SpellChecker
import NLPmodule as nlpmod

import speech_recognition as sr
import keyboard

from PyQt5 import QtCore, QtGui, QtWidgets
import os

import pyttsx3

detection_graph, sess = detector_utils.load_inference_graph()

import keras
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
hog_w=True
hog_sw=True
hog_l=True
hog_sp=True
hog_mod=True
cap_c=True
count = 0
# 0 for letters; 1 for numbers
mode = 0
pred_text=''
pred_word=''
pred_list=[]

word_clear=0

def hand_hist():
        with open("hist", "rb") as f:
            hist = pickle.load(f)
        return hist

def aslrun(frame2,classifier1,classifier2,mode):

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

    #cv2.imshow("Output",dst)
    #cv2.imshow("Output1",blur)

    _,contours, hierarchy = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    back_img=np.ones((cont.shape[0],cont.shape[1]),dtype="uint8")
    back_img=back_img*255

    if len(contours) == 0:
        print("Not Detected")
    else:

        hand_segment = max(contours, key=cv2.contourArea)
        cv2.drawContours(back_img, [hand_segment], -1, (0, 0, 0),-1)
        cont=cv2.cvtColor(cont,cv2.COLOR_BGR2GRAY)
        cv2.bitwise_or(cont,back_img,dst=back_img)
        #cv2.imshow("bi",back_img)

        ### Code when lighting is great
        frame2=back_img
        kernel2 = np.ones(shape=(3,3),dtype=np.float32)/4
        frame2=cv2.filter2D(frame2,-1,kernel2)
        #cv2.imshow('filter',frame2)
        # frame2=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        kernel3 = np.ones((3,3),np.uint8)
        gradient = cv2.morphologyEx(frame2,cv2.MORPH_GRADIENT,kernel3)
        #cv2.imshow('image1',gradient)
        gradient2=cv2.resize(gradient,(128,128))
        gradient2=gradient2.reshape(1,128,128,1)

        if mode == 0:
            out=classifier1.predict_classes(gradient2)
            pred_var = letter_lookup[int(out)]

        elif mode == 1:
            out=classifier2.predict_classes(gradient2)
            pred_var = number_lookup[int(out)]

        return pred_var

def nlpcode(pred_var,mode,pred_text,pred_word,pred_list,hog_w,hog_sw,hog_l,engine,hog_mod):
    cf=0
    if mode == 0:
        print(pred_var)
        pred_list.append(pred_var)

    elif mode == 1:
        print(pred_var)
        pred_list.append(pred_var)

    if len(pred_list) == 20:
        max_char = max(pred_list, key=pred_list.count)
        print(pred_list)
        if max_char == '#':
            mode = (mode + 1) % 2
            if(mode==0):
                hog_mod.setText("Mode:"+"\n"+"Alphabet"+"\n"+"(Alphabets,Space,"+"\n"+"Switch,End sign)")
            else:
                hog_mod.setText("Mode:"+"\n"+"Number"+"\n"+"(Numbers,End Sign)")
            print(mode)
            print('#################....... MODE CHANGE .......##############')
        else:
            if max_char == ' ':
                #pred_text=''
                if not pred_word.isnumeric():
                    #pred_word = nlpmod.correction(pred_word.lower())
                    #pred_word = TextBlob(pred_word.lower()).correct()
                    #pred_word=str(pred_word)
                    pred_word = SpellChecker().correction(pred_word.lower())
                    print('Correction Done')
                pred_text+=pred_word
                pred_text+=' '
                hog_sw.setText("Corrected Word:"+"\n"+pred_word)
                pred_word=''
                print('Corrected : ............'+pred_text+'............')
            elif max_char == '&':
                hog_w.setText("Recognized Word:"+"\n"+pred_word)
                #pred_word = nlpmod.correction(pred_word.lower())
                #pred_word = TextBlob(pred_word.lower()).correct()
                #pred_word=str(pred_word)
                pred_word = SpellChecker().correction(pred_word.lower())
                pred_text+=pred_word
                print('..........'+pred_word+'...........')
                hog_sw.setText("Corrected Word:"+"\n"+pred_word)
                print(pred_text)
                engine.say(str(pred_text))
                engine.runAndWait()
                hog_l.setText("Sentence: "+pred_text)
                pred_word=''
                pred_text='' 
                pred_list = []
                cf=1
            else:
                pred_word += max_char
                print('..........'+pred_word+'...........')
                hog_w.setText("Recognized Word:"+"\n"+pred_word)
                pred_list = []
        pred_list = []
    hog_l.setText("Sentence: "+pred_text)
    return mode,pred_text,pred_word,pred_list

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    '''
    def __init__(self, myvar, parent=None):
        QThread.__init__(self,parent)
        self.myvar = myvar
    '''
    def run(self):
        global hog_w,hog_sw,hog_l,cap_c,word_clear,hog_mod
        engine = pyttsx3.init()
        classifier1 = Sequential()
        classifier1.add(Convolution2D(64, 3, 3, input_shape = (128, 128, 1), activation = 'relu'))
        classifier1.add(MaxPooling2D(pool_size = (2, 2)))
        classifier1.add(Convolution2D(32, 3, 3, activation = 'relu'))
        classifier1.add(MaxPooling2D(pool_size = (2, 2)))
        classifier1.add(Convolution2D(32, 3, 3, activation = 'relu'))
        classifier1.add(MaxPooling2D(pool_size = (2, 2)))
        classifier1.add(Flatten())
        classifier1.add(Dense(output_dim = 2048, activation = 'relu'))
        classifier1.add(Dense(output_dim = 128, activation = 'relu'))
        classifier1.add(Dense(output_dim = 29, activation = 'softmax'))
        classifier1.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
        classifier1.load_weights("C:/Users/Sarvesh/Desktop/JavaPracIMP/ui (2)/ui/asl_new6_mod1.h5")

        classifier2 = Sequential()
        classifier2.add(Convolution2D(32, 3, 3, input_shape = (128, 128, 1), activation = 'relu'))
        classifier2.add(MaxPooling2D(pool_size = (2, 2)))
        classifier2.add(Convolution2D(32, 3, 3, activation = 'relu'))
        classifier2.add(MaxPooling2D(pool_size = (2, 2)))
        classifier2.add(Flatten())
        classifier2.add(Dense(output_dim = 128, activation = 'relu'))
        classifier2.add(Dense(output_dim = 11, activation = 'softmax'))
        classifier2.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
        classifier2.load_weights("C:/Users/Sarvesh/Desktop/JavaPracIMP/ui (2)/ui/asl_new4_mod2.h5")
        
        score_thresh = 0.4
        fps = 1
        video_source = 0
        width = 480
        height = 640
        display = 1

        mode = 0
        pred_text=''
        pred_word=''
        pred_list=[]

        cap = cv2.VideoCapture(video_source)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap_c=cap
        start_time = datetime.datetime.now()
        num_frames = 0
        im_width, im_height = (cap.get(3), cap.get(4))
        # max number of hands we want to detect/track
        num_hands_detect = 1

        #cv2.namedWindow('Single-Threaded Detection', cv2.WINDOW_NORMAL)

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
                #if (fps > 0):
                    #detector_utils.draw_fps_on_image("FPS : " + str(int(fps)), image_np)
                if(bottom!=0 and top!=0 and left!=0 and right!=0):
                    bottom=int(bottom);top=int(top);left=int(left);right=int(right)
                    bottom+=5;top-=5;left-=5;right+=5;
                    frame2 = image_np[top:bottom,left:right]
                    frame2 = cv2.cvtColor(frame2,cv2.COLOR_RGB2BGR)
                    #cv2.imshow('temp',frame2)

                    p1 = (int(left), int(top))
                    p2 = (int(right), int(bottom))
                    cv2.rectangle(image_np_copy, p1, p2, (77, 255, 9), 3, 1)
                    if keyboard.is_pressed('e'):
                        pred_var = '&'
                    else:
                        pred_var = aslrun(frame2,classifier1,classifier2,mode)
                    if word_clear==1:
                        word_clear=0
                        pred_word=''
                        pred_list=[]

                    # Now comes the further NLP code
                    mode, pred_text, pred_word, pred_list = nlpcode(pred_var,mode,pred_text,pred_word,pred_list,hog_w,hog_sw,hog_l,engine,hog_mod)
                    '''
                    if cv2.waitKey(10) & 0xFF == ord('s'):
                        cv2.imwrite(filename='img'+rr+str(int(filecount))+'.jpg',img=gradient)
                        print("{} written!".format(filecount))
                        filecount+=1
                        print(filecount)
                    '''
                    #cv2.imshow('Single-Threaded Detection', cv2.cvtColor(image_np_copy, cv2.COLOR_RGB2BGR))
                    #hog_w.setText(pred_word)
                else:
                    pred_list=[]
                h, w, ch = image_np_copy.shape
                image_np_copy=cv2.cvtColor(image_np_copy, cv2.COLOR_RGB2BGR)
                bytesPerLine = ch * w
                convertToQtFormat = QImage(image_np_copy.data, w, h, bytesPerLine, QImage.Format_BGR888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                '''
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                #hog.label_2.setText("")
                self.changePixmap.emit(p)
                '''

class Ui_Dialog3(QWidget):

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.commframe.setPixmap(QPixmap.fromImage(image))

    def camera(self,event):
        print("camera")
        #wrtie code to run handhist framw camera
    
    def speaker(self):
        global hog_sp
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak Anything :")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                hog_sp.setText(text)
            except:
                print("Sorry could not recognize what you said")

    def clear_text(self):
        global hog_w
        global hog_sw
        global word_clear
        word_clear=1
        hog_w.setText("Recognized Word:")
        hog_sw.setText("Corrected Word:")

    def setupUi(self, Dialog):
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(852, 607)
        Dialog.setStyleSheet("background-color: rgb(79, 79, 79);")
        
        font = QFont()
        font.setWeight(10)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 10, 315, 31))
        self.label.setStyleSheet("font: 63 20pt \"Segoe UI Semibold\";\n"
"color: rgb(73, 173, 188);")
        self.label.setObjectName("label")
        self.label.setText("ASL Communication")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(400, 10, 80, 40))
        self.pushButton.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 12pt \"Segoe UI Semibold\";border-radius: 4px;")
        self.pushButton.setObjectName("pushButon")
        self.pushButton.setText("Speak")
        self.pushButton.clicked.connect(self.speaker)

        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setText("")
        self.label_6.setGeometry(QtCore.QRect(490, 10, 350, 40))
        self.label_6.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 10pt \"Segoe UI Semibold\";border-radius: 4px;\n"
"")
        self.label_6.setObjectName("label_6")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 51, 41))
        self.label_2.setStyleSheet("image: url(:/newbie/aslnew.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.delete_word = QtWidgets.QPushButton(Dialog)
        self.delete_word.setGeometry(QtCore.QRect(10, 510, 65, 70))
        #self.label_3.setStyleSheet("image: url(:/newbie/pg.png);\n""")
        self.delete_word.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 9pt \"Segoe UI Semibold\";border-radius: 4px;")
        self.delete_word.setText("Delete \n Current \n Word")
        self.delete_word.setObjectName("delete_word")
        self.delete_word.clicked.connect(self.clear_text)

        self.commframe = QtWidgets.QLabel(Dialog)
        self.commframe.setGeometry(QtCore.QRect(16, 62, 650, 431))
        self.commframe.setFrameShape(QtWidgets.QFrame.Panel)
        self.commframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.commframe.setText("")
        self.commframe.setObjectName("commframe")
        self.commframe.mousePressEvent= self.camera
        self.sentence = QtWidgets.QLabel(Dialog)
        self.sentence.setGeometry(QtCore.QRect(80, 510, 761, 71))
        self.sentence.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63  10pt \"Segoe UI Semibold\";border-radius: 4px;\n"
"")
        self.sentence.setObjectName("sentence")
        self.sentence.setText("Sentence:")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setText("Recognized Word:")
        self.label_4.setGeometry(QtCore.QRect(680, 60, 160, 160))
        self.label_4.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 10pt \"Segoe UI Semibold\";border-radius: 4px;\n"
"")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setText("Corrected Word:")
        self.label_5.setGeometry(QtCore.QRect(680, 230, 160, 160))
        self.label_5.setStyleSheet(" background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 10pt \"Segoe UI Semibold\";border-radius: 4px;\n"
"")
        self.label_5.setObjectName("label_5")

        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setText("Mode:"+"\n"+"Alphabet"+"\n"+"(Alphabets,Space,"+"\n"+"Switch,End sign)")
        self.label_7.setGeometry(QtCore.QRect(680, 400, 160, 100))
        self.label_7.setStyleSheet(" background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 10pt \"Segoe UI Semibold\";border-radius: 4px;\n"
"")
        self.label_7.setObjectName("label_7")
        
        global hog_w,hog_sw,hog_l,hog_sp,hog_mod
        hog_sp=self.label_6
        hog_w=self.label_4
        hog_sw=self.label_5
        hog_mod=self.label_7
        hog_l=self.sentence
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        #self.retranslateUi(Dialog)
        #QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ASL Communication"))
        self.sentence.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Sentence display</p></body></html>"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Word </span></p><p align=\"center\"><span style=\" font-weight:600;\">Formed</span></p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Spell</p><p align=\"center\">Correct</p><p align=\"center\">word</p></body></html>"))
        #self.sentence.setText(_translate("Dialog", str("    ") + "write here the text to be set")) #set the sentence to be displayed
        #self.label_4.setText(_translate("Dialog", str("    ") + "write here the text to be set")) #set word formed
        #self.label_5.setText(_translate("Dialog", str("    ") + "write here the text to be set")) #set spelled correct word
        
import newtest_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog3 = QtWidgets.QDialog()
    Dialog3.setWindowTitle("Capture")
    ui = Ui_Dialog3()
    ui.setupUi(Dialog3)
    Dialog3.show()
    #cap_c.release()
    sys.exit(app.exec_())


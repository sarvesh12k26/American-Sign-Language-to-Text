# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'handhistframe.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import cv2
import numpy as np
import pickle
import keyboard
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets

def build_squares(img):
    x, y, w, h = 420, 140, 10, 10
    d = 10
    imgCrop = None
    crop = None
    for i in range(10):
        for j in range(5):
            if np.any(imgCrop == None):
                imgCrop = img[y:y+h, x:x+w]
            else:
                imgCrop = np.hstack((imgCrop, img[y:y+h, x:x+w]))
            #print(imgCrop.shape)
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)
            x+=w+d
        if np.any(crop == None):
            crop = imgCrop
        else:
            crop = np.vstack((crop, imgCrop)) 
        imgCrop = None
        x = 420
        y+=h+d
    return crop

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    '''
    def __init__(self, myvar, parent=None):
        QThread.__init__(self,parent)
        self.myvar = myvar
    '''
    def run(self):
        global hog
        cam = cv2.VideoCapture(1)
        if cam.read()[0]==False:
            cam = cv2.VideoCapture(0)
        x, y, w, h = 300, 100, 300, 300
        flagPressedC, flagPressedS = False, False
        imgCrop = None
        while True:
            img = cam.read()[1]
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (640, 480))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                print('You Pressed A Key!')
            keypress = cv2.waitKey(1)
            if keyboard.is_pressed('s'):        
                hsvCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2HSV)
                #cv2.imshow('HSV',hsvCrop)
                flagPressedC = True
                hist = cv2.calcHist([hsvCrop], [0, 1], None, [180, 256], [0, 180, 0, 256])
                # cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
            '''
            elif keypress == ord('s'):
                flagPressedS = True 
                break
            '''
            if flagPressedC:    
                dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)
                dst1 = dst.copy()
                disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
                cv2.filter2D(dst,-1,disc,dst)
                #cv2.imshow("Filter2D",dst)
                blur = cv2.GaussianBlur(dst, (11,11), 0)
                blur = cv2.medianBlur(blur, 15)
                # ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                # thresh = cv2.merge((thresh,thresh,thresh))
                # cv2.imshow("res", res)
                cv2.imshow("Thresh", blur)
            if keyboard.is_pressed('x'):  # if key 'q' is pressed 
                flagPressedC=False
                cv2.destroyAllWindows()
            if not flagPressedS:
                imgCrop = build_squares(img)
            #cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)   
            self.changePixmap.emit(p)
            if flagPressedC:
                with open("hist", "wb") as f:
                    pickle.dump(hist, f)
            #cv2.imshow("Set hand histogram", img)
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

class Ui_Dialog4(QWidget):

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.histframe.setPixmap(QPixmap.fromImage(image))

    def camera(self,event):
        print("camera")
        #wrtie code to run handhist framw camera
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(730, 559)
        Dialog.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.instructions1 = QtWidgets.QLabel(Dialog)
        self.instructions1.setGeometry(QtCore.QRect(380, 0, 350, 50))
        self.instructions1.setStyleSheet("background-color: rgb(84, 162, 177,0.5);\n"
";\n"
"font: 63 8pt \"Segoe UI Semibold\";border-radius: 4px;")
        self.instructions1.setText("Press 'S' to save and press 'X' to close testing window \n Make sure your hand is all white in testing window ")
        self.instructions1.setObjectName("instructions1")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 10, 310, 41))
        self.label.setStyleSheet("font: 63 20pt \"Segoe UI Semibold\";\n"
"color: rgb(73, 173, 188);")
        self.label.setObjectName("label")
        self.label.setText("ASL Communication")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 51, 41))
        self.label_2.setStyleSheet("image: url(:/new/aslnew.png);\n"
"")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.histframe = QtWidgets.QLabel(Dialog)
        self.histframe.setGeometry(QtCore.QRect(16, 62, 701, 471))
        self.histframe.setFrameShape(QtWidgets.QFrame.Panel)
        self.histframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.histframe.setText("")
        self.histframe.setObjectName("histframe")
        #self.histframe.mousePressEvent= self.camera

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        #self.retranslateUi(Dialog)
        #QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.instructions1.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Instructions: <span style=\" font-weight:600;\">Press \'q\' to exit or press \'s\' to save</span></p></body></html>"))
        self.label.setText(_translate("Dialog", "ASL Communication"))

import test_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog4 = QtWidgets.QDialog()
    ui = Ui_Dialog4()
    ui.setupUi(Dialog4)
    Dialog4.show()
    sys.exit(app.exec_())


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signup.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql
from asl import Ui_Dialog
from homepage import Ui_Dialog1
import os
class Ui_Dialog2(object):  #class name Ui_Dialog2
    #running loginfile
    def loginlink(self):
        print('in')
        
        #os.system('python asl.py')
        #os.close(self)
       
        print("open")
        self.window=QtWidgets.QDialog()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()
        Dialog2.hide()
    #pass username  post signup to homepage and close current window   
    def openWindow(self,username): 
        print("open")
        self.window=QtWidgets.QDialog()
        self.message = username
        self.ui=Ui_Dialog1(self.message)
        self.ui.setupUi(self.window)
        self.window.show()
        Dialog2.hide()
        
    def signup(self):
        username=self.lineEdit.text()
        password=self.lineEdit_2.text()
        email=self.lineEdit_3.text()
        if(self.radioButton.isChecked()):
            gender="Female"
        else:
            gender="Male"

        print(gender)
        #connection checking
        try:
            conn = pymysql.connect(host='localhost' ,port= 3305,user='root',password='',db='sample')
        except pymysql.MySQLError as e:
            print(e)
            sys.exit()
        finally:
            print("done")
        cur=conn.cursor()
        query="insert into login(username,password,email,gender) values(%s,%s,%s,%s)"
        data=cur.execute(query,(username,password,email,gender))
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.openWindow(username)
        conn.commit()
        cur.close()
        conn.close()
        #os.system('python homepage.py')  # redirecting to homepage after successful signup
        #sys.exit()
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(711, 520)
        Dialog.setMinimumSize(QtCore.QSize(0, 520))
        Dialog.setMaximumSize(QtCore.QSize(711, 520))
        Dialog.setWindowOpacity(10.0)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("QDialog{\n"
"    border-image: url(:/new/bg6.jpg) strech strech;\n"
"\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        Dialog.setModal(True)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(210, 80, 301, 371))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255,0.6);\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"font: 8pt \"Berlin Sans FB\";")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(90, 300, 121, 41))
        self.pushButton.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"\n"
"border-radius: 10px;")
        self.pushButton.setObjectName("pushBUtton_2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(60, 270, 111, 16))
        self.label_4.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"font:  10pt \"Berlin Sans FB\";")
        self.label_4.setObjectName("label_4")
        #self.label_5 = QtWidgets.QLabel(self.frame)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 270, 71, 16))
        self.pushButton_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);\n"
"font:  10pt \"Berlin Sans FB\";\n"
"")

   
       
        #self.label_5.setOpenExternalLinks(True)
       
        
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(30, 80, 221, 21))
        self.lineEdit.setStyleSheet("font: 8pt \"Berlin Sans FB\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"border:none;\n"
"border-bottom:1px solid grey;")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 130, 221, 21))
        self.lineEdit_2.setStyleSheet("font: 8pt \"Berlin Sans FB\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"border:none;\n"
"border-bottom:1px solid grey;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(2)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(110, 20, 151, 41))
        self.label_3.setStyleSheet("font: 75 16pt \"Berlin Sans FB\";\n"
"color: rgb(0, 0, 0);\n"
"\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(30, 180, 211, 21))
        self.lineEdit_3.setStyleSheet("font: 8pt \"Berlin Sans FB\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"border:none;\n"
"border-bottom:1px solid grey;\n"
"")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.radioButton = QtWidgets.QRadioButton(self.frame)
        self.radioButton.setGeometry(QtCore.QRect(60, 226, 91, 21))
        self.radioButton.setStyleSheet("font: 8pt \"Berlin Sans FB\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"border:none;\n"
"")
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame)
        self.radioButton_2.setGeometry(QtCore.QRect(180, 230, 82, 17))
        self.radioButton_2.setStyleSheet("font: 8pt \"Berlin Sans FB\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"border:none;\n"
"")
        self.radioButton_2.setObjectName("radioButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(340, 30, 71, 71))
        self.label.setStyleSheet("image: url(:/logo/profile.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton.clicked.connect(self.signup)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Sign Up"))
        self.label_4.setText(_translate("Dialog", "Already a Member?"))
        self.pushButton_2.setText(_translate("Dialog", "Login Here"))
        #self.label_5.setText("<a href=asl.py>Login here</a>");
        self.pushButton_2.clicked.connect(self.loginlink)  #redirect to login
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Username"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Password"))
        self.label_3.setText(_translate("Dialog", "Sign Up"))
        self.lineEdit_3.setPlaceholderText(_translate("Dialog", "Email id"))
        self.radioButton.setText(_translate("Dialog", "Female"))
        self.radioButton_2.setText(_translate("Dialog", "Male"))
        #self.pushButton.clicked.connect(self.asl)

import test_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog2 = QtWidgets.QDialog()

    ui = Ui_Dialog2()
    ui.setupUi(Dialog2)
    Dialog2.show()
    sys.exit(app.exec_())



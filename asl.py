# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asl.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
import os
from homepage import Ui_Dialog1
#from signup import Ui_Dialog2
class Ui_Dialog(object):  #class name Ui_Dialog
    def signuplink(self):#running sugnupfile
        print("open signup")
        self.window=QtWidgets.QDialog()
        self.ui=Ui_Dialog2()
        self.ui.setupUi(self.window)
        self.window.show()
        Dialog.hide()
    # this method is to open homepage and hide the current window
    def openWindow(self,username): 
        print("open")
        self.window=QtWidgets.QDialog()
        self.message = self.lineEdit.text()
        self.ui=Ui_Dialog1(self.message)
        self.ui.setupUi(self.window)
        self.window.show()
        Dialog.hide()
        
        
        
    #Login verfication fucntion
    def login(self):
        print("hello")
        username=self.lineEdit.text()
        password=self.lineEdit_2.text()
        print(username)
        #connection checking
        try:
            conn = pymysql.connect(host='localhost' ,port= 3305,user='root',password='',db='sample')
        except pymysql.MySQLError as e:
            print(e)
            sys.exit()
        finally:
            print("done")
        cur=conn.cursor()
        query="select * from login where username=%s and password=%s"
        data=cur.execute(query,(username,password))
        #print(cur.description)
        print()
        row=cur.fetchall()
        if(len(row)>0):
            for row in row:
                print(row)
            print("Login Successful!!")#successful login 
            mess=QtWidgets.QMessageBox()
            mess.setWindowTitle("Congrats")
            mess.setText("Logged In!")
            mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
            mess.exec_()
            self.openWindow(username)
           
            #os.system('python homepage.py')# redirecting to homepage after successful login
            
            #sys.exit()

        else:#WRONG LOGIN DIALOG
            print("Please login again!")
            self.lineEdit_2.clear()
            self.lineEdit.clear()
            mess=QtWidgets.QMessageBox()
            mess.setWindowTitle("Alert")
            mess.setText("Try Again!")
            mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
            mess.exec_()

       
        
        
       
       
        cur.close()
        conn.close()
        
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
        self.frame.setGeometry(QtCore.QRect(20, 90, 291, 341))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255,0.2);\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"font: 8pt \"Berlin Sans FB\";")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(80, 260, 121, 41))
        self.pushButton.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"\n"
"border-radius: 10px;")
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(70, 30, 151, 31))
        self.label_3.setStyleSheet("font: 75 16pt \"Berlin Sans FB\";\n"
"color: rgb(0, 0, 0);\n"
"\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(60, 220, 71, 16))
        self.label_4.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"font:  10pt \"Berlin Sans FB\";")
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        #self.label_5 = QtWidgets.QLabel(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 220, 71, 16))
        self.pushButton_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);\n"
"font:  10pt \"Berlin Sans FB\";\n"
"")
        #self.label_5.setOpenExternalLinks(True)
        #self.label_5.setText('<a> href=file:///'+signup.py+'>Open Project Folder</a>')
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(30, 90, 221, 41))
        self.lineEdit.setStyleSheet("font: 8pt \"Berlin Sans FB\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"border:none;\n"
"border-bottom:1px solid grey;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 150, 221, 41))
        self.lineEdit_2.setStyleSheet("font: 8pt \"Berlin Sans FB\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"border:none;\n"
"border-bottom:1px solid grey;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(340, 30, 71, 71))
        self.label.setStyleSheet("image: url(:/logo/profile.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(120, 40, 81, 71))
        self.label_2.setStyleSheet("image: url(:/logo/pg.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton.clicked.connect(self.login)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Log In"))
        self.label_3.setText(_translate("Dialog", "Welcome to ASL"))
        self.label_4.setText(_translate("Dialog", "New to ASL?"))
        #self.label_5.setText(_translate("Dialog", "Sign Up here"))
        self.pushButton_2.setText(_translate("Dialog", "Sign up Here"))
        
        self.pushButton_2.clicked.connect(self.signuplink) # redirect to signup
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Username"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Password"))

import test_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    


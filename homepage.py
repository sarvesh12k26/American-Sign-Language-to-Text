# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'homepage.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from handhistframe import Ui_Dialog4
from capture import Ui_Dialog3
import os
class Ui_Dialog1(object):  #class name Ui_Dialog1
    def __init__(self,message):
        self.message=message
        print("hello" +str(message))

        
    def handhist(self):
        print("hand hist fun")
        os.system('python handhistframe.py')
        '''
        self.window=QtWidgets.QDialog()
        self.ui=Ui_Dialog4()
        self.ui.setupUi(self.window)
        self.window.show()
        '''






          
    def communicate(self):
        print("communciate fun")
        os.system('python capture.py')
        '''
        self.window=QtWidgets.QDialog()
        self.ui=Ui_Dialog3()
        self.ui.setupUi(self.window)
        self.window.show()
        #Dialog1.hide()
        '''


        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(730, 566)
        Dialog.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(110, 400, 201, 61))
        self.pushButton.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 12pt \"Segoe UI Semibold\";border-radius: 4px;")
        self.pushButton.setObjectName("pushButon")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 400, 211, 61))
        self.pushButton_2.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 12pt \"Segoe UI Semibold\";border-radius: 4px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 10, 310, 41))
        self.label.setStyleSheet("font: 63 20pt \"Segoe UI Semibold\";\n"
"color: rgb(73, 173, 188);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(0, 10, 51, 41))
        self.label_2.setStyleSheet("image: url(:/new/aslnew.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(410, 10, 61, 41))
        self.label_3.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 12pt \"Segoe UI Semibold\";border-radius: 4px;")
        self.label_3.setObjectName("label_3")
        self.instructions = QtWidgets.QLabel(Dialog)
        self.instructions.setGeometry(QtCore.QRect(40, 90, 540, 230))
        self.instructions.setStyleSheet("background-color: rgb(84, 162, 177,0.5);\n"
";\n"
"font: 63 10pt \"Segoe UI Semibold\";border-radius: 4px;")
        self.instructions.setObjectName("instructions")
        self.instructions.setText("  Instructions:\n  1.Click on 'Setup hand' button to scan your hand for the APP.\n  2.It is necessary to scan each time you change your environment.\n  3.For scanning press 'S', a new window will open, make sure in that\n  window your hand is white and its surrounding is black, to close the\n  new window press 'X'.\n  4. Click on Communicate button to start using the text formulation\n  services")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(465, 10, 261, 41))
        self.label_4.setStyleSheet("background-color: rgb(84, 162, 177);\n"
";\n"
"font: 63 12pt \"Segoe UI Semibold\";border-radius: 4px;")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.pushButton.clicked.connect(self.handhist)
        self.pushButton_2.clicked.connect(self.communicate)
        self.retranslateUi(Dialog)
        self.label_4.setText("Sarvesh")
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Setup Hand"))
        self.pushButton_2.setText(_translate("Dialog", "Communicate"))
        self.label.setText(_translate("Dialog", "ASL Communication"))
        self.label_3.setText(_translate("Dialog", "  Hi!  "))
        #self.instructions.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Instructions: <span style=\" font-weight:600;\">Press \'q\' to exit or press \'s\' to save</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog", str("    ") + self.message)) #set logged in username
import test_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog1 = QtWidgets.QDialog()
    ui = Ui_Dialog1("Hello")
    ui.setupUi(Dialog1)
    Dialog1.show()
    sys.exit(app.exec_())


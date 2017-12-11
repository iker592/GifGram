#________________________________________________
#Juan Gallaga
# CST 205 - Final Project - "GifGram" 
# December 9, 2017
# 
# 
#Description - GifGram-  Desktop PyQt5 App that searches, and modifies gifs from Giphy.com
# Features - Text Editor, Searchbar, Webcam, Color Editor.
# 
 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
######
import math
from camera import Camera


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # self.home()
        self.showLogo()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.verticalGroupBox)
        self.setLayout(mainLayout)
        self.setGeometry(150,150,600,500)
        self.setWindowTitle("GifGram")







        self.show()
    # #CentralWidget for GifGram UI.
    # def home(self):
    #     vbox = QVBoxLayout()
    #     central_widget = QWidget()
    #     central_widget.setLayout(vbox)
    #     vbox.addWidget(SearchGroupBox())
    #     self.setCentralWidget(central_widget)
    #     self.show()

# #############################################################
# class SearchGroupBox(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.create()
#         self.showLogo()
#         mainLayout = QVBoxLayout()
#         mainLayout.addWidget(self.verticalGroupBox)
#         mainLayout.addWidget(self.h_srcgroupbox)
#         self.setLayout(mainLayout)
#     def create(self):
#         #Widgets
#         self.h_srcgroupbox= QGroupBox("SEARCH FOR GIFS")
#         self.searchbar= QLineEdit(self)
#         self.searchbar.setPlaceholderText("Search Gif Term Here")
#         # self.searchbar.returnPressed()
#         self.src_btn = QPushButton("Search",self)
#         self.limit_label = QLabel(self)
#         self.limit_label.setText("GifGram\u2122 is in alpha stage. Please Wait while GifGram\u2122"" Searches for Gifs. ")#\u2122 tm
#         self.limit_label.setAlignment(Qt.AlignCenter)
#         self.limit_bar = QLineEdit(self)
#         self.limit_bar.setPlaceholderText("Enter Limit Here")
#         #Layouts 
#         h_layout = QHBoxLayout()
#         h_layout.addWidget(self.searchbar)
#         h_layout.addWidget(self.limit_bar)
#         h_layout.addWidget(self.src_btn)
#         #
#         v2_layout = QVBoxLayout()
#         v2_layout.addWidget(self.limit_label)

#         v_layout = QVBoxLayout()
#         v_layout.addLayout(h_layout)
#         v_layout.addLayout(v2_layout)
#         #Set Layout
#         self.h_srcgroupbox.setLayout(v_layout)
#         #Search button clicked
#         self.src_btn.clicked.connect(self.on_click)
    def showLogo(self):
        self.verticalGroupBox = QGroupBox()
        #Logo
        self.picture_label = QLabel(self)
        my_image = QPixmap("gifgram_logo.png")
        self.picture_label.setPixmap(my_image)
        self.picture_label.setAlignment(Qt.AlignCenter)
        #Layout
        v_layoutp = QVBoxLayout()
        v_layoutp.addWidget(self.picture_label)
        self.verticalGroupBox.setLayout(v_layoutp)
#################
    @pyqtSlot()
    def on_click(self):

        src_btn = self.sender()

#############################
my_app = QApplication(sys.argv)
a_window = MyWindow()

a_window.show()
#This code below opens camera. It opens in a new window. 
# Idont know why after I take a pic, the camera widget wont close.
# my_cam = Camera()
# my_cam.show()


sys.exit(my_app.exec_())


#


#


##

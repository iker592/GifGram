#________________________________________________
#Juan Gallaga
# CST 205 - Homework 3
# October 10, 2017
# 
#Description - Pyqt GUI that searches through Dictionary in image_information.py and retrieves image back. The Gui has
# a combobox that has a list of image manipulation options to change the image.
import requests
import json
import sys
from pprint import pprint
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from itertools import count
from PyQt5 import QtCore, QtGui, QtWidgets
###########3


my_key = 'lS0mFdGz0h6K8qPVK77kOM2atN4vQppp'

q = 'otter'

limit = 3

endpoint = "https://api.giphy.com/v1/gifs/search?api_key=lS0mFdGz0h6K8qPVK77kOM2atN4vQppp&q=" + str(q) + "&limit=" + str(limit) + "&offset=0&rating=G&lang=en"

response = requests.get(endpoint)

data = response.json()
##############
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PIL import Image
import math
from camera import Camera


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        #self.create_label() 
        # self.createSearchHGroupBox()
        # self.createComboBox()
        # self.showPicture()
        #mainLayout = QVBoxLayout()
        # mainLayout.addWidget(self.horizontalGroupBox)
        # mainLayout.addWidget(self.verticalGroupBox)
        # mainLayout.addWidget(self.my_combo_box)
        #mainLayout.addWidget(MyWindow2())
        #mainLayout.addWidget(self.search_box)
        ####3
        #wid = QtGui.QWidget(self)
        # self.setCentralWidget(wid)
        # layout = QtGui.QVBoxLayout()
        # wid.setLayout(layout)
        #3
        #self.setCentralWidget(mainLayout)
        #self.setLayout(mainLayout)

        self.home()
        self.setGeometry(150,150,600,500)
        self.setWindowTitle("GifGram")
        self.show()
    def home(self):
        vbox = QVBoxLayout()
        #textbrowser = QTextBrowser()
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        #btn.clicked.connect(self.close)
        # vbox.addWidget(textbrowser)
        vbox.addWidget(SearchGroupBox())
        #vbox.addWidget(showLogo())
        self.setCentralWidget(central_widget)
        self.show()


# ######################################################################################3
class SearchGroupBox(QWidget):

    def __init__(self):
        super().__init__()
        self.create(my_key, q, limit, endpoint, response, data)
        self.showLogo()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.verticalGroupBox)
        mainLayout.addWidget(self.h_groupbox)
        self.setLayout(mainLayout)
    def create(self, my_key, q, limit, endpoint, response, data):
        #Widgets
        self.h_groupbox= QGroupBox("SEARCH FOR GIFS")
        self.searchbar= QLineEdit(self)
        # q= self.searchbar.text()
        self.src_btn = QPushButton("Search",self)
        self.limit_label = QLabel(self)
        self.limit_label.setText("GifGram\u2122 is in alpha stage. Please Wait while GifGram\u2122"" Searches for Gifs. ")
        self.limit_label.setAlignment(Qt.AlignCenter)

        #
        # self.gifgram_logo = QLabel(self)
        # my_image = QPixmap("gifgram_logo.png")
        # self.gifgram_logo.setPixmap(my_image)
        #Layouts
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.searchbar)
        h_layout.addWidget(self.src_btn)
        #
        v2_layout = QVBoxLayout()
        # v2_layout.addWidget(self.gifgram_logo)
        v2_layout.addWidget(self.limit_label)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addLayout(v2_layout)
        ###
        self.h_groupbox.setLayout(v_layout)
        self.src_btn.clicked.connect(self.on_click)
    def showLogo(self):
        self.verticalGroupBox = QGroupBox()
        self.picture_label = QLabel(self)
        my_image = QPixmap("gifgram_logo.png")
        
        self.picture_label.setPixmap(my_image)
        self.picture_label.setAlignment(Qt.AlignCenter)
        #
        v_layoutp = QVBoxLayout()
        v_layoutp.addWidget(self.picture_label)
        self.verticalGroupBox.setLayout(v_layoutp)

#################

############################################################################3
        #  pyqtSlot() function decorator to create a Qt slot

    @pyqtSlot()
    def on_click(self):
        # self.results = APIResults(self)
        #self.results = QWidget()

        #search_button = self.sender()
        src_btn = self.sender()
        APIResults(self).show()

####33
class APIResults(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        self.setGeometry(200, 200, 400, 400)
        #self.setGeometry(200, 200, size.width(), size.height())
        self.setWindowTitle("GIF results")
        
        #for i in range(0, limit, 1)
        #size = self.movie.scaledSize()     
        
        # Set up the label
        self.movie_screen = QLabel()
        
        # Make the label fit the gif
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        
        # Create the layout     
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)    
        self.setLayout(main_layout)
        
        gif_url = data["data"][0]["images"]["original"]["url"]
        
        #print(gif_url)
        
        gif_to_open = requests.get(gif_url)
            
        gif = Image.open(BytesIO(gif_to_open.content))      
        
        # Load the file into a QMovie
        self.movie = QMovie("happy.gif", QByteArray(), self)
        
        
        # Add the QMovie object to the label
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
#########################################
#merge class here to display in main certral widget.


#############################
my_app = QApplication(sys.argv)
a_window = MyWindow()
a_window.show()
#This code below opens camera. It opens in a new window. 
# Idont know why after I take a pic, the camera widget wont close.
# my_cam = Camera()
# my_cam.show()
# sys.exit(my_cam.exec_())

sys.exit(my_app.exec_())

#


#


##

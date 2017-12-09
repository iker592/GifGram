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
import urllib
from urllib import request
import cv2
import numpy as np
import os
import imageio
import math

limit  = 8

class APIResults(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		
		self.setGeometry(200, 200, 400, 400)
		self.setWindowTitle("GIF results")		
		
		# Create the layout		
		main_layout = QVBoxLayout()			
		
		self.horizontalGroupBox = QGroupBox("")
		row_layout = QHBoxLayout()
		
		for i in range(0, limit, 1):
		
			# After every 4th gif, display the next gif in the next row.	
			# If this is the fourth gif, move to the next row.
			if i % 4 == 0:
				
				self.horizontalGroupBox = QGroupBox("")
				row_layout = QHBoxLayout()
			
			# Set up the label
			self.movie_screen = QLabel()
				
			# Make the label fit the gif
			self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.movie_screen.setAlignment(Qt.AlignCenter)
				
			# Load the file into a QMovie
			self.movie = QMovie('./thumbnail_results/result' + str(i) + '.gif', QByteArray(), self)
				
			# Add the QMovie object to the label
			self.movie.setCacheMode(QMovie.CacheAll)
			self.movie.setSpeed(100)
			self.movie_screen.setMovie(self.movie)
			self.movie.start()
			

			row_layout.addWidget(self.movie_screen)
			
			if i % 4 == 0:
				self.horizontalGroupBox.setLayout(row_layout)				
				main_layout.addWidget(self.horizontalGroupBox)			
		
		self.setLayout(main_layout)



app = QApplication(sys.argv)
main = APIResults()

			#main.setGeometry(700, 400, 200, 50)

main.show()
sys.exit(app.exec_())

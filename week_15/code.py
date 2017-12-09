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

my_key = 'lS0mFdGz0h6K8qPVK77kOM2atN4vQppp'

q = 'otter'

limit = 3

endpoint = "https://api.giphy.com/v1/gifs/search?api_key=lS0mFdGz0h6K8qPVK77kOM2atN4vQppp&q=" + str(q) + "&limit=" + str(limit) + "&offset=0&rating=G&lang=en"

response = requests.get(endpoint)

data = response.json()

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







app = QApplication(sys.argv)
main = APIResults()

#main.setGeometry(700, 400, 200, 50)

main.show()
sys.exit(app.exec_())
		
		
		
			
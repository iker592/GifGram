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

my_key = 'lS0mFdGz0h6K8qPVK77kOM2atN4vQppp'

q = 'marvel comics'

limit = 10

endpoint = "https://api.giphy.com/v1/gifs/search?api_key=lS0mFdGz0h6K8qPVK77kOM2atN4vQppp&q=" + str(q) + "&limit=" + str(limit) + "&offset=0&rating=G&lang=en"

response = requests.get(endpoint)

data = response.json()

# This function produces a thumbnail of an image by reducing its size by half

# Get the thumbnail of each frame, and save the new frames

def thumbnail(photo):
	new_photo = Image.new("RGB", (math.ceil(photo.width/2), math.ceil(photo.height/2)), "white")
	target_x = 0
	for source_x in range(0, photo.width, 2):
		target_y = 0
		for source_y in range(0, photo.height, 2):
			color = photo.getpixel((source_x, source_y))
			new_photo.putpixel((target_x, target_y), color)
			target_y += 1
		target_x += 1
	return new_photo

# Open each downloaded API response gif, make them a thumbnail, save (overwrite) the original gif
# Get the frames of a gif, thumbnail then, and then reassemble the frames.
# Path: the path to a gif
#def thumbnail_results(path, result_number):	
	
	#for i in range(0, limit, 1):
	
		#path = './api_results/result' + str(i) + '.gif'
	
	#gif = Image.open(path)			
	#thumbnail_gif = thumbnail(gif)
		
	#thumbnail_gif.save('./thumbnail_results/result' + str(result_number) + '.gif')
	
	
		
		#with open('./api_results/result' + str(i) + '.gif', 'wb')  as file:
					#file.write(thumbnail_gif)
	
# Download the gifs returned by the API call
def download_gifs():

	# Loop over all results, get their url, and download each result gif 
	for i in range(0, limit, 1):					
		url = data["data"][i]["images"]["original"]["url"]
			
			#gif = urllib.request.urlretrieve(url, '/api_results/result' + str(i) + '.gif')
			
			#gif = urllib.request.urlretrieve(url, 'result.gif')
		with open('./api_results/result' + str(i) + '.gif', 'wb')  as file:
			file.write(requests.get(url).content)	

# Extract each frame from a gif
# Path: The path to the downloaded gif
# Result_number: the number of which result: first or second etc.
def get_frames_from_gif(path, result_number):

	# This will be returned at the end of the function, because we need to know how long to iterate when reconstructing the thumbnailed gif from the frames
	number_of_frames = 0
	
	mode = analyze_gif(path)['mode']
	image = Image.open(path)
	
	p = image.getpalette()
	last_frame = image.convert('RGBA')
	
	try:
		while True:
			# If the gif uses local color tables, each frame will have its own palette.
			# If not, we need to apply the global palette to the new frame.
			if not image.getpalette():
				image.putpalette(p)
				
			new_frame = Image.new('RGBA', image.size)	
			
			# If the gif is a "partial" mode gif where frames update a region of a different size
			# to the entire image, we must create the new frame by putting it over the preceding frame.
			if mode == 'partial':
				new_frame.paste(last_frame)
			
			new_frame.paste(image, (0,0), image.convert('RGBA'))
			# This should put frames into the frames folder!!!!!!!!
			
			# Save the thumnail of each frame
			thumbnail_image = thumbnail(new_frame)			
			thumbnail_image.save('frames/%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), number_of_frames), 'PNG')
			
			number_of_frames += 1
			last_frame = new_frame
			image.seek(image.tell() + 1)
	except EOFError:
		pass
		
	return number_of_frames
			
# Pre-proces the image to determine the mode: full or additive. This is necessary because
# assessing single frames is not reliable, so we must know the mode before processing the frames of a gif.
def analyze_gif(path):
	image = Image.open(path)
	results = {
		'size': image.size,
		'mode': 'full'
	}
	try:
		while True:
			if image.tile:
				tile = image.tile[0]
				update_region = tile[1]
				update_region_dimensions = update_region[2:]
				if update_region_dimensions != image.size:
					results['mode'] = 'partial'
					break
			image.seek(image.tell() + 1)
	except EOFError:
		pass
	return results	

# This function puts together the frames of a gif
def construct_gif(list_of_frames, new_name):
	images = []
	for file in list_of_frames:
		#print("FILE:" + str(file))
		images.append(imageio.imread(file))
	imageio.mimsave(new_name, images)
	
#class ClickableGif(QLabel):
	#clicked = QtCore.Signal(str)
	
	#def__init__(self, image_name):
	#	super(ClickableGif, self).__init__()
		
		
	#def mouse_press_event(self, event):
	#	self.clicked.emit(self.objectName())
	
	
def clickable(widget):
	class Filter(QObject):
		clicked = pyqtSignal()
		
		def eventFilter(self, obj, event):
		
			if obj == widget:
				if event.type() == QEvent.MouseButtonRelease:
					if obj.rect().contains(event.pos()):
						self.clicked.emit()
						return True
			return False
	filter = Filter(widget)
	widget.installEventFilter(filter)
	return filter.clicked
			
			

class APIResults(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		
		self.setGeometry(100, 100, 400, 400)
		#self.setGeometry(200, 200, size.width(), size.height())
		self.setWindowTitle("GIF results")
		
		# Create the layout		
		main_layout = QVBoxLayout()
		
		self.horizontalGroupBox = QGroupBox("")
		row_layout = QHBoxLayout	
		
		self.results_label = QLabel()
		self.results_label.setText('<h1>Results<h1>')
		main_layout.addWidget(self.results_label)
		
		# This list will keep track of each GIF's number in order. These numbers will be used in the combo box to choose an GIF for modification.
		image_number_list = []
		
		for i in range(0, limit, 1):
		
			# After every 4th gif, display the next gif in the next row.	
			# If this is the fourth gif, move to the next row.
			if i % 5 == 0:
				
				self.horizontalGroupBox = QGroupBox("")
				row_layout = QHBoxLayout()
		
			self.empty_label = QLabel()
			row_layout.addWidget(self.empty_label)
		
		
			# The number of the image. This helps the user see the number of the image which they wish to modiy.
			self.number_label = QLabel()
			self.number_label.setText('GIF ' + str(i+1) + ':')
			row_layout.addWidget(self.number_label)		
			
			
			# Set up the label
			self.movie_screen = QLabel()
				
			# Make the label fit the gif
			self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.movie_screen.setAlignment(Qt.AlignCenter)
				
			self.movie_screen.setObjectName('./thumbnail_results/result' + str(i) + '.gif')	
			
			# Load the file into a QMovie
			self.movie = QMovie('./thumbnail_results/result' + str(i) + '.gif', QByteArray(), self)
			#self.button.setObjectName('./thumbnail_results/result' + str(i) + '.gif')
			#self.movie_screen.mousePressEvent = self.clicked_gif
			
			clickable(self.movie_screen).connect(self.on_click)
			
			#self.movie_screen.setText('./thumbnail_results/result' + str(i) + '.gif');
				
			# Add the QMovie object to the label
			self.movie.setCacheMode(QMovie.CacheAll)
			self.movie.setSpeed(100)
			self.movie_screen.setMovie(self.movie)
			self.movie.start()
						
			
			#self.button.setObjectName('./thumbnail_results/result' + str(i) + '.gif')
			#self.title.setText('./thumbnail_results/result' + str(i) + '.gif')
			#row_layout.addWidget(self.title)
			
			#print("Name: " + self.movie_screen.objectName())
			
			row_layout.addWidget(self.movie_screen)
			#row_layout.addWidget(self.button)
			
			# After every 4th gif, add the horizontal layout to the main layout
			if i % 5 == 0:
				self.horizontalGroupBox.setLayout(row_layout)
				main_layout.addWidget(self.horizontalGroupBox)		
				
			image_number_list.append(str(i+1))
		
		self.choose_label = QLabel()
		self.choose_label.setText('Choose the GIF to be modified:')
		main_layout.addWidget(self.choose_label)
		
		# Combo box to choose the number of the image which will be modified
		self.combo_box = QComboBox()
		self.combo_box.addItems(image_number_list)
		main_layout.addWidget(self.combo_box)
		
		# This button will be clicked when the number of the image which will be modified is selected from the combo box
		self.modify_button = QPushButton("Modify")
		self.modify_button.clicked.connect(self.on_click)
		main_layout.addWidget(self.modify_button)
		
		self.setLayout(main_layout)
	
	# This function is called on click to the modify_button
	@pyqtSlot()
	def on_click(self):
		print(self.combo_box.currentText())

# First download each gif returned by the API call, get the frames of each, thumbnail each frame of a gif,
# put the thumbnailed frames together, and show the gif
download_gifs()

for i in range(0, limit, 1):	
	
	number_of_frames = get_frames_from_gif('./api_results/result' + str(i) + '.gif', i)
	
	# This list will store the list of files that are the thumbnailed frames
	list_of_frames = []
	
	# Iterate through each thumbnailed frame extracted from the current gif, and construct the thumbnailed gif
	
	
	# Get the names of each frame
	for frame_number in range(0, number_of_frames, 1):
		
		frame_name = 'frames/result' + str(i) + '-' + str(frame_number) + '.png'
		list_of_frames.append(frame_name)

	
	# Construct the thumbnailed gif
	construct_gif(list_of_frames, './thumbnail_results/result' + str(i) + '.gif')
#thumbnail_results('./api_results/result' + str(0) + '.gif', 0)
	
	


app = QApplication(sys.argv)
main = APIResults()

			#main.setGeometry(700, 400, 200, 50)

main.show()
sys.exit(app.exec_())
		
		
		
			
# Author: Albert Jozsa-Kiraly
# Course: CST 205 - Multimedia Design & Programming
# Final Project - GifGram
# Date: 12/09/2017

# This is the API results window.
# This Python file is used to send a request to the Giphy API with a given search term and the number of gifs to be returned.
# The returned gifs are downloaded to a folder, their frames are extracted, downscaled, and thumbnail gifs are produced.
# These thumbnail gifs are displayed in a window along with some labels. The user can choose the number of the gif to be
# modified from a combo box, and on click to the "Modify" button, the user is taken to a different window where the gif can be modified.

import requests
import json
import sys
import os
import imageio
import math
from urllib import request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox, QGroupBox, QSizePolicy
from PyQt5.QtCore import pyqtSlot, Qt, QByteArray
from PyQt5.QtGui import QMovie
from PIL import Image

# The search term being sent to the API. Gifs related to this will be searched.
q = 'otter'

# The number of gifs to be returned to the user
limit = 5

# This is the search endpoint with the API key included. The response will be in JSON format.
endpoint = "https://api.giphy.com/v1/gifs/search?api_key=lS0mFdGz0h6K8qPVK77kOM2atN4vQppp&q=" + str(q) + "&limit=" + str(limit) + "&offset=0&rating=G&lang=en"
response = requests.get(endpoint)
data = response.json()

# This function produces a thumbnail of an image by reducing its size by half. We will use this function to scale down the frames of a gif.
# Parameter:
# photo: the frame of the gif
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
	
# This function downloads the gifs returned by the API call.
def download_gifs():
	# Loop over all results, get each url, and download each returned gif 
	for i in range(0, limit, 1):					
		url = data["data"][i]["images"]["original"]["url"]				
		with open('./api_results/result' + str(i) + '.gif', 'wb')  as file:
			file.write(requests.get(url).content)	

# This function extracts each frame from a gif.
# Parameters:
# path: the path to the downloaded gif
# result_number: the number of the result gif: first, or second etc.
def get_frames_from_gif(path, result_number):

	# This variable will be returned at the end of the function, because we need to know how long to iterate when reconstructing the thumbnailed gif from the frames
	number_of_frames = 0
	
	# Analyze the gif: pre-process the image.
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
			# to the entire image, we must create the new frame by putting it over the previous frame.
			if mode == 'partial':
				new_frame.paste(last_frame)
			
			new_frame.paste(image, (0,0), image.convert('RGBA'))
			
			# Save the thumnail of each frame
			thumbnail_image = thumbnail(new_frame)			
			thumbnail_image.save('frames/%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), number_of_frames), 'PNG')
			
			number_of_frames += 1
			last_frame = new_frame
			image.seek(image.tell() + 1)
	except EOFError:
		pass
		
	return number_of_frames
			
# Pre-proces the image to determine the mode: full or additive. This is necessary, because
# assessing single frames is not reliable, so we must know the mode before processing the frames of a gif.
# Parameter:
# path: the path to the downloaded gif
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

# This function puts together the frames to produce a gif.
# Parameters:
# list_of_frames: the list containing the file name of each frame
# new_name: the name of the new gif
def construct_gif(list_of_frames, new_name):
	images = []
	for file in list_of_frames:
		images.append(imageio.imread(file))
	imageio.mimsave(new_name, images)				

# This class creates the GUI for the window which displays the gifs, some labels showing the numbers of the gifs, a combo box, and a button.
class APIResults(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		
		self.setGeometry(100, 100, 400, 400)
		self.setWindowTitle("GIF results")
		
		# Create the layout		
		main_layout = QVBoxLayout()
		
		# Gifs will be dispalyed in rows, there will be 5 gif in each row.
		self.horizontalGroupBox = QGroupBox("")
		row_layout = QHBoxLayout	
		
		self.results_label = QLabel()
		self.results_label.setText('<h1>Results<h1>')
		main_layout.addWidget(self.results_label)
		
		# This list will keep track of each gif's number in order. These numbers will be used in the combo box, so that the user can choose a gif for modification.
		image_number_list = []
		
		# Loop and display each thumbnail gif
		for i in range(0, limit, 1):
		
			# After every 4th gif, move to the next row, and display the next gifs there.	
			if i % 4 == 0:				
				self.horizontalGroupBox = QGroupBox("")
				row_layout = QHBoxLayout()
		
			# This empty label is just needed to make some space between the actual labels and the gifs in the window.
			self.empty_label = QLabel()
			row_layout.addWidget(self.empty_label)		
		
			# The number of the current gif. This helps the user see the number of the gif which they wish to modiy.
			self.number_label = QLabel()
			self.number_label.setText('GIF ' + str(i+1) + ':')
			row_layout.addWidget(self.number_label)			
			
			# Set up the label which will hold the gif
			self.gif_screen = QLabel()
				
			# Make the label fit the gif
			self.gif_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.gif_screen.setAlignment(Qt.AlignCenter)
			
			# Load the current gif into a QMovie
			self.movie = QMovie('./thumbnail_results/result' + str(i) + '.gif', QByteArray(), self)
				
			# Add the QMovie object to the label
			self.movie.setCacheMode(QMovie.CacheAll)
			self.movie.setSpeed(100)
			self.gif_screen.setMovie(self.movie)
			self.movie.start()
									
			row_layout.addWidget(self.gif_screen)
			
			# After every 4th gif, add the horizontal layout to the main layout.
			if i % 4 == 0:
				self.horizontalGroupBox.setLayout(row_layout)
				main_layout.addWidget(self.horizontalGroupBox)		
				
			image_number_list.append(str(i+1))
		
		self.choose_label = QLabel()
		self.choose_label.setText('Choose the GIF to be modified:')
		main_layout.addWidget(self.choose_label)
		
		# Combo box which allows the user to choose the number of the gif which will be modified.
		self.combo_box = QComboBox()
		self.combo_box.addItems(image_number_list)
		main_layout.addWidget(self.combo_box)
		
		# This button will be clicked when the number of the gif to be modified is selected from the combo box.
		self.modify_button = QPushButton("Modify")
		self.modify_button.clicked.connect(self.on_click)
		main_layout.addWidget(self.modify_button)
		
		self.setLayout(main_layout)
	
	# This function is called on click to modify_button
	@pyqtSlot()
	def on_click(self):
		print(self.combo_box.currentText())

# First, download each gif returned by the API.
download_gifs()

# Loop over each gif, get the frames of the current gif, thumbnail each frame,
# and put the thumbnail frames together to produce a new gif. This is done for each downloaded gif.
for i in range(0, limit, 1):	
	
	# Extract the frames of the current gif
	number_of_frames = get_frames_from_gif('./api_results/result' + str(i) + '.gif', i)
	
	# This list will store the list of files which are the thumbnail frames
	list_of_frames = []
	
	# Iterate through each thumbnail frame of the current gif, and store the name of the frame.
	for frame_number in range(0, number_of_frames, 1):
		
		frame_name = 'frames/result' + str(i) + '-' + str(frame_number) + '.png'
		list_of_frames.append(frame_name)
		
	# Construct the thumbnail gif from the frames
	construct_gif(list_of_frames, './thumbnail_results/result' + str(i) + '.gif')

# Launch the GUI
app = QApplication(sys.argv)
main = APIResults()

main.show()
sys.exit(app.exec_())
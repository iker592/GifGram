# Course: CST 205 - Multimedia Design & Programming
# Title: CST 205 Final Project - Team 6: GifGram
# Authors: Iker Redondo Pedroce, Juan Gallaga-Chavez, Albert Jozsa-Kiraly
# Date: 12/10/2017

# This is a Python program which opens a window, so the user can search for gifs 
# related to a specific term, and the program uses the Giphy API to find gifs to the user. 
# By default, always 4 gifs are returned and displayed in a new window. 
# The user can choose the number of the gif and click on the "Modify" button. 
# Afterwards, a new window pops up where the user can add text to the top and 
# bottom of the gif, and apply a filter to the gif. 
# The modified gif is automatically saved in the project folder.

import gifextract
import toGIF
import addText
import sys
import time
import requests
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import imageio
import math
from urllib import request
from PIL import Image
from PIL.ImageQt import ImageQt

# The gif filter options
my_list = ["None", "Sepia", "Negative", "Grayscale"]

# The number of gifs to be returned to the user
limit = 4

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
def download_gifs(q, limit):

	# First, make the API call to get the gifs
	# This is the search endpoint with the API key included. The response will be in JSON format.
	endpoint = "https://api.giphy.com/v1/gifs/search?api_key=lS0mFdGz0h6K8qPVK77kOM2atN4vQppp&q=" + str(q) + "&limit=" + str(limit) + "&offset=0&rating=G&lang=en"
	response = requests.get(endpoint)
	data = response.json()

    # Loop over all results, get each url, and download each returned gif 
	for i in range(0, int(limit), 1):                    
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
            thumbnail_image.save('framesThumb/%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), number_of_frames), 'PNG')
            
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

# This function calls the functions which make the API call, get the frames of the gifs, and construct the thumbnail gifs.
# This is the main workflow of getting the gifs from the Giphy API.
def callAPI(q, limit):

    # First, download each gif returned by the API.
	download_gifs(q, limit) 

    # Loop over each gif, get the frames of the current gif, thumbnail each frame,
    # and put the thumbnail frames together to produce a new gif. This is done for each downloaded gif.
	for i in range(0, int(limit), 1):    
        
        # Extract the frames of the current gif
		number_of_frames = get_frames_from_gif('./api_results/result' + str(i) + '.gif', i)
        
        # This list will store the list of files which are the thumbnail frames
		list_of_frames = []
        
        # Iterate through each thumbnail frame of the current gif, and store the name of the frame.
		for frame_number in range(0, number_of_frames, 1):
            
			frame_name = 'framesThumb/result' + str(i) + '-' + str(frame_number) + '.png'
			list_of_frames.append(frame_name)
            
        # Construct the thumbnail gif from the frames
		construct_gif(list_of_frames, './thumbnail_results/result' + str(i) + '.gif')   

# This class creates the GUI for the window which displays the gifs, some labels showing the numbers of the gifs, a combo box, and a button.
class APIResults(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
        
		self.setGeometry(100, 100, 400, 400)
		self.setWindowTitle("GIF results")
		
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.cyan)
		self.setPalette(p)
        
        # Create the layout     
		main_layout = QVBoxLayout()
        
        # Gifs will be dispalyed in rows, there will be 5 gif in each row.
		self.horizontalGroupBox = QGroupBox("")
		row_layout = QHBoxLayout    
        
		self.results_label = QLabel()
		self.results_label.setText('<h1>Results<h1>')
		self.results_label.setAlignment(Qt.AlignCenter)
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
		global file
		file ="api_results/result"+ str(int(self.combo_box.currentText()) - 1)+".gif"
		print(file)
		self.new_win = editWindow()
		self.new_win.show()

# This is the window where the user can edit a gif
class editWindow(QWidget):

	filenames = []

	def __init__(self):
		super().__init__()
		self.init_ui()

	def loadGIF(self,fileName):
		self.movie_screen = QLabel()
        # Make the label fit the gif
		self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.movie_screen.setAlignment(Qt.AlignCenter)
		
        # Load the file into a QMovie
		self.movie = QMovie(fileName, QByteArray(), self)
		
        # Add the QMovie object to the label
		self.movie.setCacheMode(QMovie.CacheAll)
		self.movie.setSpeed(100)
		self.movie_screen.setMovie(self.movie)
		self.movie.start()

	def init_ui(self):
		self.my_label = QLabel("Top Text: ", self)
		self.my_labelBottom = QLabel("Bottom Text: ", self)
		self.my_labelPick = QLabel("Pick a Filter: ", self)

		self.my_line_edit = QLineEdit(self)
		self.my_line_edit.setPlaceholderText("Enter some text")

		self.my_line_editBottom = QLineEdit(self)
		self.my_line_editBottom.setPlaceholderText("Enter some text")

		self.my_combo_box = QComboBox()
		self.my_combo_box.addItems(my_list)

		self.response_label = QLabel(self)

		self.submit_btn = QPushButton("Create", self)

		self.my_label2 = QLabel(self)
		print(f"the file name: {file}")
		self.loadGIF(file)

		h_layout = QHBoxLayout()
		h_layout.addWidget(self.my_label)
		h_layout.addWidget(self.my_line_edit)

		h2_layout = QHBoxLayout()
		h2_layout.addWidget(self.my_labelBottom)
		h2_layout.addWidget(self.my_line_editBottom)

		h3_layout = QHBoxLayout()
		h3_layout.addWidget(self.my_labelPick)
		h3_layout.addWidget(self.my_combo_box)

		self.v2_layout = QVBoxLayout()
		self.v2_layout.addWidget(self.submit_btn)
		self.v2_layout.addWidget(self.movie_screen)

		self.v_layout = QVBoxLayout()
		self.v_layout.addWidget(self.my_label2)

		self.v_layout.addLayout(h_layout)
		self.v_layout.addLayout(h2_layout)
		self.v_layout.addLayout(h3_layout)
		self.v_layout.addLayout(self.v2_layout)

		self.setLayout(self.v_layout)

		self.my_combo_box.currentIndexChanged.connect(self.update_ui)
		self.submit_btn.clicked.connect(self.on_click)
		
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.cyan)
		self.setPalette(p)

		self.setWindowTitle("Edit Window")
		self.setGeometry(450, 200, 600, 400)
		self.show()

	# Produces the negative of an image
	def negative(self,picture,i,top_line_value,bottom_line_value):
		new_list = []
		for p in picture.getdata():
			temp = (255-p[0], 255-p[1], 255-p[2])
			new_list.append(temp)
		picture.putdata(new_list)
		picture = addText.add(picture,top_line_value,bottom_line_value,picture.width,picture.height)
		picture.save("modifiedFrames/newFrame-"+str(i)+".png")
		self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")

	# Saves a gif which does not need a filter (if the user chose to apply no filter to the modified gif).
	def noneFilter(self,picture,i,top_line_value,bottom_line_value):

		picture = addText.add(picture,top_line_value,bottom_line_value,picture.width,picture.height)
		picture.save("modifiedFrames/newFrame-"+str(i)+".png")
		self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")

	# Produces a sepia image
	def grayscaleSepia(self,picture,i,top_line_value,bottom_line_value):
		new_list = []
		for p in picture.getdata():
			new_red = int(p[0] * 0.299)
			new_green = int(p[1] * 0.587)
			new_blue = int(p[2] * 0.114)
			luminance = new_red + new_green + new_blue
			temp = (luminance, luminance, luminance)
			new_list.append(temp)
		picture.putdata(new_list)
		picture = addText.add(picture,top_line_value,bottom_line_value,picture.width,picture.height)
		picture.save("modifiedFrames/newFrame-"+str(i)+".png")
		self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")
		return new_list

	def sepia_tint(self,picture,i,top_line_value,bottom_line_value):
		width, height = picture.size
		mode = picture.mode
		temp_list = []
		pic_data = self.grayscaleSepia(picture,i,top_line_value,bottom_line_value)
		for p in pic_data:
            # tint shadows
			if p[0] < 63:
				red_val = int(p[0] * 1.1)
				green_val = p[1]
				blue_val = int(p[2] * 0.9)
            # tint midtones
			if p[0] > 62 and p[0] < 192:
				red_val = int(p[0] * 1.15)
				green_val = p[1]
				blue_val = int(p[2] * 0.85)
            # tint highlights
			if p[0] > 191:
				red_val = int(p[0] * 1.08)
				if red_val > 255:
					red_val = 255
				green_val = p[1]
				blue_val = int(p[2] * 0.5)
			temp_list.append((red_val, green_val, blue_val))
		picture.putdata(temp_list)
		picture = addText.add(picture,top_line_value,bottom_line_value,picture.width,picture.height)
		picture.save("modifiedFrames/newFrame-"+str(i)+".png")
		self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")

	# Produces the thumbnail of an image
	def thumbnail(self,picture,i,top_line_value,bottom_line_value):
		s = 2
		canvas = Image.new("RGB", (math.ceil(picture.width/s), math.ceil(picture.height/s)), "white")
		target_x = 0
		for source_x in range(0, picture.width, s):
			target_y = 0
			for source_y in range(0, picture.height, s):
				color = picture.getpixel((source_x, source_y))
				canvas.putpixel((target_x, target_y), color)
				target_y += 1
			target_x += 1
		picture = addText.add(picture,top_line_value,bottom_line_value,picture.width,picture.height)

		picture.save("modifiedFrames/newFrame-"+str(i)+".png")
		self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")

	# Produces the grayscale of an image
	def grayscale(self,picture,i,top_line_value,bottom_line_value):
		new_list = []
		for p in picture.getdata():
			intensity = int((p[0] + p[1] + p[2])/3)
			temp = (intensity, intensity, intensity)
			new_list.append(temp)
		picture.putdata(new_list)

		picture = addText.add(picture,top_line_value,bottom_line_value,picture.width,picture.height)

		picture.save("modifiedFrames/newFrame-"+str(i)+".png")
		self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")

	@pyqtSlot()
	def update_ui(self):
		my_text = self.my_combo_box.currentText()
		print(f'\n{my_text} filter selected')

	# This function is called when the "Create" button is pressed in the Edit Window. 
	# The selected modification is applied to the gif.
	@pyqtSlot()
	def on_click(self):
		item = self.v2_layout.takeAt(1)
		item.widget().deleteLater()

		self.v2_layout.addWidget(self.movie_screen)
		self.setLayout(self.v_layout)

		top_line_value = self.my_line_edit.text()
		bottom_line_value = self.my_line_editBottom.text()

		numberOfFrames = gifextract.processImage(file)
		my_text = self.my_combo_box.currentText()
		if my_text != 'Pick a filter':
			if my_text == 'Grayscale':
				for i in range(0,numberOfFrames):
					im = Image.open('frames/'+file[11:-4] +"-"+ str(i) + '.png')
					self.grayscale(im,i,top_line_value,bottom_line_value)
				toGIF.gifIt(self.filenames)
				self.filenames.clear()
			elif my_text == 'Negative':
				for i in range(0,numberOfFrames):
					im = Image.open('frames/'+file[11:-4] +"-"+ str(i) + '.png')
					self.negative(im,i,top_line_value,bottom_line_value)
				toGIF.gifIt(self.filenames)
				self.filenames.clear()
			elif my_text == 'Sepia':
				for i in range(0,numberOfFrames):
					im = Image.open('frames/'+file[11:-4] +"-"+ str(i) + '.png')
					self.sepia_tint(im,i,top_line_value,bottom_line_value)
				toGIF.gifIt(self.filenames)
				self.filenames.clear()
			elif my_text == 'None':
				for i in range(0,numberOfFrames):
					im = Image.open('frames/'+file[11:-4] +"-"+ str(i) + '.png')
					self.noneFilter(im,i,top_line_value,bottom_line_value)
				toGIF.gifIt(self.filenames)
				self.filenames.clear()	
				
		item = self.v2_layout.takeAt(1)
		item.widget().deleteLater()

		self.loadGIF("newGIF.gif")

		self.v2_layout.addWidget(self.movie_screen)
		self.setLayout(self.v_layout)
		
# This is the window the user sees after launching the application.
# The main logo is displayed. A search box is provided where a search term can be entered.
class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.v_layout = QVBoxLayout()
		self.picture_label = QLabel(self)
		my_image = QPixmap("gifgram_logo_big.png")
		self.picture_label.setPixmap(my_image)
		self.picture_label.setAlignment(Qt.AlignCenter)
		self.search_line_edit = QLineEdit(self)
		self.search_line_edit.setPlaceholderText("Enter some text")
		self.v_layout.addWidget(self.picture_label)
		self.v_layout.addWidget(self.search_line_edit)
		self.submit_btn = QPushButton("Search", self)
		self.submit_btn.clicked.connect(self.showResults)
		self.v_layout.addWidget(self.submit_btn)
		self.setLayout(self.v_layout)

	@pyqtSlot()
	def showResults(self):
		q = self.search_line_edit.text()
		callAPI(q, limit)        
		self.new_win = APIResults()
		self.new_win.show()

app = QApplication(sys.argv)
main = MainWindow()
main.setAutoFillBackground(True)
p = main.palette()
p.setColor(main.backgroundRole(), Qt.cyan)
main.setPalette(p)
main.setWindowTitle("GifGram\u2122 Search Window")
main.setGeometry(450, 200, 600, 400)
main.show()
sys.exit(app.exec_())
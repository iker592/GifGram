import requests
import json
import sys
from pprint import pprint
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
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
#pprint(data)

#with open("response.txt", "w") as file:
	#file.write(json.dumps(data))



#qt_app = QApplication(sys.argv)

# Window object
#window = QWidget()
#window.setWindowTitle("Results")




	
	# This label will hold the image
	#image_label = QLabel(window)
	#image = QPixmap()
	
	

#window.resize(500, 1000)
#window.show()

#sys.exit(my_qt_app.exec_())

###########

class ImageLabel(tk.Label):
	def load(self, img):
		if isinstance(img, str):
			img = Image.open(img)
		self.loc = 0
		self.frames = []
		
		try:
			for i in count(1):
				self.frames.append(ImageTk.PhotoImage(img.copy()))
				img.seek(i)
				
		except EOFError:
			pass
			
		try:
			self.delay = img.info['duartion']
		except:
			self.delay = 100
			
		if len(self.frames) == 1:
			self.config(image = self.frames[0])
		else:
			self.next_frame()
	
	def unload(self):
		self.config(image=None)
		self.frames = None
	
	def next_frame(self):
		if self.frames:
			self.loc += 1
			self.loc %= len(self.frames)
			self.config(image=self.frames[self.loc])
			self.after(self.delay, self.next_frame)
			
			
for i in range(0, limit, 1):
	
	
	# QPixmap object
	
	
	# Get the url of the original gif
	#print(data["data"][i]["images"]["original"]["url"])
	
	gif_url = data["data"][i]["images"]["original"]["url"]
	
	gif_to_open = requests.get(gif_url)
	
	gif = Image.open(BytesIO(gif_to_open.content))
			
	root = tk.Tk()
	label = ImageLabel(root)
	label.pack()
	
	
	label.load(gif)
	root.mainloop()		
		
		
		
		
		
		
			
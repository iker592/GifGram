import gifextract
import toGIF
import addText
import sys
from PyQt5 import *
import time

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QComboBox ,QHBoxLayout, QVBoxLayout,QSizePolicy)
from PyQt5.QtCore import *#pyqtSlot
from PyQt5.QtGui import *#QPixmap,QImage
from PIL import Image
from PIL.ImageQt import ImageQt
import math

my_list = ["None", "Sepia", "Negative", "Grayscale","Thumbnail"]
term =""





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
        #self.my_line_edit.setGeometry(QtCore.QRect(0, 0, 0, 0))

        self.my_line_editBottom = QLineEdit(self)
        self.my_line_editBottom.setPlaceholderText("Enter some text")
        #self.my_line_editBottom.setGeometry(QtCore.QRect(260, 380, 50, 25))

        self.my_combo_box = QComboBox()
        self.my_combo_box.addItems(my_list)

        self.response_label = QLabel(self)

        self.submit_btn = QPushButton("Create", self)

        self.my_label2 = QLabel(self)

#///////////////////////////////////////////////////////////////////////////////////////////
        self.loadGIF("source.gif")
#///////////////////////////////////////////////////////////////////////////////////////////


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.my_label)
        h_layout.addWidget(self.my_line_edit)
        #h_layout.addWidget(self.my_combo_box)

        h2_layout = QHBoxLayout()
        h2_layout.addWidget(self.my_labelBottom)
        h2_layout.addWidget(self.my_line_editBottom)
        #h2_layout.addWidget(self.my_combo_box)

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

        self.setWindowTitle("Edit Window")
        self.setGeometry(450, 200, 600, 400)
        self.show()


#######################################################################
    def negative(self,picture,i,top_line_value,bottom_line_value):
        new_list = []
        for p in picture.getdata():
            temp = (255-p[0], 255-p[1], 255-p[2])
            new_list.append(temp)
        picture.putdata(new_list)
        #print(picture.width)
        picture = addText.add(picture,top_line_value,bottom_line_value,picture.width,picture.height)
        picture.save("modifiedFrames/newFrame-"+str(i)+".png")
        self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")

    def noneFilter(self,picture,i,top_line_value,bottom_line_value):

        picture = addText.add(picture,top_line_value,bottom_line_value,picture.width,picture.height)
        picture.save("modifiedFrames/newFrame-"+str(i)+".png")
        self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")

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
#############################################################

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

    @pyqtSlot()
    def on_click(self):
        item = self.v2_layout.takeAt(1)
        item.widget().deleteLater()

#///////////////////////////////////////////////////////////////////////////////////////////
        self.loadGIF("loading.gif")
#///////////////////////////////////////////////////////////////////////////////////////////

        self.v2_layout.addWidget(self.movie_screen)
        #self.v_layout.addLayout(self.v2_layout)
        self.setLayout(self.v_layout)
        #time.sleep(5.5)
        top_line_value = self.my_line_edit.text()
        bottom_line_value = self.my_line_editBottom.text()

        numberOfFrames = gifextract.processImage('source.gif')
        my_text = self.my_combo_box.currentText()
        if my_text != 'Pick a filter':
            if my_text == 'Grayscale':
                for i in range(0,numberOfFrames):
                    im = Image.open('frames/source-' + str(i) + '.png')
                    self.grayscale(im,i,top_line_value,bottom_line_value)
                toGIF.gifIt(self.filenames)
            elif my_text == 'Negative':
                for i in range(0,numberOfFrames):
                    im = Image.open('frames/source-' + str(i) + '.png')
                    self.negative(im,i,top_line_value,bottom_line_value)
                toGIF.gifIt(self.filenames)
            elif my_text == 'Sepia':
                for i in range(0,numberOfFrames):
                    im = Image.open('frames/source-' + str(i) + '.png')
                    self.sepia_tint(im,i,top_line_value,bottom_line_value)
                toGIF.gifIt(self.filenames)
            elif my_text == 'None':
                for i in range(0,numberOfFrames):
                    im = Image.open('frames/source-' + str(i) + '.png')
                    self.noneFilter(im,i,top_line_value,bottom_line_value)
                toGIF.gifIt(self.filenames)
            elif my_text == 'Thumbnail':
                for i in range(0,numberOfFrames):
                    im = Image.open('frames/source-' + str(i) + '.png')
                    im = self.thumbnail(im,i,top_line_value,bottom_line_value)
                toGIF.gifIt(self.filenames)

        print("GIF CREATED!!")
        #self.v2_layout.removeWidget(self.movie_screen)
        item = self.v2_layout.takeAt(1)
        item.widget().deleteLater()

#///////////////////////////////////////////////////////////////////////////////////////////
        self.loadGIF("newGIF.gif")
#///////////////////////////////////////////////////////////////////////////////////////////

        self.v2_layout.addWidget(self.movie_screen)
        #self.v_layout.addLayout(self.v2_layout)
        self.setLayout(self.v_layout)
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()
        self.my_line_edit = QLineEdit(self)
        self.my_line_edit.setPlaceholderText("Enter some text")
        self.v_layout.addWidget(self.my_line_edit)
        self.submit_btn = QPushButton("Search", self)
        self.submit_btn.clicked.connect(self.update_ui)
        self.v_layout.addWidget(self.submit_btn)

        
        self.setLayout(self.v_layout)


    @pyqtSlot()
    def update_ui(self):
        # ... do stuff
        term = self.my_line_edit.text()
        self.new_win = editWindow()
        self.new_win.show()

app = QApplication(sys.argv)
main = MainWindow()
main.show()
main.setWindowTitle("Search Window")
main.setGeometry(450, 200, 600, 400)
sys.exit(app.exec_())
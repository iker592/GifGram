import gifextract
import toGIF
import addText
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QComboBox ,QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap,QImage
from PIL import Image
from PIL.ImageQt import ImageQt
import math

my_list = ["Pick a filter", "Sepia", "Negative", "Grayscale","None"]

class Window(QWidget):

    filenames = []

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.my_label = QLabel("Top Text: ", self)
        self.my_labelBottom = QLabel("Bottom Text: ", self)
        self.my_labelPick = QLabel("Pick a Filter: ", self)
        #self.my_labelFilter = QLabel("Search: ", self)

        self.my_line_edit = QLineEdit(self)
        self.my_line_edit.setPlaceholderText("Enter some text")
        self.my_line_edit.setGeometry(QtCore.QRect(260, 380, 113, 25))

        self.my_line_editBottom = QLineEdit(self)
        self.my_line_editBottom.setPlaceholderText("Enter some text")
        self.my_line_edit.setGeometry(QtCore.QRect(260, 380, 113, 25))

        self.my_combo_box = QComboBox()
        self.my_combo_box.addItems(my_list)

        self.response_label = QLabel(self)

        self.submit_btn = QPushButton("Create", self)

        self.my_label2 = QLabel(self)


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

        v2_layout = QVBoxLayout()
        v2_layout.addWidget(self.submit_btn)
        v2_layout.addWidget(self.response_label)

        v_layout = QVBoxLayout()

        v_layout.addWidget(self.my_label2)
#        im = Image.open('source-0.png')
#        im = im.convert("RGBA")
#        qim = ImageQt(im)
#        pix = QPixmap.fromImage(qim)  
#        self.my_pixmap = pix    #QPixmap('images/'+max+'.jpg')
#        self.my_label2.setPixmap(self.my_pixmap)
#        self.my_label2.setGeometry(380, 50, 500, 500)

        v_layout.addLayout(h_layout)
        v_layout.addLayout(h2_layout)
        v_layout.addLayout(h3_layout)
        v_layout.addLayout(v2_layout)

        self.setLayout(v_layout)

        self.my_combo_box.currentIndexChanged.connect(self.update_ui)
        self.submit_btn.clicked.connect(self.on_click)

        self.setWindowTitle("Window layout")
        self.setGeometry(450, 200, 600, 400)
        self.show()


#######################################################################
    def negative(self,picture,i,top_line_value,bottom_line_value):
        new_list = []
        for p in picture.getdata():
            temp = (255-p[0], 255-p[1], 255-p[2])
            new_list.append(temp)
        picture.putdata(new_list)
        picture = addText.add(picture,top_line_value,bottom_line_value)
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
        picture = addText.add(picture,top_line_value,bottom_line_value)
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
        picture = addText.add(picture,top_line_value,bottom_line_value)
        picture.save("modifiedFrames/newFrame-"+str(i)+".png")
        self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")



#    def thumbnail(self,picture):
#        s = 2
#        canvas = Image.new("RGB", (math.ceil(picture.width/s), math.ceil(picture.height/s)), "white")
#        target_x = 0
#        for source_x in range(0, picture.width, s):
#            target_y = 0
#            for source_y in range(0, picture.height, s):
#                color = picture.getpixel((source_x, source_y))
#                canvas.putpixel((target_x, target_y), color)
#                target_y += 1
#            target_x += 1
#        return canvas
#############################################################

    def grayscale(self,picture,i,top_line_value,bottom_line_value):
        new_list = []
        for p in picture.getdata():
            intensity = int((p[0] + p[1] + p[2])/3)
            temp = (intensity, intensity, intensity)
            new_list.append(temp)
        picture.putdata(new_list)

        picture = addText.add(picture,top_line_value,bottom_line_value)

        picture.save("modifiedFrames/newFrame-"+str(i)+".png")
        self.filenames.append("modifiedFrames/newFrame-"+str(i)+".png")

    @pyqtSlot()
    def update_ui(self):
        my_text = self.my_combo_box.currentText()
        print(f'\n{my_text} filter selected')

    @pyqtSlot()
    def on_click(self):
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
        print("GIF CREATED!!")

#            elif my_text == 'Thumbnail':
#                for i in range(0,numberOfFrames):
#                    im = Image.open('frames/source-' + str(i) + '.png')
#                    im = self.thumbnail(im,i)



app = QApplication(sys.argv)
main = Window()

sys.exit(app.exec_())



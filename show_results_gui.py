from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap

qt_app = QApplication(sys.argv)

# Window object
window = QWidget()
window.setWindowTitle("Results")



for(0, 2, 1):
	# This label will hold the image
	image_label = QLabel(window)
	
	# QPixmap object
	image = QPixmap()
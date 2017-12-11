#!/usr/bin/env python2
# coding=utf-8
"""

"""

# http://stackoverflow.com/questions/15177313/accessing-a-webcam-from-pyside-opencv

from PySide import QtCore, QtGui
import cv, time

app = QtGui.QApplication([])

camcapture = cv.CaptureFromCAM(0)

while True:

    frame = cv.QueryFrame(camcapture)
    image = QtGui.QImage(frame.tostring(), frame.width, frame.height, QtGui.QImage.Format_RGB888).rgbSwapped()
    pixmap = QtGui.QPixmap.fromImage(image)
    time.sleap(0.05)

app.exec_() 

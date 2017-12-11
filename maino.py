
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QDialog
from mainwindow import Ui_MainWindow
#from results import Ui_Form



#####
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    # @pyqtSlot()
    # def on_click(self):
    #     search = self.sender()
    #     print(search.text())
#class Form(QWidget):
#	def __init__(self):
#		super(Form, self).__init__()
#		#
#		self.ui2 = Ui_Form()
#		self.ui2.setupUi(self)


app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()

sys.exit(app.exec_())
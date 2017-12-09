from PyQt5 import QtGui, QtCore, QtWidgets

MainFile = "mainfile.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainFile)
FileIntro = "Intro.ui" 
Ui_WindowIntro,_ = uic.loadUiType(FileIntro)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.ButtonIntro.clicked.connect(self.OpenWindowIntro)

    def OpenWindowIntro(self):
        self.anotherwindow = WindowIntro()
        self.anotherwindow.close()

class WindowIntro(QtWidgets.QMainWindow, Ui_WindowIntro):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_WindowIntro.__init__(self)
        self.setupUi(self)

        #close the window
        self.Button2.clicked.connect(self.Close)

    def Close(self):
        self.close()

if __name__ == "__main__":
    app = 0 # if not the core will die
    app = QtWidgets.QApplication(sys.argv)

    if login():
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
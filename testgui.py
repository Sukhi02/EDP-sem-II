import sys
from PyQt4 import QtGui,QtCore, uic

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('MainGui.ui', self)
	self.startButton.clicked.connect(self.startb)
	self.pauseButton.clicked.connect(self.pauseb)
	self.stopButton.clicked.connect(self.stopb)
        self.show()

    def startb(self):
	print('startButton Pressed')

    def pauseb(self):
	print('pauseButton Pressed')
    
    def stopb(self):
	print('stopButton Pressed')

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

	


from PyQt4 import QtGui
from PyQt4 import QtCore
import sys

# Import our user interface produced by QTDesigner.
import ui

# For the loading stuff.
import os

# Computer vision library
import cv2

class TextureReconstruction(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.LoadImagesButton.clicked.connect(self.loadImagesCalib)
        # When the calibration is not done disable tab 1.
        self.applicationTab.setTabEnabled(1, False)
        # When the reconstruction is not done disable tab 2.
        self.applicationTab.setTabEnabled(2, False)


    def loadImagesCalib(self):
        filenames = QtGui.QFileDialog.getOpenFileNames(self , "Open File", QtCore.QDir.currentPath());

        for fileName in filenames:
            if fileName:
                image = QtGui.QImage(fileName)
                if image.isNull():
                    QtGui.QMessageBox.information(self, "Image Viewer", "Cannot load %s. Only image files are accepted." % fileName)
                    return
            tmp = QtGui.QPixmap(fileName)
            label = QtGui.QLabel(self.distortedImage)
            # Does not work ...
            label.setScaledContents(True)
            label.setPixmap(tmp)
            label.show()

def main():
    app = QtGui.QApplication(sys.argv)
    form = TextureReconstruction()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

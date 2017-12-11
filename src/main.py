
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys

# Import our user interface produced by QTDesigner.
import ui

# For the loading stuff.
import os

# Computer vision library
import cv2

import calibration

# In this file, we handle the link between our library and the UI.

class TextureReconstruction(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.loadImagesButton.clicked.connect(self.loadImagesCalib)
        self.calibrateButton.clicked.connect(self.calibrateCamera)
        # When the calibration is not done disable tab 1.
        self.applicationTab.setTabEnabled(1, False)
        # When the reconstruction is not done disable tab 2.
        self.applicationTab.setTabEnabled(2, False)

        # Attributes.
        self.calibImages = []
        self.reconstructionImages = []

    def loadImagesCalib(self):
        self.calibImages = []
        filenames = QtGui.QFileDialog.getOpenFileNames(self , "Open File", QtCore.QDir.currentPath());
        for fileName in filenames:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer", "Cannot load %s. Only image files are accepted." % fileName)
                return
            opencv_img = cv2.imread(str(fileName))
            self.calibImages += [opencv_img]
            #calibration.checkCalibImage(opencv_img)
            #gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('lol', gray)
            #cv2.waitKey(500);

            #tmp = QtGui.QPixmap(fileName)
            #self.distortedImage.setPixmap(tmp)
            #self.distortedImage.show()
        self.calibrateButton.setEnabled(True)

    def calibrateCamera(self):
        calibration.calibrateImages(self.calibImages)


def main():
    app = QtGui.QApplication(sys.argv)
    form = TextureReconstruction()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy as np
import sys

# Import our user interface produced by QTDesigner.
import ui

# For the loading stuff.
import os

# Computer vision library
import cv2

import calibration
import reconstruction
import visualization

# In this file, we handle the link between our library and the UI.

# Callback for square selection.
def polyDraw(event, x, y, flags, poly):
    if event == cv2.EVENT_LBUTTONDOWN:
        poly += [(x, y)]

class TextureReconstruction(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        # When the calibration is not done disable tab 1.
        self.applicationTab.setTabEnabled(1, False)
        # When the reconstruction is not done disable tab 2.
        self.applicationTab.setTabEnabled(2, False)
        # Calibration related.
        self.loadImagesButton.clicked.connect(self.loadImagesCalib)
        self.imageSlider.setVisible(False)
        self.undistortedImage.setVisible(False)
        self.distortedImage.setVisible(False)
        self.calibrationProgress.setVisible(False)
        # Reconstruction related.
        self.loadImagesReconstructionButton.clicked.connect(self.loadImagesReconstruction)
        self.alignSlider.setVisible(False)
        self.alignProgress.setVisible(False)
        self.recon = reconstruction.Reconstruction(self)
        self.initImage.setVisible(False)
        self.resultImage.setVisible(False)
        # Attributes.
        self.calibImages = []
        self.reconstructionImages = []
        self.calib = calibration.Calibration(self)
	self.visu = visualization.Visualization(self)

    def loadImagesCalib(self):
	self.calibrationOutput.setText("")
        self.calibImages = []
        self.undistortedImages = []
        self.distortedImages = []
        filenames = QtGui.QFileDialog.getOpenFileNames(self , "Open File", QtCore.QDir.currentPath());
        for fileName in filenames:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer", "Cannot load %s. Only image files are accepted." % fileName)
                return
            opencv_img = cv2.imread(str(fileName))
            # A little too long.
            if not(self.calib.checkCalibImage(opencv_img)):
		self.calibrationOutput.append("<span style='color:#ff0000;'>Image " + fileName + " does not contain a calibration grid !</span>")
	    else:
		self.calibrationOutput.append("Image " + fileName + " contains a calibration grid.")
            	self.calibImages += [opencv_img]
		
        self.calibrateButton.setEnabled(True)
	if (len(self.calibImages) > 3):
		self.calibrationOutput.append("<html><b>Calibration images loaded successfully</b</html>")
	else:
		self.calibrationOutput.append("<html><b>Calibration images failed to load</b></html>")
	self.calib.setCalibImages(self.calibImages)
		
    def loadImagesReconstruction(self):
	self.recon.polyImages = []
	self.reconstructionImages = []
        filenames = QtGui.QFileDialog.getOpenFileNames(self , "Open File", QtCore.QDir.currentPath());
        for fileName in filenames:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer", "Cannot load %s. Only image files are accepted." % fileName)
                return

            opencv_img = cv2.imread(str(fileName))
            # FIXME: don't do it everytime.
            height, width, channel = opencv_img.shape
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.calib.K, self.calib.dist, (width, height), 1, (width, height))
            opencv_img = cv2.undistort(opencv_img, self.calib.K, self.calib.dist, None, newcameramtx)
            # End.

            self.reconstructionImages += [opencv_img]
        self.alignImagesButton.setEnabled(True)

        # Init image.
        poly = []
        init = self.reconstructionImages[0].copy()
	cv2.putText(init, "Click on the plane corners.", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
        cv2.imshow('Square initialization', init)
        init = cv2.cvtColor(init, cv2.COLOR_BGR2RGB)
        cv2.setMouseCallback('Square initialization', polyDraw, poly)
        while len(poly) != 4:
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        for i in range(0, len(poly)):
            cv2.line(init, (poly[i-1][0], poly[i-1][1]), (poly[i][0], poly[i][1]), (255,0, 0),5)

        height, width, channel = init.shape
        bytesPerLine = 3 * width
        tmp = QtGui.QImage(init.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.initImage.setPixmap(QtGui.QPixmap.fromImage(tmp))
        self.initImage.show()
	self.recon.setReconstructionImages(self.reconstructionImages)
	self.recon.setPoly(poly)
        tmp = QtGui.QImage(init.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.recon.polyImages = [tmp]

def main():
    app = QtGui.QApplication(sys.argv)
    form = TextureReconstruction()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

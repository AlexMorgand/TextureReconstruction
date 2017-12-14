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

# In this file, we handle the link between our library and the UI.

# Callback for square selection.
def polyDraw(event, x, y, flags, poly):
    if event == cv2.EVENT_LBUTTONDOWN:
        poly += [(x, y)]

class TextureReconstruction(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        # Calibration.
        self.loadImagesButton.clicked.connect(self.loadImagesCalib)
        self.calibrateButton.clicked.connect(self.calibrateCamera)
        # When the calibration is not done disable tab 1.
        self.applicationTab.setTabEnabled(1, False)
        # When the reconstruction is not done disable tab 2.
        self.applicationTab.setTabEnabled(2, False)
        self.imageSlider.setVisible(False)
        self.imageSlider.valueChanged.connect(self.calibrationSliderChange)
        self.calibrationProgress.setVisible(False)
        # Reconstruction.
        self.loadImagesReconstructionButton.clicked.connect(self.loadImagesReconstruction)
        self.alignImagesButton.clicked.connect(self.alignImages)
        self.alignSlider.setVisible(False)
        self.alignProgress.setVisible(False)

        # Attributes.
        self.calibImages = []
        self.undistortedImages = []
        self.distortedImages = []
        self.reconstructionImages = []
        self.calib = calibration.Calibration(self)

    def loadImagesCalib(self):
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
            # if not(self.calib.checkCalibImage(opencv_img)):
            #    QtGui.QMessageBox.information(self, "Image Viewer", "Cannot detect a calibration grid in the image %s." % fileName)
            #    return
            self.calibImages += [opencv_img]
        self.calibrateButton.setEnabled(True)

    def calibrateCamera(self):
        self.calibrationProgress.setVisible(True)
        self.K, self.dist = self.calib.calibrateImages(self.calibImages)
        self.calibrationProgress.setVisible(False)
        nb_img = len(self.calibImages)
        height, width, channel = self.calibImages[0].shape
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.K, self.dist, (width, height), 1, (width, height))

        for img in self.calibImages:
            # OpenCV is BGR and Qt is RGB.
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # undistort
            dst = cv2.undistort(img, self.K, self.dist, None, newcameramtx)
            bytesPerLine = 3 * width
            tmp = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            self.distortedImages += [tmp]

            tmp = QtGui.QImage(dst.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)

            self.undistortedImages += [tmp]

            self.applicationTab.setTabEnabled(1, True)
            self.alignImagesButton.setEnabled(False)
            self.imageSlider.setVisible(True)
            self.imageSlider.setMinimum(0)
            self.imageSlider.setMaximum(nb_img - 1)
            self.imageSlider.setValue(0)

            # Initial call to init.
            self.calibrationSliderChange()

    def calibrationSliderChange(self):
        i = self.imageSlider.value()
        disImg = self.distortedImages[i]
        self.distortedImage.setPixmap(QtGui.QPixmap.fromImage(disImg))
        self.distortedImage.show()

        undisImg = self.undistortedImages[i]
        self.undistortedImage.setPixmap(QtGui.QPixmap.fromImage(undisImg))
        self.undistortedImage.show()


    def loadImagesReconstruction(self):
        self.recontructionImages = []
        filenames = QtGui.QFileDialog.getOpenFileNames(self , "Open File", QtCore.QDir.currentPath());
        for fileName in filenames:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer", "Cannot load %s. Only image files are accepted." % fileName)
                return


            opencv_img = cv2.imread(str(fileName))


            # FIXME: don't do it everytime.
            height, width, channel = opencv_img.shape
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.K, self.dist, (width, height), 1, (width, height))
            opencv_img = cv2.undistort(opencv_img, self.K, self.dist, None, newcameramtx)
            # End.

            self.reconstructionImages += [opencv_img]
        self.alignImagesButton.setEnabled(True)

        # Init image.
        poly = []
        init = cv2.cvtColor(self.reconstructionImages[0], cv2.COLOR_BGR2RGB)
        cv2.imshow('Square initialization', init)
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
        self.recon = reconstruction.Reconstruction(self, poly, self.reconstructionImages)
        tmp = QtGui.QImage(init.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.recon.polyImages += [tmp]

    def alignImages(self):
        texture = self.recon.alignImage()
        texture = cv2.cvtColor(texture, cv2.COLOR_BGR2RGB)
        height, width, channel = texture.shape
        bytesPerLine = 3 * width
        tmp = QtGui.QImage(texture.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.resultImage.setPixmap(QtGui.QPixmap.fromImage(tmp))
        self.resultImage.show()



def main():
    app = QtGui.QApplication(sys.argv)
    form = TextureReconstruction()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

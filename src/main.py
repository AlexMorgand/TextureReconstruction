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

        self.imageSlider.setVisible(False)
        self.imageSlider.valueChanged.connect(self.sliderChange)

        # Attributes.
        self.calibImages = []
        self.undistortedImages = []
        self.distortedImages = []
        self.reconstructionImages = []
        self.calib = calibration.Calibration(self)

    def loadImagesCalib(self):
        self.calibImages = []
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
        K, dist = self.calib.calibrateImages(self.calibImages)
        nb_img = len(self.calibImages)
        height, width, channel = self.calibImages[0].shape
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(K, dist, (width, height), 1, (width, height))

        for img in self.calibImages:
            # undistort
            dst = cv2.undistort(img, K, dist, None, newcameramtx)

            #mapx,mapy = cv2.initUndistortRectifyMap(K, dist, None, newcameramtx, (width, height),5)
            #dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

            # crop the image
            #x, y, w, h = roi
            #dst = dst[y:y+h, x:x+w]

            bytesPerLine = 3 * width
            tmp = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            self.distortedImages += [tmp]

            tmp = QtGui.QImage(dst.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)

            self.undistortedImages += [tmp]

            self.applicationTab.setTabEnabled(1, True)
            self.imageSlider.setVisible(True)
            self.imageSlider.setMinimum(0)
            self.imageSlider.setMaximum(nb_img - 1)

            # Initial call to init.
            self.sliderChange()

    def sliderChange(self):
        i = self.imageSlider.value()
        disImg = self.distortedImages[i]
        self.distortedImage.setPixmap(QtGui.QPixmap.fromImage(disImg))
        self.distortedImage.show()

        undisImg = self.undistortedImages[i]
        self.undistortedImage.setPixmap(QtGui.QPixmap.fromImage(undisImg))
        self.undistortedImage.show()


def main():
    app = QtGui.QApplication(sys.argv)
    form = TextureReconstruction()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

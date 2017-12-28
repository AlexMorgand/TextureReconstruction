import numpy as np
import cv2
from PyQt4 import QtGui
from PyQt4 import QtCore

class Calibration():
  def __init__(self, ui, row = 9, col = 6):
    # Link the user interface to handle progress bars and focus.
    self.ui = ui
    self.row = row
    self.col = col
    self.undistortedImages = []
    self.distortedImages = []
    self.ui.calibrateButton.clicked.connect(self.calibrateCamera)
    self.ui.imageSlider.valueChanged.connect(self.calibrationSliderChange)

  def setCalibImages(self, imgs):
    self.calibImages = imgs

  def checkCalibImage(self, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Termination criteria.
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((self.col * self.row, 3), np.float32)
    objp[:, :2] = np.mgrid[0:self.row, 0:self.col].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (self.row, self.col), None)
    # If found, add object points, image points (after refining them)
    if ret:
      return True
    else:
      return False

  def calibrateImages(self, images):
    self.ui.calibrationOutput.setText("")
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((self.col * self.row, 3), np.float32)
    objp[:, :2] = np.mgrid[0:self.row, 0:self.col].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    step = 100.0 / len(images)
    val = 0
    i = 1
    nb_img = len(images)
    consoleText = ''
    for image in images:
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      # Find the chess board corners
      ret, corners = cv2.findChessboardCorners(gray, (self.row, self.col), None)
      # If found, add object points, image points (after refining them)
      if ret:
          objpoints.append(objp)
          cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
          imgpoints.append(corners)
          val += step
          self.ui.calibrationProgress.setValue(int(val))
	  self.ui.calibrationOutput.append("Grid calibration detection in image " + str(i) + " out of " + str(nb_img))
	  i += 1
    self.ui.calibrationOutput.append("Grid calibration detection in image " + str(i) + " out of " + str(nb_img))
    self.ui.calibrationOutput.append("<html><b>Calibration done ! Intrinsic parameters matrix is:</b></html>")
    self.ui.calibrationProgress.setValue(100)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    return (mtx, dist)

  def calibrateCamera(self):
      self.ui.calibrationProgress.setVisible(True)
      self.K, self.dist = self.calibrateImages(self.calibImages)
      self.ui.calibrationOutput.append(str(self.K))
      self.ui.calibrationProgress.setVisible(False)
      nb_img = len(self.calibImages)
      height, width, channel = self.calibImages[0].shape
      newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.K, self.dist, (width, height), 1, (width, height))
      for img in self.calibImages:
          # OpenCV is BGR and Qt is RGB.
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          dst = cv2.undistort(img, self.K, self.dist, None, newcameramtx)
          bytesPerLine = 3 * width
          tmp = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
          self.distortedImages += [tmp]
          tmp = QtGui.QImage(dst.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
          self.undistortedImages += [tmp]
          self.ui.applicationTab.setTabEnabled(1, True)
          self.ui.alignImagesButton.setEnabled(False)
          self.ui.imageSlider.setVisible(True)
          self.ui.imageSlider.setMinimum(0)
          self.ui.imageSlider.setMaximum(nb_img - 1)
          self.ui.imageSlider.setValue(0)
          # Initial call to init.
          self.calibrationSliderChange()

  def calibrationSliderChange(self):
      i = self.ui.imageSlider.value()
      disImg = self.distortedImages[i]
      self.ui.distortedImage.setPixmap(QtGui.QPixmap.fromImage(disImg))
      self.ui.distortedImage.show()
      undisImg = self.undistortedImages[i]
      self.ui.undistortedImage.setPixmap(QtGui.QPixmap.fromImage(undisImg))
      self.ui.undistortedImage.show()


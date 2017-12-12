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

  def checkCalibImage(self, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
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
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((self.col * self.row, 3), np.float32)
    objp[:, :2] = np.mgrid[0:self.row, 0:self.col].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    step = 100.0 / len(images)
    val = 0

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

    self.ui.calibrationProgress.setValue(100)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    return (mtx, dist)

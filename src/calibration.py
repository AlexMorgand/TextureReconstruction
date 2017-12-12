import numpy as np
import cv2
from PyQt4 import QtGui

class Calibration():
  def __init__(self, ui, row = 9, col = 6):
    # Link the user interface to handle progress bars and focus.
    self.ui = ui
    self.row = 9
    self.col = 6

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
    #objpoints = [] # 3d point in real world space
    #imgpoints = [] # 2d points in image plane.

    # Parallel version.
    #num_cores = multiprocessing.cpu_count()
    #objpoints, imgpoints = Parallel(n_jobs = num_cores)(delayed(computeChessboardPoints)(image) for image in images)
    #Parallel(n_jobs = num_cores)(delayed(computeChessboardPoints)(image, row, col, criteria, objpoints, imgpoints, objp) for image in images)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    #self.progress = QtGui.QProgressDialog("Calibrating...", "cancel", 0, 10)
    #self.progress.setFocus()
    #self.progress.show()

    #step = 100.0 / len(images)
    #val = 0
    # Basic version.
    for image in images:
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      # Find the chess board corners
      ret, corners = cv2.findChessboardCorners(gray, (self.row, self.col), None)

      # If found, add object points, image points (after refining them)
      if ret:
        objpoints.append(objp)
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        #val += step
        #self.progress.setValue(val)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    #self.progress.close()
    return (mtx, dist)

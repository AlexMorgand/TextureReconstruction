import numpy as np
import cv2
import glob

def checkCalibImage(image):
  row, col = (9, 6)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # termination criteria
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
  objp = np.zeros((col * row, 3), np.float32)
  objp[:, :2] = np.mgrid[0:row, 0:col].T.reshape(-1, 2)

  # Arrays to store object points and image points from all the images.
  objpoints = [] # 3d point in real world space
  imgpoints = [] # 2d points in image plane.

  # Find the chess board corners
  ret, corners = cv2.findChessboardCorners(gray, (row, col), None)

  # If found, add object points, image points (after refining them)
  if ret:
    return True
    #objpoints.append(objp)
    #corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    #imgpoints.append(corners2)
    ## Draw and display the corners
    #gray = cv2.drawChessboardCorners(gray, (row, col), corners2, ret)
    #cv2.imwrite('res', gray, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
  else:
    return False

def calibrateImages(images):
  row, col = (9, 6)
  # termination criteria
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
  objp = np.zeros((col * row, 3), np.float32)
  objp[:, :2] = np.mgrid[0:row, 0:col].T.reshape(-1, 2)

  # Arrays to store object points and image points from all the images.
  objpoints = [] # 3d point in real world space
  imgpoints = [] # 2d points in image plane.

  for image in images:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (row, col), None)

    # If found, add object points, image points (after refining them)
    if ret:
      objpoints.append(objp)
      cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
      imgpoints.append(corners)
  ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
  print(ret, mtx, dist, rvecs, tvecs)

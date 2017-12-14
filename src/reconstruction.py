import cv2
from matplotlib import pyplot as plt
import numpy as np

class Reconstruction():
    def __init__(self, ui, poly, reconstructionImages):
        self.ui = ui
        self.poly = poly
        self.reconstructionImages = reconstructionImages
        # FIXME: do an array of H and poly.
        # FIXME: result image, transform four clicks into a square.

    def alignImage(self):
        # Image 1 is the reference.
        img1 = self.reconstructionImages[0]
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        for i in range(1, len(self.reconstructionImages)):
            img2 = self.reconstructionImages[i]
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            M = self.computeHomography(gray1, gray2)

            for elt in self.poly:
                cv2.circle(img1, (elt[0], elt[1]), 4, (0, 0, 255), 5)
                p = M * np.matrix([[elt[0]], [elt[1]], [1]])
                p[0] = p[0] / p[2]
                p[1] = p[1] / p[2]
                cv2.circle(img2, (p[0], p[1]), 4, (0, 0, 255), 5)

            cv2.imshow("img1", img1)
            cv2.imshow("img2", img2)
            cv2.waitKey(0)


    def computeHomography(self, gray1, gray2):
        # Initiate SIFT detector
        sift = cv2.SIFT()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(gray1, None)
        kp2, des2 = sift.detectAndCompute(gray2, None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        #if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        return M
        #else:
        #    print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)


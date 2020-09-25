import os
import cv2 as cv
import numpy as np


def filtering(target):
    os.chdir(target)
    files = [f for f in os.listdir()]
    files.sort()
    for file in files:
        file_name, ext = os.path.splitext(file)
        if ext != ".bmp":
            continue

        img_gray = cv.imread(file, cv.IMREAD_GRAYSCALE)

        _, img_fil = cv.threshold(img_gray, 63, 0, cv.THRESH_TOZERO)
        # img_fil = cv.adaptiveThreshold(img_fil, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 0)
        img_edge = cv.Canny(img_gray, 3, 15)
        img_fil = cv.subtract(img_fil, img_edge)
        # kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)
        kernel = np.ones((5, 5), np.uint8)
        itr = 2
        # 縮小
        img_fil = cv.erode(img_fil, kernel, iterations=itr)
        # 拡大
        img_fil = cv.dilate(img_fil, kernel, iterations=itr - 1)
        # オープニング
        img_fil = cv.morphologyEx(img_fil, cv.MORPH_OPEN, kernel)
        # クロージング
        cv.imwrite("{0}.tif".format(file_name), img_fil)
        # cv.imwrite("{0}_edge.tif".format(fName), img_edge)


if __name__ == "__main__":
    filtering('dataset/Problem01')

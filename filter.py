import os
import cv2 as cv
import numpy as np

def main():
    img_mask = cv.imread("mask.png", cv.IMREAD_GRAYSCALE)
    # dataType = input("'part'か'problem'を入力\n")
    dataType = 'problem'
    if dataType == "part":
        dataNum = input("01~31を入力\n")
        dataName = "Part{0}".format(dataNum)
        os.chdir("dataset/Parts/" + dataName)
    elif dataType == "problem":
        # dataNum = input("01~05を入力\n")
        dataNum = '01'
        dataName = "dataset/Problem{0}".format(dataNum)
        os.chdir(dataName)
    else:
        print("入力が不正です")
        os.close(0)

    files = [f for f in os.listdir()]
    files.sort()
    for file in files:
        fName, ext = os.path.splitext(file)
        if ext != ".bmp":
            continue

        img_gray = cv.imread(file, cv.IMREAD_GRAYSCALE)

        _, img_fil = cv.threshold(img_gray, 63, 0, cv.THRESH_TOZERO)
        # img_fil = cv.adaptiveThreshold(img_fil, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 0)
        img_edge = cv.Canny(img_gray, 3, 15)
        img_fil = cv.subtract(img_fil, img_edge)
        # kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)
        kernel = np.ones((5,5),np.uint8)
        itr = 2
        # 縮小
        img_fil = cv.erode(img_fil, kernel, iterations=itr)
        # 拡大
        img_fil = cv.dilate(img_fil, kernel, iterations=itr-1)
        # オープニング
        img_fil = cv.morphologyEx(img_fil, cv.MORPH_OPEN, kernel)
        # クロージング
        img_fil = cv.morphologyEx(img_fil, cv.MORPH_CLOSE, kernel)
        # バケツのマスク処理
        # img_fil = cv.bitwise_and(img_fil, img_mask)
        cv.imwrite("{0}.tif".format(fName), img_fil)
        # cv.imwrite("{0}_edge.tif".format(fName), img_edge)

# def test():
    # file = 'mask.png'
    # fName, _ = os.path.splitext(file)
    # img_bgr = cv.imread(file)
    # img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)

    # img = cv.bitwise_not(img_gray)
    # # kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)
    # # # img_blur = cv.blur(img_gray,(5,5))
    # # img_blur = cv.filter2D(img_gray, -1, kernel)
    # cv.imwrite("{0}.png".format(fName), img)

if __name__ == "__main__":
    main()
    # test()
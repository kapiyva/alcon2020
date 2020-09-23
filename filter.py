import os
import cv2
import numpy as np

def main():
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

        img_bgr = cv2.imread(file)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)
        img_fil = cv2.filter2D(img_gray, -1, kernel)
        cv2.imwrite("{0}.tif".format(fName), img_fil)

def test():
    file = 'Problem01_0162.bmp'
    fName, _ = os.path.splitext(file)
    img_bgr = cv2.imread(file)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)
    # img_blur = cv2.blur(img_gray,(5,5))
    img_blur = cv2.filter2D(img_gray, -1, kernel)
    cv2.imwrite("{0}.tif".format(fName), img_blur)

if __name__ == "__main__":
    main()
    # test()
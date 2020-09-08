import os
import cv2

def main():
    dataType = input("'part'か'problem'を入力\n")
    if dataType == "part":
        dataNum = input("01~31を入力\n")
        dataName = "Part{0}".format(dataNum)
        os.chdir("dataset/Parts/" + dataName)
    elif dataType == "problem":
        dataNum = input("01~05を入力\n")
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
        _, img_edge = cv2.Canny(img_gray, 0, 12)
        cv2.imwrite("{0}.tif".format(fName), img_edge)

def test():
    file = "dataset/Problem01/Problem01_0150"
    img_bgr = cv2.imread("{0}.bmp".format(file))
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    img_edge = cv2.Canny(img_gray, 0, 12)
    cv2.imwrite("{0}.tif".format(file), img_edge)
    
if __name__ == "__main__":
    main()
    # test()
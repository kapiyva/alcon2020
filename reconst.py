import os
import pathlib
import cv2
import numpy as np
import matplotlib.pyplot as plt
# from mayavi import mlab, tools


# def show_model(box):
#     src = mlab.pipeline.scalar_field(box)
#     mlab.pipeline.iso_surface(src)
#     mlab.show()

def reconst(threshold=68):
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

    box_raw = [] 
    # box[x][y][z]  zは何枚目の画像かを表す
    files = [f for f in os.listdir()]
    files.sort()
    loaded = 10
    for file in files:
        _, ext = os.path.splitext(file)
        if ext != ".bmp":
            continue

        box_raw.append(cv2.imread(file, cv2.IMREAD_GRAYSCALE))

        if (len(box_raw) / len(files)) > (loaded/100):
            print("{0}% loaded".format(loaded))
            loaded += 10

    box_np = np.array(box_raw)
    # np.set_printoptions(threshold=np.inf)
    box = np.where(box_np < threshold, 0, 1)
    print("voxel shape: {0}".format(box_np.shape))
    return box_np, box

if __name__ == "__main__":
    reconst()
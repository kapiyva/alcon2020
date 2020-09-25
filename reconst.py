import os
import cv2
import numpy as np


def reconst(target, threshold=68):
    defaultPath = os.getcwd()
    os.chdir(target)
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
    os.chdir(defaultPath)
    print(os.getcwd())
    return box_np, box

if __name__ == "__main__":
    reconst("dataset/Problem01")
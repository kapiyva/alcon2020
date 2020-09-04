import os
import pathlib
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def show_model(box):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(box)
    plt.show()


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

box = np.empty(0)
threshold = 100
# box[x][y][z]  zは何枚目の画像かを表す
for i, file in enumerate(os.listdir()):
    _, ext = os.path.splitext(file)
    if ext != ".bmp":
        continue

    if i == 0:
        tmp = np.array(Image.open(file).convert('L'))
        box = np.where(tmp < threshold, False, True)
    else:
        tmp = np.array(Image.open(file).convert('L'))
        img = np.where(tmp < threshold, False, True)
        box = np.dstack([box, img])
        break

show_model(box)

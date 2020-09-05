import os
import pathlib
from PIL import Image
import numpy as np
from mayavi import mlab
from mayavi import tools


def show_model(box):
    src = mlab.pipeline.scalar_field(box)
    outer = mlab.pipeline.iso_surface(src)
    mlab.show()


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
files = [f for f in os.listdir()]
files.sort()
for file in files:
    _, ext = os.path.splitext(file)
    if ext != ".bmp":
        continue

    if box.size == 0:
        tmp = np.array(Image.open(file).convert('L'))
        box = np.where(tmp < threshold, 0, 1)
    else:
        tmp = np.array(Image.open(file).convert('L'))
        img = np.where(tmp < threshold, 0, 1)
        box = np.dstack([box, img])

print(box.shape)
show_model(box)

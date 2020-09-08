import os
import pathlib
from PIL import Image
import numpy as np
from mayavi import mlab, tools


def show_model(box):
    src = mlab.pipeline.scalar_field(box)
    mlab.pipeline.iso_surface(src)
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

box_raw = np.empty(0)
threshold = 70
# box[x][y][z]  zは何枚目の画像かを表す
files = [f for f in os.listdir()]
files.sort()
loaded = 10
for file in files:
    _, ext = os.path.splitext(file)
    if ext != ".bmp":
        continue

    if box_raw.size == 0:
        box_raw = np.array(Image.open(file).convert('L'))

    else:
        img = np.array(Image.open(file).convert('L'))
        box_raw = np.dstack([box_raw, img])

        if (box_raw.shape[2] / len(files)) > (loaded/100):
            print("{0}% loaded".format(loaded))
            loaded += 10
            break


box = np.where(box_raw < threshold, 0, 1)
print(box.shape)
show_model(box)

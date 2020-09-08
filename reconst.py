import os
import pathlib
from PIL import Image
import numpy as np
from mayavi import mlab, tools


def show_model(box):
    src = mlab.pipeline.scalar_field(box)
    mlab.pipeline.iso_surface(src)
    mlab.show()

class Histogram(object):
    def __init__(self):
        self.graph = np.zeros(256)
        self.pixNum = 0
    
    def add_image(self, img):
        for i in range(len(img)):
            for j in range(len(img[i])):
                self.graph[img[i][j]] += 1
                self.pixNum += 1
    
    def get_threshold(self):
        maxS = 0
        for devider in range(1, 256):
            class1 = self.graph[:devider]
            class2 = self.graph[devider:]
            sigW = class1.sum() * np.var(class1) + class2.sum() * np.var(class2)
            sigB = class1.sum() * (np.mean(class1) - np.mean(self.graph)) + class2.sum() * (np.mean(class2) - np.mean(self.graph))
            S = sigB/sigW
            if S > maxS:
                maxS = S
                threshold = devider
        return threshold

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
histogram = Histogram()
for file in files:
    _, ext = os.path.splitext(file)
    if ext != ".bmp":
        continue

    if box_raw.size == 0:
        box_raw = np.array(Image.open(file).convert('L'))
        histogram.add_image(box_raw)

    else:
        img = np.array(Image.open(file).convert('L'))
        histogram.add_image(img)
        box_raw = np.dstack([box_raw, img])

        if (box_raw.shape[2] / len(files)) > (loaded/100):
            print("{0}% loaded".format(loaded))
            loaded += 10


box = np.where(box_raw < histogram.get_threshold(), 0, 1)
#print(histogram.graph)
#print(histogram.graph.shape)
print(box.shape)
show_model(box)

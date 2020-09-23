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
threshold = 70
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
np.set_printoptions(threshold=np.inf)
box = np.where(box_np < threshold, 0, 1)
# show_model(box)

from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from skimage import measure

verts, faces, normals, values = measure.marching_cubes_lewiner(box, 0)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Fancy indexing: `verts[faces]` to generate a collection of triangles
mesh = Poly3DCollection(verts[faces])
mesh.set_edgecolor('lightgreen')
mesh.set_facecolor('darkgreen')

ax.add_collection3d(mesh)

ax.set_xlabel("x-axis")
ax.set_ylabel("y-axis")
ax.set_zlabel("z-axis")
ax.set_xlim(0,300)
ax.set_ylim(0,300)
ax.set_zlim(0,300)

#ax.set_aspect('equal')
ax.view_init(elev=-160, azim=30)
plt.tight_layout()
#plt.savefig('mc_cactus3.jpg',dpi=100)
plt.show()
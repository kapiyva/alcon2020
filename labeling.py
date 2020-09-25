import cc3d
from reconst import reconst
import numpy as np


def labeling(voxel, connect=6):
    d, h, w = voxel.shape()
    connectivity = connect
    labeled_voxel = cc3d.connected_components(voxel, connectivity=connectivity)

    label_count = [0] * np.amax(labeled_voxel)
    thresh_size = 90 //
    # 体積が一定以下のものを除去
    for i in range(d):
        for j in range(h):
            for k in range(w):
                label_count[voxel[i][j][k]] += 1

    for i in range(np.amax(labeled_voxel)):
        if label_count[i]

    return labeled_voxel


if __name__ == '__main__':
    _, voxel = reconst('dataset/Parts/Part01')
    label = labeling(voxel)
    print(np.amax(label))

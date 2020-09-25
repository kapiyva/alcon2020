import cc3d
from reconst import reconst
import numpy as np


def labeling(voxel, connect=6):
    d = voxel.shape[0]
    h = voxel.shape[1]
    w = voxel.shape[2]
    connectivity = connect
    labeled_voxel = cc3d.connected_components(voxel, connectivity=connectivity)

    label_count = [0] * np.amax(labeled_voxel)
    thresh_size = 90 // (0.064 ** 3)
    cutted_label_num = 0
    # 体積が一定以下のものを除去
    for i in range(d):
        for j in range(h):
            for k in range(w):
                label_count[voxel[i][j][k]] += 1

    for i in range(np.amax(labeled_voxel)):
        if label_count[i] < thresh_size:
            labeled_voxel[labeled_voxel == i] = 0
            cutted_label_num += 1

    print("label num: {0}".format(np.amax(labeled_voxel) - cutted_label_num))

    return labeled_voxel


if __name__ == '__main__':
    _, voxel = reconst('dataset/Parts/Part01')
    label = labeling(voxel)
    print(np.amax(label))

import cc3d
from reconst import reconst
import numpy as np


def labeling(voxel, connect=6):
    connectivity = connect
    labeled_voxel = cc3d.connected_components(voxel, connectivity=connectivity)

    # 領域数を出力
    # numbers = np.max(labeled_voxel) - 1
    # print('総領域数は' + numbers + 'つです')

    return labeled_voxel


if __name__ == '__main__':
    _, voxel = reconst('dataset/Parts/Part01')
    label = labeling(voxel)
    print(np.amax(label))

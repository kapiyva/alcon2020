import cc3d
import numpy as np


def labeling(voxel, connect):

    connectivity = connect
    labeled_voxel = cc3d.connected_components(voxel, connectivity=connectivity)

    #領域数を出力
    numbers = np.max(labeled_voxel) - 1
    print('総領域数は' + numbers + 'つです')

    return labeled_voxel
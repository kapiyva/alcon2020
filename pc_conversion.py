import numpy as np
import open3d as o3d
from reconst import reconst

# Input: labeled voxels
# output: individual point coulds for each object labeled
def pc_conversion(voxel):    
    #get voxel maximum = number of labeled components
    num_objs = np.amax(voxel)
    pcdList = []
    for i in range(1, num_objs.astype(int) + 1):
        pcd = o3d.geometry.PointCloud()

        np_points = np.where(voxel == i)
        xyz = np.zeros([len(np_points[0]),3])
        for j in range(len(np_points[0])):
            xyz[j,:] = [np_points[0][j], np_points[1][j], np_points[2][j]]
        
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcdList.append(pcd)
        # o3d.visualization.draw_geometries([pcd])
    return pcdList


if __name__ == '__main__':
    _, voxel = reconst('dataset/Parts/Part04')
    test = np.zeros([3,3,3])
    test[0:2,2] = 1
    pc_conversion(voxel)


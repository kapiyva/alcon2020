import open3d as o3d
import numpy as np

def obj_mesh(path):
  return o3d.io.read_triangle_mesh(path)

def draw_mesh(mesh):

  mesh.paint_uniform_color([1., 0., 0.])
  mesh.compute_vertex_normals()
  o3d.visualization.draw_geometries([mesh])

def mesh2ply(mesh):
  pcd = o3d.geometry.PointCloud()
  pcd.points = o3d.utility.Vector3dVector(np.asarray(mesh.vertices))
  return pcd


def obj_transfer(label_num):
    for i in label_num :
        path = "/Users/alcon/dataset/label" + i + ".obj"
        mesh = obj_mesh(path)
        pcd = mesh2ply(mesh)
        o3d.io.write_point_cloud("pointcloud" + i + ".pcd", pcd)
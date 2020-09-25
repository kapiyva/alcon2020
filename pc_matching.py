# ライブラリインポート
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import copy
import time

start = time.time()

def show(model, scene, model_to_scene_trans=np.identity(4)):
    model_t = copy.deepcopy(model)
    scene_t = copy.deepcopy(scene)

    model_t.paint_uniform_color([1, 0, 0])
    scene_t.paint_uniform_color([0, 0, 1])

    model_t.transform(model_to_scene_trans)

    o3d.visualization.draw_geometries([model_t, scene_t])


# 入力データ
model = o3d.io.read_point_cloud("/Users/nakamura/Desktop/alcon2020/parts_pc/Part14.ply")
scene = o3d.io.read_point_cloud("/Users/nakamura/Desktop/alcon2020/parts_pc/Part22.ply")
trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
model.transform(trans_init)

# いろいろなサイズの元： model点群の1/10を基本サイズsizeにする
size = np.abs((model.get_max_bound() - model.get_min_bound())).max() /10
kdt_n = o3d.geometry.KDTreeSearchParamHybrid(radius=size, max_nn=50)
kdt_f = o3d.geometry.KDTreeSearchParamHybrid(radius=size * 50, max_nn=50)

model.estimate_normals(kdt_n)
scene.estimate_normals(kdt_n)

show(model, scene)


# ダウンサンプリング
model_d = model.voxel_down_sample(size)
scene_d = scene.voxel_down_sample(size)

model_d.estimate_normals(kdt_n)
scene_d.estimate_normals(kdt_n)

show(model_d, scene_d)

# 特徴量計算
model_f = o3d.registration.compute_fpfh_feature(model_d, kdt_f)
scene_f = o3d.registration.compute_fpfh_feature(scene_d, kdt_f)

# 準備
checker = [o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
           o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(size * 2)]

est_ptp = o3d.registration.TransformationEstimationPointToPoint()
est_ptpln = o3d.registration.TransformationEstimationPointToPoint()

criteria = o3d.registration.RANSACConvergenceCriteria(max_iteration=40000, max_validation=500)
# RANSACマッチング
result1 = o3d.registration.registration_ransac_based_on_feature_matching(model_d, scene_d,
                                                                        model_f, scene_f,
                                                                        max_correspondence_distance=size * 2,
                                                                        estimation_method=est_ptp,
                                                                        ransac_n=4,
                                                                        checkers=checker,
                                                                        criteria=criteria)

show(model_d, scene_d, result1.transformation)


# ICPで微修正
result2 = o3d.registration.registration_icp(model, scene, size, result1.transformation, est_ptpln)

show(model, scene, result2.transformation)


process_time = time.time() - start
print(process_time)

print('+' * 40)
print(result1)
print('+' * 40)
print(result2)

# ライブラリインポート
import open3d as o3d
import os
import numpy as np
import copy


# def show(model, scene, model_to_scene_trans=np.identity(4)):
#     model_t = copy.deepcopy(model)
#     scene_t = copy.deepcopy(scene)
#
#     model_t.paint_uniform_color([1, 0, 0])
#     scene_t.paint_uniform_color([0, 0, 1])
#
#     model_t.transform(model_to_scene_trans)
#
#     o3d.visualization.draw_geometries([model_t, scene_t])


def pc_matching(target):
    defalutPath = os.getcwd()
    scene = target
    ans = 0
    # 入力データ
    os.chdir('parts_pc')
    files = [f for f in os.listdir()]
    files.sort()
    min_err = np.inf
    for file in files:
        index_str, ext = os.path.splitext(file)
        if ext != '.pcd':
            print(file)
            continue
        model = o3d.io.read_point_cloud(file)
        trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                                 [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
        model.transform(trans_init)

        # いろいろなサイズの元： model点群の1/10を基本サイズsizeにする
        size = np.abs((model.get_max_bound() - model.get_min_bound())).max() / 10
        kdt_n = o3d.geometry.KDTreeSearchParamHybrid(radius=size, max_nn=50)
        kdt_f = o3d.geometry.KDTreeSearchParamHybrid(radius=size * 50, max_nn=50)

        o3d.geometry.PointCloud.estimate_normals(model, kdt_n)
        o3d.geometry.PointCloud.estimate_normals(scene, kdt_n)
        # show(model, scene)

        # ダウンサンプリング
        model_d = o3d.geometry.PointCloud.voxel_down_sample(model, size)
        scene_d = o3d.geometry.PointCloud.voxel_down_sample(scene, size)
        o3d.geometry.PointCloud.estimate_normals(model_d, kdt_n)
        o3d.geometry.PointCloud.estimate_normals(scene_d, kdt_n)
        # show(model_d, scene_d)

        # 特徴量計算
        model_f = o3d.registration.compute_fpfh_feature(model_d, kdt_f)
        scene_f = o3d.registration.compute_fpfh_feature(scene_d, kdt_f)

        # 準備
        checker = [o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
                   o3d.registration.CorrespondenceCheckerBasedOnDistance(size * 2)]

        est_ptp = o3d.registration.TransformationEstimationPointToPoint()
        est_ptpln = o3d.registration.TransformationEstimationPointToPlane()

        criteria = o3d.registration.RANSACConvergenceCriteria(max_iteration=40000,max_validation=500)
        # RANSACマッチング
        result1 = o3d.registration.registration_ransac_based_on_feature_matching(model_d, scene_d,
                                                                                 model_f, scene_f,
                                                                                 max_correspondence_distance=size * 2,
                                                                                 estimation_method=est_ptp,
                                                                                 ransac_n=4,
                                                                                 checkers=checker,
                                                                                 criteria=criteria)
        # show(model_d, scene_d, result1.transformation)

        # ICPで微修正
        # result2 = o3d.registration.registration_icp(model, scene, size, result1.transformation, est_ptpln)
        if result1.inlier_rmse < min_err and result1.inlier_rmse > 0:
            min_err = result1.inlier_rmse
            ans = int(index_str)
        os.chdir(defalutPath)
    return ans


if __name__ == '__main__':
    model = o3d.io.read_point_cloud('parts_pc/1.pcd')
    ans = pc_matching(model)
    print(ans)

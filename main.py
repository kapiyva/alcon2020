from . import *
import numpy as np

def main():
    target = 'dataset/Problem01'
    # 前処理
    filter(target)
    # 三次元復元してnp.arrayに変換
    voxel = reconst(target)
    # 塊ごとにラベルを振っていく
    labeled_voxel = labeling(voxel)
    # 塊ごとの点群の配列
    part_pc = pc_conversion(labeled_voxel)
    count = [0]*31
    for part in part_pc:
        p_ans = pc_matching(part)
        count[p_ans] += 1

print(count)
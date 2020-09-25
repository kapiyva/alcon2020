from filter import filtering
from reconst import reconst
from labeling import labeling
from pc_conversion import pc_conversion
from pc_matching import pc_matching


def main():
    target = 'dataset/Problem01'
    # 前処理
    filtering(target)
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

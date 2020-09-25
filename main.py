from filter import filtering
from reconst import reconst
from labeling import labeling
from pc_conversion import pc_conversion
from pc_matching import pc_matching


def main():
    target = 'dataset/Problem01'
    # 前処理
    print('filtering')
    # filtering(target)
    # 三次元復元してnp.arrayに変換
    print("reconst")
    _, voxel = reconst(target)
    # 塊ごとにラベルを振っていく
    print("labeling")
    labeled_voxel = labeling(voxel)
    # 塊ごとの点群の配列
    print("conversion")
    part_pc = pc_conversion(labeled_voxel)
    count = [0]*32
    print("matching")
    for part in part_pc:
        p_ans = pc_matching(part)
        count[p_ans] += 1

    print(count)

if __name__ == '__main__':
    main()
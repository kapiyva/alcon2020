import numpy as np

def rasterScan(voxel):
    print(voxel.shape)
    z, x, y = voxel.shape
    label = 1
    labelBox = np.full_like(voxel, np.inf)
    lookUpTable = {1:1,2:2}
    print(type(lookUpTable))
    for i in range(z):
        for j in range(x):
            for k in range(y):
                min_label = np.inf
                if voxel[i][j][k] == 0:
                    continue
                # 6結合でラスタスキャン
                if k > 0:
                    if voxel[i][j][k-1] == 1:
                        min_label = min(min_label, labelBox[i][j][k-1])
                        lookUpTable[labelBox[i][j][k-1]] = min_label
                if j > 0:
                    if voxel[i][j-1][k] == 1:
                        min_label = min(min_label, labelBox[i][j-1][k])
                        lookUpTable[labelBox[i][j-1][k]] = min_label
                if i > 0:
                    if voxel[i-1][j][k] == 1:
                        min_label = min(min_label, labelBox[i-1][j][k])
                        lookUpTable[labelBox[i-1][j][k]] = min_label
                
                if min_label == np.inf:
                    labelBox[i][j][k] = label
                    label += 1
                else:
                    labelBox[i][j][k] = min_label
    labelBox[labelBox == np.inf] = 0 
    for i in lookUpTable:
        labelBox[labelBox == i] = lookUpTable[i]
    return labelBox, lookUpTable
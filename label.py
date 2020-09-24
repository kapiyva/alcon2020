import numpy as np

from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt 
import numpy as np
plt.rcParams["font.size"] = 16

data=np.arange(25).reshape((5,5))
 
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(231, projection='3d')
ax2 = fig.add_subplot(232, projection='3d')
ax3 = fig.add_subplot(233, projection='3d')
ax4 = fig.add_subplot(234, projection='3d')
ax5 = fig.add_subplot(235, projection='3d')
ax6 = fig.add_subplot(236, projection='3d')

x, y, z = np.indices((5, 5, 1))
v1 = (z == 0)
v2 = (x<3) & (y<4) #data[:3,:4]
v3 = (x%2==0) #data[::2,:]
v4 = (y%2==1) #data[:,1::2]
v5 = (x==4) & (y==4) #data[-1,-1]
v6 = (x>2) & (y>1) #data[-2:,-3:]
v7 = (x<3) & (y<4) #data[2::-1,3::-1]

for aa in (ax1, ax2, ax3, ax4, ax5, ax6):
    aa.voxels(v1, facecolors='pink', edgecolor='grey')
    aa.set_axis_off()
    aa.view_init(90, 270)
    aa.set_zlim(0,1000)
    aa.text2D(0.4, 0.15, "axis 0", transform=aa.transAxes)
    aa.text2D(0.15, 0.45, "axis 1", transform=aa.transAxes,rotation=90)

ax1.voxels(v2, facecolors='lime', edgecolor='green')
ax2.voxels(v3, facecolors='lime', edgecolor='green')
ax3.voxels(v4, facecolors='lime', edgecolor='green')
ax4.voxels(v5, facecolors='lime', edgecolor='green')
ax5.voxels(v6, facecolors='lime', edgecolor='green')
ax6.voxels(v7, facecolors='lime', edgecolor='green')

ax1.set_title('data[:3,:4]')
ax2.set_title('data[::2,:]')
ax3.set_title('data[:,1::2]')
ax4.set_title('data[-1,-1]')
ax5.set_title('data[-2:,-3:]')
ax6.set_title('data[2::-1,3::-1]')

fig.suptitle('Visualization of slice', fontsize=24)
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig('slice_voxel.png',dpi=135)
plt.show()
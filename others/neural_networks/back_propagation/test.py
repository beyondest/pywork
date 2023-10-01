import numpy as np
import math
import mypack as my
import random as ran
import matplotlib.pyplot as plt
a=[[-1,2],
   ]
b=[3,6]
c=[1,4]
h=np.float64(3.5)
g=np.float64(3.6)
m=np.vstack((b,c))
x=[i for i in range(6)]
y=[i+10 for i in range(6)]
z=[np.reshape([1,2],(1,2)),np.reshape([2,3],(1,2)),np.reshape([4,5],(1,2))]

fig,axs=plt.subplots(2,2)
fig.set_facecolor('red')
for i in range(2):
   for j in range(2):
      if i==1:
         axs[i][j].scatter(x,z)
      else:
         axs[i][j].scatter(x,y)
      axs[i][j].set_xlabel('x')
      axs[i][j].set_ylabel('y')
      axs[i][j].set_title(f'[{i},{j}]')
plt.show()


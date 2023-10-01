import numpy as np
import random as ran
import mypack as my
import matplotlib.pyplot as plt
import math
target=1
def target_func(x):
    global target
    if target==0:
       return x**2 
    if target==1:
        return 10*math.sin(x)
    if target==2:
        return math.log(x)
    if target==3:
        return x**3-2*x
train_len=1000
test_len=30

fig,axs=my.plt_init(2,2)

x_list,y_list=my.make_data(train_len,target_func,1,[-1.5,1.5],'random')
general_X=np.array([x_list]).astype(np.float64)
general_Y=np.array([y_list]).astype(np.float64)
my.plt_axeinit(x_list,y_list,'data for learning',axs[0][0])

x_list,y_list=my.make_data(test_len,target_func,0,[-1.5,1.5],'normal')
test_X=np.array([x_list]).astype(np.float64)
test_Y=np.array([y_list]).astype(np.float64)
my.plt_axeinit(x_list,y_list,'data for test, also the target img',axs[0][1])




w_list,b_list=my.net_init(general_X.shape[0],general_Y.shape[0],[10,10,10,1])


w_list,b_list,record_list1=my.train(general_X,general_Y,1,w_list,b_list,0.001,0.001,'train',times=30)
record_list2,accuracy,final_out_list=my.train(test_X,test_Y,1,w_list,b_list,0,0,'test',permit=0.1)
x=[i for i in range(len(record_list1))]
y=record_list1
print('record1=',record_list1)

print('accuracy=',accuracy)
print(len(final_out_list))
print(final_out_list[0].shape)

my.plt_axeinit(x,y,'train_process',axs[1][0],'train_times','general_cost')
my.plt_axeinit(x_list,final_out_list,'fit function img',axs[1][1])

plt.show()


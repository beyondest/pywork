import math
import numpy as np
import os
import random as ran
import matplotlib.pyplot as plt
morse_dict = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/', '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'}

def mypow(mat_x)->np.ndarray:
    rows=mat_x.shape[0]
    columns=mat_x.shape[1]
    out=np.copy(mat_x)
    for i in range(rows):
        for j in range(columns):
            if mat_x[i][j]<0:
                out[i][j]=-pow(-mat_x[i][j],1/3)
            elif mat_x[i][j]>0:
                out[i][j]=pow(mat_x[i][j],1/3)
            else:
                out[i][j]=0
    return out
def mypow2(mat_x):
    rows=mat_x.shape[0]
    columns=mat_x.shape[1]
    out=np.copy(mat_x)
    for i in range(rows):
        for j in range(columns):
            if mat_x[i][j]<0:
                out[i][j]=1/3*pow(-mat_x[i][j],-2/3)
            elif mat_x[i][j]>0:
                out[i][j]=1/3*pow(mat_x[i][j],-2/3)
            else:
                out[i][j]=0
    return out
        
def activate_func(x)->tuple:
    '''return x**(1/3),diff(x)'''
    def sigmoid(m):
        return 1/(1+np.exp(-m))
    return sigmoid(x),sigmoid(x)*(1-sigmoid(x))

def cost_func(mat_x:np.ndarray,mat_y:np.ndarray)->tuple:
    '''return cost_list,each in list is num=1/2(xi-yi)^2,diff(x,y)
    @costfunc=1/2sum_i (x_i-y_i)^2'''
    cols=mat_x.shape[1]
    rows=mat_x.shape[0]
    out_list=[]
    
    for i in range(cols):
        s=0
        for j in range(rows):
            s+=0.5*(mat_x[j][i]-mat_y[j][i])**2
        out_list.append(s)
    
    return out_list,mat_x-mat_y




def find_key(value,dictt:dict):
    keys=list(dictt.keys())
    values=list(dictt.values())
    return keys[values.index(value)]


def transto_code(s,dictt:dict=morse_dict)->tuple:
    '''code split by ' ',one ' ' one character'''
    out=''
    miss=[]
    for i in s:
        if i in dictt:
            out+=dictt[i]+' '
        elif i.upper() in dictt:
            out+=dictt[i.upper()]+' '
        else:
            miss.append(i)
    return out,miss
def translate(code:str,dictt:dict=morse_dict)->tuple:
    '''code split by ' ',one '' one character '''
    out=''
    dictt=morse_dict
    code_list=code.split()
    miss=[]
    for i in code_list:
        if i in dictt.values():
            out+=find_key(i,dictt)
        else:
            miss.append(i)
    return out,miss

def read_data(abs_path:str,mode:str='num',split:str=',')->tuple:
    '''each odd line in file will be turned into a colume vector in general_X,
    each even line in file will be turned into a colume vector in general_Y,
    can only record each num, notice that each num is splited by split'''
    fp=open(abs_path)
    general_X=[]
    general_Y=[]
    count=0
    for each_line in fp.readlines():
        count+=1
        each_list=each_line.strip().split(split)
        if count%2!=0:
            general_X.append([eval(i) for i in each_list if type(eval(i))==int or type(eval(i))==float] )
        else:
            general_Y.append([eval(i) for i in each_list if type(eval(i))==int or type(eval(i))==float])
    return general_X,general_Y
def make_data(dim:int,func,bias_interval,x_interval:list,mode:str='random')->tuple:
    '''return x_list,y_list,len is dim;
    @mode='random'or'normal' '''
    seed_list=[]
    out_list=[]
    if mode=='random':
        for i in range(dim):
            seed=ran.uniform(x_interval[0],x_interval[1])
            seed_list.append(seed)
            bias=ran.uniform(-1/2*bias_interval,1/2*bias_interval)
            out_list.append(func(seed)+bias)
    elif mode=='normal':
        step=(x_interval[1]-x_interval[0])/dim
        seed=x_interval[0]
        for i in range(dim):
            seed_list.append(seed)
            bias=ran.uniform(-1/2*bias_interval,1/2*bias_interval)
            out_list.append(func(seed)+bias)
            seed+=step
    return seed_list,out_list

def net_init(x_rows:int,y_rows:int,unit_list:list=[3,5,-1])->tuple:
    '''len(unit_list)=layers, unit_list[-1]=y_rows,return w_list,b_list,notice that w_list[l] is W^l'''
    layers=len(unit_list)
    unit_list[-1]=y_rows
    unit_list.insert(0,x_rows)
    w_list=[0]
    b_list=[0]
    for l in range(1,layers+1):
        weight_l=np.random.uniform(-50,50,(unit_list[l],unit_list[l-1]))
        b_l=np.random.uniform(-50,50,(unit_list[l],1))
        w_list.append(weight_l)
        b_list.append(b_l)
    return w_list,b_list
    
def normalize(input_mat:np.ndarray,compress_interval:list=[-2,2])->np.ndarray:
    '''compress to [-2,2]'''
    max_ele=np.max(input_mat)
    min_ele=np.min(input_mat)
    actual_len=max_ele-min_ele
    if actual_len!=0:
        actual_center=1/2*(max_ele+min_ele)
        target_len=compress_interval[1]-compress_interval[0]
        target_center=1/2*(compress_interval[1]+compress_interval[0])
        center_bias=actual_center-target_center
        zoom_rate=target_len/actual_len
        out_mat=zoom_rate*(input_mat-center_bias)
        return out_mat
    else:
        return 0*input_mat
    


    
def train(general_X:np.ndarray,
          general_Y:np.ndarray,
          batch_len:int,
          w_list:list,
          b_list:list,
          alpha_w,
          alpha_b,
          mode:str='train',
          times:int=1,
          permit:int=1)->tuple:
    '''how many batches decides batch_len;
    @mode=train means train,
    return w_list,b_list,record_list,
    @mode=test means test,
    return record_list,accuracy,out_list[layers] 
    @permit is interval of bias between final_out and test_out
    @notice that batch_len decides the effect of result, both train and test, batch_len is important
    '''
    #init_len
    general_len=general_X.shape[1]
    if general_len%batch_len==0:
        batch=general_len//batch_len
    else:
        batch=general_len//batch_len+1
    layers=len(w_list)-1
    #init_list
    out_list=[0]
    in_list=[0]
    nabla_list=[0]
    record_list=[]
    for j in range(1,layers+1):
        out_list.append(0)
        in_list.append(0)
        nabla_list.append(0)
    #train_mode
    if mode=='train':
        for time in range(times):
            #update W by each batch
            for i in range(batch):
                
                #cut the batch to input
                start=i*batch_len
                end=(i+1)*batch_len
                if end>general_len:
                    end=general_len
                timely_len=end-start
                batch_X=general_X[:,start:end]
                batch_Y=general_Y[:,start:end]
                out_list[0]=batch_X
                
                #foward propagation
                
                for j in range(1,layers+1):
                    B_j=np.repeat(b_list[j],timely_len,axis=1)
                    in_list[j]=w_list[j]@out_list[j-1]+B_j
                    #last layer activate_func is y=x itself
                    if j!=layers:
                        in_list[j]=normalize(in_list[j])
                        out_list[j]=activate_func(in_list[j])[0]
                    else:
                        out_list[j]=in_list[j]
                
                
                #back propagation
                
                nabla_list[layers]=cost_func(out_list[layers],batch_Y)[1]
                
                for j in range(layers,0,-1):
                    #last layer !!!
                    if j!=layers:
                        delta_j=nabla_list[j]*activate_func(in_list[j])[1]
                    else:
                        delta_j=nabla_list[j]*1
                    dw=1/timely_len*(delta_j@out_list[j-1].transpose())
                    db=np.reshape(np.average(delta_j,axis=1),(delta_j.shape[0],1))
                    
                    w_list[j]-=alpha_w*dw
                    b_list[j]-=alpha_b*db
                    #notice that I deliver not the delta, but the nabla
                    nabla_list[j-1]=w_list[j].transpose()@delta_j
                    
            #record the wrong, use general_X
            
            out_list[0]=general_X
            for j in range(1,layers+1):
                
                in_list[j]=w_list[j]@out_list[j-1]+b_list[j]
                if j!=layers:
                    in_list[j]=normalize(in_list[j])
                    out_list[j]=activate_func(in_list[j])[0]
                else:
                    out_list[j]=in_list[j]
            wrong=1/general_len*sum(cost_func(out_list[layers],general_Y)[0])
            
            record_list.append(wrong)
        return  w_list,b_list,record_list
    #test_mode
    elif mode=='test':
        right=0
        final_out_list=[]
        
        
        for i in range(batch):
            #cut for the batch
            start=i*batch_len
            end=(i+1)*batch_len
            if end>general_len:
                end=general_len
            timely_len=end-start
            batch_X=general_X[:,start:end]
            batch_Y=general_Y[:,start:end]
            out_list[0]=batch_X
            
            
            #foward propagation
            for j in range(1,layers+1):
                
                in_list[j]=w_list[j]@out_list[j-1]+b_list[j]
                if j!=layers:
                    in_list[j]=normalize(in_list[j])
                    out_list[j]=activate_func(in_list[j])[0]
                else:
                    out_list[j]=in_list[j]
            #record the wrong
            wrong=1/timely_len*sum(cost_func(out_list[layers],batch_Y)[0])
            if wrong<permit:
                right+=1
            record_list.append(wrong)
            final_out_list.append(out_list[layers])
            
        accuracy=right/batch
        return record_list,accuracy,final_out_list

def plt_init(rows,cols)->tuple:
    '''return fig,axs'''
    fig,axs=plt.subplots(rows,cols)
    fig.set_dpi(100)
    fig.set_figwidth(50)
    fig.set_figheight(50)
    return fig,axs

def plt_axeinit(x_list:list,
                y_list:list,
                name:str,
                target_axe:plt.Axes,
                x_label:str='x',
                y_label:str='y')->None:
    '''set target_axe'''
    target_axe.set_title(name)
    target_axe.set_xlabel(x_label)
    target_axe.set_ylabel(y_label)
    target_axe.scatter(x_list,y_list,s=3)
    return None



    

if __name__ == '__main__':
    net_init(5,2,[4,3,1])





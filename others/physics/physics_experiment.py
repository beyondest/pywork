
import math 

storage={'data1':[],'data2':[],'out':[],'average':0,'variance':0,'l_uncertainty':0,'k(data1=y,data2=x)':0,'b(data1=y,data2=x)':0}
func='data1+data2'
ld1=0
ld2=0
ld=0
s=0
c=0.061
sigma_xiyi=0
sigma_xi2=0
def func_load():
    global func
    func=input('out=func(data1,data2)(e.g. data1+data2)=')
def calculate(data1,data2):
    return eval(func)
def data_load():
    global ld1,ld2
    read_data1=input("data1(split by ',')=")
    read_data2=input("data2(split by ',')=")
    storage['data1'].extend([float(i) for i in list(read_data1.split(','))])
    storage['data2'].extend([float(i) for i in list(read_data2.split(','))])
    ld1=len(storage['data1'])
    ld2=len(storage['data2'])
def check_data_size():
    while ld1!=ld2:
        if ld1<ld2:
            answer=input(f'size data1={ld1}<size data2={ld2},reload or cut=(r/c)')
            if answer=='r':
                data_clear()
                data_load()
            else:
                del storage['data2'][ld1:]
                return 0
        else:
            answer=input(f'size data1={ld1}>size data2={ld2},reload or cut=(r/c)')
            if answer=='r':
                data_clear()
                data_load()
            else:
                del storage['data1'][ld2:]
                return 0
    print(f'size data1=size data2={ld1}')                   
def data_clear():
    storage['data1'].clear()            
    storage['data2'].clear()          

data_load()
check_data_size()
func_load()
ld=min(ld1,ld2)
storage['out']=[calculate(storage['data1'][i],storage['data2'][i]) for i in range(ld)]
storage['average']=sum(storage['out'])/ld
for i in storage['out']:
    s+=(i-storage['average'])**2
storage['variance']=s**0.5/ld
storage['l_uncertainty']=(s/ld/(ld-1))**0.5
yba=sum(storage['data1'])/ld
xba=sum(storage['data2'])/ld
for i in range(ld):
    sigma_xiyi+=storage['data1'][i]*storage['data2'][i]
    sigma_xi2+=storage['data2'][i]**2
if ld*xba**2-sigma_xi2!=0:
    storage['k(data1=y,data2=x)']=(ld*xba*yba-sigma_xiyi)/(ld*xba**2-sigma_xi2)
    storage['b(data1=y,data2=x)']=yba-storage['k(data1=y,data2=x)']*xba
else:
    storage['k(data1=y,data2=x)']='denominator=0'
    storage['b(data1=y,data2=x)']='denominator=0'
print(storage)
    
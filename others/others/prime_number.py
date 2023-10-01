num=input("input 10 integers,split by ',':")
num=num.split(',')
num=[int(i) for i in num]
out=[]
def check_prime(a):
    if a<2:
        return 0
    for i in range(2,a):
        if a%i==0:
            break
    else:
        out.append(a)
for i in num:
    check_prime(i)
print(f'prime={out}')
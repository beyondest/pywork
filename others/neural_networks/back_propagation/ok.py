# -*- coding:utf-8 -*-
import numpy as np
 
def loaddataset(filename):
	fp = open(filename)
 
	#�������
	dataset = []
 
	#��ű�ǩ
	labelset = []
	for i in fp.readlines():
		a = i.strip().split()
 
		#ÿ�������е����һ���Ǳ�ǩ
		dataset.append([float(j) for j in a[:len(a)-1]])
		labelset.append(int(float(a[-1])))
	return dataset, labelset
 
 
#xΪ�������Ԫ������yΪ������Ԫ������z�������Ԫ����
def parameter_initialization(x, y, z):
 
	#������ֵ,dtype=[[1,2,4,~]]
	value1 = np.random.randint(-5, 5, (1, y)).astype(np.float64)
 
	#�������ֵ
	value2 = np.random.randint(-5, 5, (1, z)).astype(np.float64)
 
	#����������������Ȩ��
	weight1 = np.random.randint(-5, 5, (x, y)).astype(np.float64)
 
	#����������������Ȩ��
	weight2 = np.random.randint(-5, 5, (y, z)).astype(np.float64)
 
	return weight1, weight2, value1, value2
 
def sigmoid(z):
	return 1 / (1 + np.exp(-z))
 

#weight1:����������������Ȩ��
#weight2:����������������Ȩ��
#value1:������ֵ
#value2:�������ֵ

def trainning(dataset, labelset, weight1, weight2, value1, value2):
	#xΪ����,or learning rate
	x = 0.01
	for i in range(len(dataset)):
		#��������
		inputset = np.mat(dataset[i]).astype(np.float64)
		#���ݱ�ǩ
		outputset = np.mat(labelset[i]).astype(np.float64)
		#��������,only one line one time,size matched,cause x=len(dataset[0])
		input1 = np.dot(inputset, weight1).astype(np.float64)
		#�������,minus threshold then activate
		output2 = sigmoid(input1 - value1).astype(np.float64)
		#���������
		input2 = np.dot(output2, weight2).astype(np.float64)
		#��������
		output3 = sigmoid(input2 - value2).astype(np.float64)
 
		#���¹�ʽ�ɾ��������ʾ
		a = np.multiply(output3, 1 - output3)
		g = np.multiply(a, outputset - output3)
		#b is delta 2,cause only 2 layers
		b = np.dot(g, np.transpose(weight2))
		c = np.multiply(output2, 1 - output2)
		#e is delta 1
		e = np.multiply(b, c)
 
		value1_change = -x * e
		value2_change = -x * g
		weight1_change = x * np.dot(np.transpose(inputset), e)
		weight2_change = x * np.dot(np.transpose(output2), g)
 
		#���²���
		value1 += value1_change
		value2 += value2_change
		weight1 += weight1_change
		weight2 += weight2_change
	return weight1, weight2, value1, value2
 
def testing(dataset, labelset, weight1, weight2, value1, value2):
	#��¼Ԥ����ȷ�ĸ���
	rightcount = 0
	for i in range(len(dataset)):
		#����ÿһ������ͨ��������·���Ԥ��ֵ
		inputset = np.mat(dataset[i]).astype(np.float64)
		outputset = np.mat(labelset[i]).astype(np.float64)
		output2 = sigmoid(np.dot(inputset, weight1) - value1)
		output3 = sigmoid(np.dot(output2, weight2) - value2)
 
		#ȷ����Ԥ���ǩ,this is classifacation prediction
		if output3 >0.5 :
			flag = 2
		else:
			flag = 1
		if outputset == flag:
			rightcount += 1
		#���Ԥ����
		print(f"predict={flag}   actual={outputset}")
	#������ȷ��
	return rightcount / len(dataset)
 
if __name__ == '__main__':
	dataset, labelset = loaddataset('D:/data/data.txt')	
	
	weight1, weight2, value1, value2 = parameter_initialization(len(dataset[0]), len(dataset[0]), 1)
	#training i times
	for i in range(5):
		weight1, weight2, value1, value2 = trainning(dataset, labelset, weight1, weight2, value1, value2)
	rate = testing(dataset, labelset, weight1, weight2, value1, value2)
	print("accuracy=%f"%(rate))
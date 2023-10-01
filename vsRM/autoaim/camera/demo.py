#coding=utf-8
import mvsdk
import cv2
import platform
import numpy as np
import os
import control
fps=50
interval_fps=1
out_path='D:/tmdvs/pywork/vsRM/spare'


def main_loop():
    
	# ö�����
	DevList = mvsdk.CameraEnumerateDevice()
	nDev = len(DevList)
	if nDev < 1:
		print("No camera was found!")
		return
		
	for i, DevInfo in enumerate(DevList):
		print("{}: {} {}".format(i, DevInfo.GetFriendlyName(), DevInfo.GetPortType()))
	i = 0 if nDev == 1 else int(input("Select camera: "))
	DevInfo = DevList[i]
	#print(DevInfo)
	
	# �����
	hCamera = 0
	try:
		hCamera = mvsdk.CameraInit(DevInfo, -1, -1)
	except mvsdk.CameraException as e:
		print("CameraInit Failed({}): {}".format(e.error_code, e.message) )
		return

	# ��ȡ�����������
	cap = mvsdk.CameraGetCapability(hCamera)

	
	# �ж��Ǻڰ�������ǲ�ɫ���
	monoCamera = (cap.sIspCapacity.bMonoSensor != 0)

	# �ڰ������ISPֱ�����MONO���ݣ���������չ��R=G=B��24λ�Ҷ�
	if monoCamera:
		mvsdk.CameraSetIspOutFormat(hCamera, mvsdk.CAMERA_MEDIA_TYPE_MONO8)

	# ���ģʽ�л��������ɼ�
	mvsdk.CameraSetTriggerMode(hCamera, 0)
	mvsdk.CameraSetGamma(hCamera,30)
	# �ֶ��ع⣬�ع�ʱ�䵥λ΢�룬1/fps*1000**2
	mvsdk.CameraSetAeState(hCamera, 0)
	mvsdk.CameraSetExposureTime(hCamera, 10*1000)
	info=control.get_all(hCamera)
	control.print_getall(info)
	# ��SDK�ڲ�ȡͼ�߳̿�ʼ����
	mvsdk.CameraPlay(hCamera)
	
	# ����RGB buffer����Ĵ�С������ֱ�Ӱ�����������ֱ���������
	# ֮����*3������Ϊprawdata����isp����rgb��Ҫ*3����prawdata�ǲ���Ҫ*3�ģ���isp�������ҲҪ����buffer����*3
	FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * (1 if monoCamera else 3)

	# ����RGB buffer���������ISP�����ͼ��
	# ��ע����������䵽PC�˵���RAW���ݣ���PC��ͨ�����ISPתΪRGB���ݣ�����Ǻڰ�����Ͳ���Ҫת����ʽ������ISP����������������Ҳ��Ҫ�������buffer��
	# 16 ���ڴ�����йأ���raw��ʽ�޹�
	pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)
	countt=-1
    #��interval_fps֡����ͼƬһ��
    
	while (cv2.waitKey(1) & 0xFF) != 27:
		countt=countt+1
		# �����ȡһ֡ͼƬ
		try:
			pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
			mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
			mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)
			
			# windows��ȡ����ͼ�����������µߵ��ģ���BMP��ʽ��š�ת����opencv����Ҫ���·�ת������
			# linux��ֱ��������ģ�����Ҫ���·�ת
			if platform.system() == "Windows":
				mvsdk.CameraFlipFrameBuffer(pFrameBuffer, FrameHead, 1)
			
			# ��ʱͼƬ�Ѿ��洢��pFrameBuffer�У����ڲ�ɫ���pFrameBuffer=RGB���ݣ��ڰ����pFrameBuffer=8λ�Ҷ�����
			# ��pFrameBufferת����opencv��ͼ���ʽ�Խ��к����㷨����
			
			frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)

			frame = np.frombuffer(frame_data, dtype=np.uint8)
			
			frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3) )

			if countt%interval_fps==0:
				filepath=os.path.join(out_path,str(countt)+'.png')
				cv2.imwrite(filepath,frame)

			#frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_LINEAR)
			cv2.imshow("Press q to end", frame)

			
		except mvsdk.CameraException as e:
			if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
				print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message) )
				

	# �ر����
	mvsdk.CameraUnInit(hCamera)

	# �ͷ�֡����
	mvsdk.CameraAlignFree(pFrameBuffer)

def main():
	try:
		main_loop()
	finally:
		cv2.destroyAllWindows()
def PrintCapbility(cap):
	for i in range(cap.iTriggerDesc):
		desc = cap.pTriggerDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iImageSizeDesc):
		desc = cap.pImageSizeDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iClrTempDesc):
		desc = cap.pClrTempDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iMediaTypeDesc):
		desc = cap.pMediaTypeDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iFrameSpeedDesc):
		desc = cap.pFrameSpeedDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iPackLenDesc):
		desc = cap.pPackLenDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iPresetLut):
		desc = cap.pPresetLutDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iAeAlmSwDesc):
		desc = cap.pAeAlmSwDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iAeAlmHdDesc):
		desc = cap.pAeAlmHdDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iBayerDecAlmSwDesc):
		desc = cap.pBayerDecAlmSwDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )
	for i in range(cap.iBayerDecAlmHdDesc):
		desc = cap.pBayerDecAlmHdDesc[i]
		print("{}: {}".format(desc.iIndex, desc.GetDescription()) )

main()

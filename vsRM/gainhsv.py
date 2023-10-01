#coding=utf-8
import cv2
import matplotlib.pyplot as plt
import numpy as np
'''
hsv(rm official blue):
min:83, 70, 194
max:114, 255, 255
'''
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# 读取图片并缩放方便显示
img = cv2.imread('D:/tmdvs/pywork/vsRM/spare/20.png')
img = cv2.resize(img, (320, 256), interpolation=cv2.INTER_AREA)

# img1 = cv2.imread('test.jpg')
# img1 = cv2.resize(img1, (320, 256), interpolation=cv2.INTER_AREA)
# BGR转化为HSV
HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# HSV1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

def trackChaned(x):
    pass


cv2.namedWindow('H',cv2.WINDOW_NORMAL)
cv2.namedWindow('S',cv2.WINDOW_NORMAL)
cv2.namedWindow('V',cv2.WINDOW_NORMAL)
cv2.createTrackbar("Max", "H", 0, 255, trackChaned)
cv2.createTrackbar("Min", "H", 0, 255, trackChaned)

cv2.createTrackbar("Max", "S", 0, 255, trackChaned)
cv2.createTrackbar("Min", "S", 0, 255, trackChaned)

cv2.createTrackbar("Max", "V", 0, 255, trackChaned)
cv2.createTrackbar("Min", "V", 0, 255, trackChaned)

while 1:
    hul = cv2.getTrackbarPos("Max", "H")
    huh = cv2.getTrackbarPos("Min", "H")

    sul = cv2.getTrackbarPos("Max", "S")
    suh = cv2.getTrackbarPos("Min", "S")

    vul = cv2.getTrackbarPos("Max", "V")
    vuh = cv2.getTrackbarPos("Min", "V")
    upper = np.array([hul, sul, vul], dtype="uint8")  # [70, 0, 250]
    lower = np.array([huh, suh, vuh], dtype="uint8")
    img = cv2.inRange(HSV, lower, upper)
    # img1 = cv2.inRange(HSV1, lower, upper)
    height, width = img.shape[:2]
    size = (int(width * 1), int(height * 1))
    # 缩放
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    preprocess_Img = cv2.erode(img, kernel)
    # preprocess_Img1 = cv2.erode(img1, kernel)
    cv2.imshow("wocaomn", preprocess_Img)
    # cv2.imshow("wocaomn1", preprocess_Img1)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()

# ----------------------------------------------------------取并集，耗时，但更完整，酌情使用

#
# cv2.namedWindow('H')
# cv2.namedWindow('S')
# cv2.namedWindow('V')
# cv2.createTrackbar("Max", "H", 0, 255, trackChaned)
# cv2.createTrackbar("Min", "H", 0, 255, trackChaned)
#
# cv2.createTrackbar("Max", "S", 0, 255, trackChaned)
# cv2.createTrackbar("Min", "S", 0, 255, trackChaned)
#
# cv2.createTrackbar("Max", "V", 0, 255, trackChaned)
# cv2.createTrackbar("Min", "V", 0, 255, trackChaned)
#
# cv2.namedWindow('H2')
# cv2.namedWindow('S2')
# cv2.namedWindow('V2')
# cv2.createTrackbar("Max", "H2", 0, 255, trackChaned)
# cv2.createTrackbar("Min", "H2", 0, 255, trackChaned)
#
# cv2.createTrackbar("Max", "S2", 0, 255, trackChaned)
# cv2.createTrackbar("Min", "S2", 0, 255, trackChaned)
#
# cv2.createTrackbar("Max", "V2", 0, 255, trackChaned)
# cv2.createTrackbar("Min", "V2", 0, 255, trackChaned)
# while 1:
#     hul = cv2.getTrackbarPos("Max", "H")
#     huh = cv2.getTrackbarPos("Min", "H")
#
#     sul = cv2.getTrackbarPos("Max", "S")
#     suh = cv2.getTrackbarPos("Min", "S")
#
#     vul = cv2.getTrackbarPos("Max", "V")
#     vuh = cv2.getTrackbarPos("Min", "V")
#     lower = np.array([hul, sul, vul], dtype="uint8")  # [70, 0, 250]
#     upper = np.array([huh, suh, vuh], dtype="uint8")
#     mask1 = cv2.inRange(HSV, lower, upper)
#
#
#
#     hul2 = cv2.getTrackbarPos("Max", "H2")
#     huh2 = cv2.getTrackbarPos("Min", "H2")
#
#     sul2 = cv2.getTrackbarPos("Max", "S2")
#     suh2 = cv2.getTrackbarPos("Min", "S2")
#
#     vul2 = cv2.getTrackbarPos("Max", "V2")
#     vuh2 = cv2.getTrackbarPos("Min", "V2")
#     lower2 = np.array([hul2, sul2, vul2], dtype="uint8")  # [70, 0, 250]
#     upper2 = np.array([huh2, suh2, vuh2], dtype="uint8")
#     mask2 = cv2.inRange(HSV, lower2, upper2)
#
#     mask = mask1 + mask2
#
#     mask = cv2.dilate(mask, kernel)
#     cv2.imshow("wocaomn", mask)
#
#     if cv2.waitKey(1) == 27:
#         break
#
# cv2.destroyAllWindows()

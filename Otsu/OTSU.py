import cv2
import numpy as np


image = cv2.imread("Otsu\medical_image.jpg", 0)


ret, segmented = cv2.threshold(
    image,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

cv2.imwrite("Otsu\otsu_result.png", segmented)


print("Optimal Threshold:", ret)

import cv2
import numpy as np


image = cv2.imread("Graph Cut/image3.png")

if image is None:
    print("Error: Image not found. Check file path.")
    exit()

image = cv2.resize(image, (512, 512))

mask = np.zeros(image.shape[:2], np.uint8)

bgdModel = np.zeros((1,65), np.float64)
fgdModel = np.zeros((1,65), np.float64)

rect = (100,100,1000,1000)

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# coords = cv2.findNonZero(gray)
# x, y, w, h = cv2.boundingRect(coords)
# image = image[y:y+h, x:x+w]

cv2.grabCut(
    image,
    mask,
    rect,
    bgdModel,
    fgdModel,
    5,
    cv2.GC_INIT_WITH_RECT
)

mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

result = image * mask2[:,:,np.newaxis]

cv2.imwrite("Graph Cut/graphcut_result.png", result)
cv2.imshow("Segmented Image", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

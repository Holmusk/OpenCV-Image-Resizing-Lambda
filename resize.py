import cv2
import time

 
img = cv2.imread('images/original/test_image1.jpg', cv2.IMREAD_UNCHANGED)
 
dim = (299, 299)
start = time.perf_counter()
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
 end = time.perf_counter()
print('Resized Dimensions : ',resized.shape)
 
cv2.imwrite('images/resized/test_image1_resized.jpg',resized)
print(end-start)

import cv2
import time
import numpy as np

 
img = cv2.imread('images/original/test_image1.jpg', cv2.IMREAD_UNCHANGED)

smoothed_image = cv2.GaussianBlur(img, (9, 9), 10)
unsharped_image = cv2.addWeighted(img, 1.5, smoothed_image, -0.5, 0)

#improve image contrast
clahe = cv2.createCLAHE(clipLimit=4.0)

H, S, V = cv2.split(cv2.cvtColor(unsharped_image, cv2.COLOR_RGB2HSV))
eq_V = clahe.apply(V)
eq_image = cv2.cvtColor(cv2.merge([H, S, eq_V]), cv2.COLOR_HSV2RGB)

#add padding to image
h, w = img.shape[:2]
if h > w:
   diff = h-w
   pad_width = np.floor((diff)/2).astype(np.int)
   if (diff % 2) == 0:
       padded_image= np.pad(eq_image, ((0, 0), (pad_width, pad_width), (0, 0)),
                     'constant', constant_values=0)
   else:
       padded_image= np.pad(img, ((0, 0), (pad_width, pad_width+1), (0, 0)),
                     'constant', constant_values=0)
elif h < w:
   diff = w-h
   pad_width = np.floor((diff)/2).astype(np.int)
   if (diff % 2) == 0:
       padded_image=  np.pad(eq_image, ((pad_width, pad_width), (0, 0), (0, 0)),
                     'constant', constant_values=0)
   else:
       padded_image= np.pad(eq_image, ((pad_width, pad_width+1), (0, 0), (0, 0)),
                     'constant', constant_values=0)
else:
   padded_image= eq_image
dim = (299, 299)
start = time.perf_counter()
# resize image
resized = cv2.resize(padded_image, dim, interpolation = cv2.INTER_CUBIC)
end = time.perf_counter()
print('Resized Dimensions : ',resized.shape)
 
cv2.imwrite('images/resized/test_image_resized.jpg',resized)
print(end-start)

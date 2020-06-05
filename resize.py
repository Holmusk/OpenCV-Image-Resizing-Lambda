import cv2
 
img = cv2.imread('images/original/test_image1.jpg', cv2.IMREAD_UNCHANGED)
 
dim = (299, 299)
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
 
print('Resized Dimensions : ',resized.shape)
 
cv2.imwrite('images/resized/test_image1_resized.jpg',resized)

from PIL import Image
import numpy as np
img_name=input('Enter filename with extension- ')
img=Image.open(img_name).convert('L')
img_arr=np.array(img)
k=7
sigma=100000000
weights=np.zeros((k,k))
for i in range(k):
	for j in range(k):
		weights[i,j]=np.exp(-((i-k//2)**2+(j-k//2)**2)/sigma)
weights/=np.sum(weights)
img_height,img_breadth=img_arr.shape
img_blurred_arr=np.zeros((img_height,img_breadth))
for i in range(10,290):
	for j in range(10,190):
		kernal=img_arr[i-k//2:i+k//2+1,j-k//2:j+k//2+1]
		img_blurred_arr[i][j]=np.sum(kernal*weights)
img_blurred=Image.fromarray(img_blurred_arr)
img_blurred.show()

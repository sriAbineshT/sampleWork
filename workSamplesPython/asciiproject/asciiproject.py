from PIL import Image                                                                                                                                                                                        
import numpy as np

#please ensure a big char_ramp, mahn, ok?
#two char_ramps are given already, the second being surprisingly better than the first
#char_ramp="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!1I;:,\"^`'"
char_ramp="@%#*+=-:. "
char_ramp_len=len(char_ramp)
asp_rat_correction=2.1 #correction factor; if image appears stretched vertically, increase value, decrease for the opposite effect; 2 is the best value; approved after a very accurate analysis ;)
			#but somehow, 2.1 feels right and better, ok?
			#correction factor remains 2 for whatsapp on analysis, 2.1 is probably good for the eyes,huh?

display_length=203 #203 for this editor; 31 for whatsapp
display_breadth=53 #53 for this; 34 for whatsapp
#name_without_ext=input("Type in your filename(without the . and extension)\n")
#file_type=input("Enter the file type(without the .)\n")
#filename=name_without_ext+"."+file_type
filename=input("Type in your filename(with the extension, ofcourse)\n")
name_without_ext=filename.split('.')[0]
img=Image.open(filename).convert('L')
img_length,img_breadth=img.size
img_dim_ratio=img_length/img_breadth
if img_dim_ratio*asp_rat_correction<(display_length/display_breadth):
	resize_length=int(img_dim_ratio*display_breadth*asp_rat_correction)
	resize_breadth=display_breadth
else:
	resize_length=display_length
	resize_breadth=int(display_length/(img_dim_ratio*asp_rat_correction))
img=img.resize((resize_length,resize_breadth))

img_arr=np.array(img)
array_length,array_breadth=img_arr.shape
gsv_min=img_arr.min()
gsv_max=img_arr.max()
gsv_range=gsv_max-gsv_min

file=open(name_without_ext+"1",'w')
string=""
for i in range(0,array_length):
	for j in range(0,array_breadth):
		gsv=img_arr[i][j]
		if gsv==gsv_min:
			#file.write(char_ramp[0])
			string+=char_ramp[0]
		else: 
			if gsv==gsv_max:
				#file.write(char_ramp[-1])
				string+=char_ramp[-1]
			else:
				#file.write(char_ramp[(gsv-gsv_min)*char_ramp_len//gsv_range])
				string+=char_ramp[(gsv-gsv_min)*char_ramp_len//gsv_range]
	#file.write('\n')
	string+='\n'
print(string)
print("The above image/text has been stored in a file")
file.write(string)
file.close()
print("Look for a text file by the name- "+name_without_ext+"1")

	


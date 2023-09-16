from PIL import Image, ImageEnhance
from math import cos, sin, tan, log, log10, sqrt
import os
import os.path
import glob

def scale(i):
	return (i/16.0)**2

def scale_2(i):
	return (i/40)**3

def first_process(image: Image.Image, f):
	source = image.split()
	# convert = ImageEnhance.Color(image)
	R, G, B = 0, 1, 2

	# select regions where red is less than 100
	mask_red = source[R].point(lambda i: i > 180 and 255)
	# mask_blue = source[B].point(lambda i: i < 180 and 255)
	mask_green = source[G].point(lambda i: i > 100 and 255)

	# process the green band
	out_red = source[R].point(scale )
	# out_red = source[R].point(lambda i: 12*i**.5)
	out_green = source[G].point(scale_2)
	# out_blue = source[B].point(scale)


	convert = ImageEnhance.Color(source[R])
	# paste the processed band back, but only where red was < 100
	
	# source[B].paste(out_blue, None, mask_red)
	# mask_green = source[G].point(lambda i: i > 100 and 255)

	# paste the processed band back, but only where red was < 100
	# source[R].paste(out_green, None, mask_red)

	source[R].paste(out_red, None, None)
	source[G].paste(out_green, None, None)
	# source[B].paste(out_blue, None, None)




	# build a new multiband image
	image = Image.merge(image.mode, source)
	outpath = "output_images/first_process/"
	# print(f)
	os.makedirs(os.path.join(outpath, 'sample_images'),exist_ok=True)
	image.save(os.path.join(outpath, f))



def second_process(image: Image.Image, f):
	source = image.split()
	# convert = ImageEnhance.Color(image)
	R, G, B = 0, 1, 2

	# select regions where red is less than 100
	mask_red = source[R].point(lambda i: i > 180 and 255)
	# mask_blue = source[B].point(lambda i: i < 180 and 255)
	mask_green = source[G].point(lambda i: i > 100 and 255)

	# process the green band
	# out_red = source[R].point(scale )
	# out_red = source[R].point(lambda i: 12*i**.5)
	out_green = source[G].point(scale_2)
	# out_blue = source[B].point(scale)


	# convert = ImageEnhance.Color(source[R])
	# paste the processed band back, but only where red was < 100
	
	# source[B].paste(out_blue, None, mask_red)
	# mask_green = source[G].point(lambda i: i > 100 and 255)

	# paste the processed band back, but only where red was < 100
	# source[R].paste(out_green, None, mask_red)

	# source[R].paste(out_red, None, None)
	# source[G].paste(out_green, None, mask_red)
	# source[B].paste(out_blue, None, None)


	temp_red = source[R]
	temp_green = source[G]
	temp_blue = source[B]

	# source[R].paste(temp3)
	source[B].paste(temp_green)
	source[G].paste(temp_blue)

	# build a new multiband image
	image = Image.merge(image.mode, source)
	outpath = "output_images/second_process/"
	# print(f)
	os.makedirs(os.path.join(outpath, 'sample_images'),exist_ok=True)
	image.save(os.path.join(outpath, f))

files = glob.glob("sample_images/*.jpg")
ref = glob.glob("sample_images/*.png")

process = second_process

for f in ref:
	process(Image.open(f), f)
for f in files:
	process(Image.open(f), f)


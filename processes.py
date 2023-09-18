from math import atan
from operator import inv
from PIL import Image
import sys
import numpy as np
from process import Process, Mask, R, G, B
import logging
logging.basicConfig(level=logging.INFO)

def scale_2(i):
	return (i/40)**3

def squash(i):
	return 20 + i * 0.85
	# return 255

def root(i):
	return 15 * i ** 0.5

def to_255(i):
	return 255

def scale(i):
	return (i/16.0)**2

def atan_scale(i):
	A = 29
	C = 96
	D = -4
	E = 120
	return C * atan(i/A + D) + E

def atan_scale2(i):
	A = 29
	C = 96
	D = 0
	E = 17
	return C * atan(i/A + D) + E

def avg (band1: Image.Image, band2: Image.Image, weight: float = 0.5) -> Image:
	# logging.info(len(band1.getdata()))
	bd1 = np.array(band1)
	bd2 = np.array(band2)
	y = (bd1*weight + bd2 * (1-weight))/2
	# y = [(d*weight+i*(1-weight))/2 for d, i in list(zip(band1.getdata(), band2.getdata()))]
	return Image.fromarray(y)

def subt (band1: Image.Image, band2: Image.Image, weight: float = 0.5) -> Image:
	bd1 = np.array(band1)
	bd2 = np.array(band2)
	y = np.absolute(bd1 - bd2)
	return Image.fromarray(y)

def pop_var(band1: Image.Image, band2: Image.Image, second_band=False) -> Image:
	bd1 = np.array(band1)
	bd2 = np.array(band2)
	a = avg(bd1, bd2)
	if second_band:
		y = ((bd2-a)**2)/2
	else:
		y = ((bd1-a)**2)/2
	return Image.fromarray(y)

def samp_var(band1: Image.Image, band2: Image.Image, second_band=False) -> Image:
	bd1 = np.array(band1)
	bd2 = np.array(band2)
	a = avg(bd1, bd2)
	if second_band:
		y = (bd2 - a)**2
	else:
		y = (bd1 - a)**2

	return Image.fromarray(y)

common_red_mask = Mask(R,lambda i: i > 180 and 255)


# process 6
process6 = Process("process6")
process6.scale_blue = lambda i: 0.9 * i
process6.scale_red =  lambda i: 1.145 * i #atan_scale
process6.mask_green = common_red_mask
process6.mask_blue = common_red_mask
def p6(obj: Process) -> None:
	obj.source[B].paste(obj.green_band)
	obj.source[R].paste(obj.blue_band)
	m = obj.source[R].point(lambda i: i*1.25)
	obj.source[R].paste(m)
process6.prerender = p6

# process 5
process5 = Process("process5")
process5.scale_green = lambda i: 0.9 * i
process5.scale_blue = lambda i: 0.7 * i
process5.scale_red =  lambda i: 1.145 * i #atan_scale
process5.mask_green = common_red_mask
process5.mask_blue = common_red_mask
def p5(obj: Process) -> None:
	obj.source[B].paste(obj.green_band)
	obj.source[R].paste(obj.blue_band)
	m = obj.source[R].point(lambda i: i*1.25)
	obj.source[R].paste(m)
	# obj.source[G].paste(obj.blue_band)
	pass
process5.prerender = p5


# process 3
process3 = Process("process3")
process3.scale_blue = squash
def p3(obj: Process) -> None:
	obj.source[G].paste(obj.blue_band)
	obj.source[B].paste(obj.green_band)
	# obj.source[G].paste(obj.red_band)
	pass
process3.prerender = p3

process2_2 = Process("process2-2")
process2_2.scale_green = lambda i: 0.9 * i
process2_2.scale_blue = lambda i: 0.7 * i
process2_2.scale_red =  lambda i: 1.145 * i
process2_2.mask_green = common_red_mask
process2_2.mask_blue = common_red_mask
def p2_2(obj: Process) -> None:
	obj.source[R].paste(obj.green_band)
	obj.source[G].paste(obj.blue_band)
	pass
process2_2.prerender = p2_2


process_avg_blue_green = Process("avg_bg")
process_avg_blue_green.scale_blue = lambda i: 0.25 * i
process_avg_blue_green.scale_green = lambda i: 0.25 *i
def pabg(obj: Process) -> None:
	# print("oy")
	y = pop_var(obj.blue_band, obj.green_band, True)
	# print(y)
	obj.source[G].paste(y)
	obj.source[B].paste(y)
	# obj.source[G].paste(y)
	pass
process_avg_blue_green.prerender = pabg

process_avg_red_green = Process("avg_rg")
process_avg_red_green.scale_blue = lambda i: 1 * i
process_avg_red_green.scale_green = lambda i: 1 * i
def parg(obj: Process) -> None:
	# print("oy")
	# y = pop_var(obj.red_band, obj.blue_band, True)
	bd1 = np.array(obj.red_band)
	bd2 = np.array(obj.blue_band)
	a = np.average(avg(bd1, bd2))
	y = ((bd2-a)**2)/2
	# print(y)
	# obj.source[R].paste(y)
	# obj.source[B].paste(y)
	# obj.source[G].paste(y)
	obj.source[B].paste(obj.green_band)
	obj.source[G].paste(obj.blue_band)
	pass
process_avg_red_green.prerender = parg

process7 = Process("process7")
process7.scale_green = lambda i: 255*.2
process7.scale_blue = lambda i: 1.2*i

def p7(obj: Process) -> None:
	b2 = np.asarray(obj.source[B])
	band = 4*255*.6-b2
	blueband = Image.fromarray(band)
	obj.source[B].paste(blueband)
	obj.source[R].paste(obj.blue_band)
	m = obj.source[B].point(lambda i: i*1.25)
	obj.source[B].paste(m, None, None)
	pass

process7.prerender = p7

process7.test()

process8 = Process("process8")
f= lambda i: i +50
process8.scale_blue = f
process8.scale_red = f
process8.scale_green = f

def p8(obj: Process):
	red_band = obj.source[R]
	green_band = obj.source[G]
	blue_band = obj.source[B]
	b1 = np.array(red_band)
	b2 = np.array(green_band)
	b3 = np.array(blue_band)
	red_bias = 1
	blue_bias = 1
	green_bias = 1
	total_bias = red_bias+blue_bias+green_bias
	# average = (
	# 	b1*(red_bias/total_bias) +
	# 	b2*(green_bias/total_bias) +
	# 	b3*(blue_bias/total_bias)
	# )/3
	average = (b1 + b2 + b3)/3
	print(average)
	average_image = Image.fromarray(average)
	red_bias *=1.5
	biased_average = (
		b1*red_bias/total_bias +
		b2*green_bias/total_bias +
		b3*blue_bias/total_bias)/3
	biased_image = Image.fromarray(biased_average)

	intermediate = Image.merge(mode=obj.image.mode, bands=obj.source)
	# print(average)
	vfunc = np.vectorize(lambda i: i <= 80 or 255)
	vfunc = np.vectorize(lambda i: 255 if i <= 180 else 0)
	r = vfunc(average)
	# print(r)
	average_image = Image.fromarray(r.astype(np.uint8))
	mask = average_image.point(lambda i: i <= 180 or 255)
	inv_mask = intermediate.point(lambda i: i >= 180 or 0)
	obj.__for_debug__ = [intermediate, mask, inv_mask, average_image, biased_image]
	# obj.source[R].paste(average_image, None, inv_mask)
	# obj.source[G].paste(average_image, None, inv_mask)
	# obj.source[B].paste(average_image, None, inv_mask)
	# obj.source[R].paste(biased_image, None, inv_mask)
	# obj.source[G].paste(biased_image, None, inv_mask)
	# obj.source[B].paste(biased_image, None, inv_mask)
	pass

process8.prerender = p8

processes: dict[str, Process] = {
	"process2_2": process2_2,
	"process5": process5,
	"process3": process3,
	"process6": process6,
	"avg_bg": process_avg_blue_green,
	"avg_rg": process_avg_red_green,
	"process7": process7,
	"process8": process8,
}
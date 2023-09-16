from math import atan
from PIL import Image
import numpy as np
from process import Process, Mask, R, G, B
import logging
logging.basicConfig(level=logging.INFO)

def scale(i):
	return (i/16.0)**2

def scale_2(i):
	return (i/40)**3

def squash(i):
	return 20 + i * 0.85
	# return 255

def root(i):
	return 15 * i ** 0.5

def to_255(i):
	return 255

# blue_green_swap = Process("blue_green_swap")
# def t(obj) -> None:
# 	obj.source[B].paste(obj.green_band)
# 	obj.source[G].paste(obj.blue_band)
# blue_green_swap.prerender = t
# blue_green_swap.full_test()

"""
blue_red_swap = Process("blue_red_swap")

def squash(i):
	return 20 + i * 0.85

# blue_red_swap.scale_blue = scale_2
blue_red_swap.scale_green = squash
blue_red_swap.mask_green = Mask(R,lambda i: i > 180 and 255)

def t(obj: Process) -> None:
	obj.source[G].paste(obj.blue_band)
	obj.source[B].paste(obj.green_band)
	# obj.source[G].paste(obj.red_band)
	pass
blue_red_swap.prerender = t

blue_red_swap.test()
# blue_red_swap.debug()
blue_red_swap.full_test()
"""

process = Process("process2-2")

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
# blue_red_swap.scale_blue = scale_2
process.scale_green = lambda i: 0.9 * i
process.scale_blue = lambda i: 0.7 * i
process.scale_red =  lambda i: 1.145 * i #atan_scale
# process.scale_red = squash
# process.scale_blue = squash
process.mask_green = Mask(R,lambda i: i > 180 and 255)
process.mask_blue = Mask(R,lambda i: i > 180 and 255)

def avg (band1: Image.Image, band2: Image.Image, weight: float = 0.5):
	# logging.info(len(band1.getdata()))
	bd1 = np.array(band1.getdata())
	bd2 = np.array(band2.getdata())
	y = (bd1*weight + bd2 * (1-weight))/2
	# y = [(d*weight+i*(1-weight))/2 for d, i in list(zip(band1.getdata(), band2.getdata()))]
	return y.tolist()

def subt (band1: Image.Image, band2: Image.Image, weight: float = 0.5):
	bd1 = np.array(band1.getdata())
	bd2 = np.array(band2.getdata())
	y = np.absolute(bd1 - bd2)
	return y.tolist()

def pop_var(band1: Image.Image, band2: Image.Image, weight: float = 0.5):
	bd1 = np.array(band1.getdata())
	bd2 = np.array(band2.getdata())
	y = ((bd1-bd2)**2)/2
	return y

def samp_var(band1: Image.Image, band2: Image.Image, weight: float = 0.5):
	bd1 = np.array(band1.getdata())
	bd2 = np.array(band2.getdata())
	y = (bd1 - bd2)**2
	return y.tolist()

def t(obj: Process) -> None:
	# x = subt(obj.blue_band, obj.red_band, 0.5)
	# y = avg(obj.blue_band, obj.red_band, 0.5)
	# obj.source[G].putdata(x)
	# obj.source[B].putdata(y)
	# obj.source[R].putdata(y)
	# obj.source[B].putdata(x)
	# obj.source[R].putdata(x)
	obj.source[R].paste(obj.green_band)
	obj.source[G].paste(obj.blue_band)
	# m = obj.source[R].point(lambda i: i*1.25)
	# obj.source[R].paste(m)
	# obj.source[G].paste(obj.blue_band)
	pass
process.prerender = t

process.test()
# blue_red_swap.debug()
process.full_test()
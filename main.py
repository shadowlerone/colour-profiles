from math import atan
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


process = Process("process7")

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

process.scale_green = lambda i: 255*.2
process.scale_blue = lambda i: 1.2*i
# process.scale_red =  lambda i: 1.145 * i
# process.scale_red = squash
# process.scale_blue = squash


# process.mask_green = Mask(R,lambda i: i > 100 and 255)
# process.mask_blue = Mask(R,lambda i: i > 180 and 255)


def t(obj: Process) -> None:
	# obj.source[B].paste(obj.green_band)
	# obj.source[B].paste(obj.source[G].point(lambda i: (255*.6-i)/2 + i), None, obj.source[G].point(lambda i: i < 100 or 255))
	
	# b1 = np.asarray()
	b2 = np.asarray(obj.source[B])

	band = 4*255*.6-b2
	blueband = Image.fromarray(band)
	obj.source[B].paste(blueband)
	obj.source[R].paste(obj.blue_band)
	m = obj.source[B].point(lambda i: i*1.25)
	# n = obj.source[G].point(lambda i: i*1.25)
	obj.source[B].paste(m, None, None)
	# obj.source[G].paste(n, None, None)
	pass

process.prerender = t

process.test()
# blue_red_swap.debug()
if "--full" in sys.argv:
	process.full_test()
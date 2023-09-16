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

process = Process("process3")

# blue_red_swap.scale_blue = scale_2
# process.scale_green = squash
# process.scale_red = root
process.scale_blue = squash
# process.mask_green = Mask(R,lambda i: i > 180 and 255)

def t(obj: Process) -> None:
	obj.source[G].paste(obj.blue_band)
	obj.source[B].paste(obj.green_band)
	# obj.source[G].paste(obj.red_band)
	pass
process.prerender = t

process.test()
# blue_red_swap.debug()
process.full_test()

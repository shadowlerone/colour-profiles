from gc import callbacks
from glob import glob
from typing import Callable
from PIL import Image
import os
import logging as l

R, G, B = 0, 1, 2

class Mask():
	band: int
	selector: Callable
	def __init__(self, band, selector):
		self.band = band
		self.selector = selector

class Process():
	name: str
	mask_red: [Mask, None]
	mask_green: [Mask, None]
	mask_blue: [Mask, None]
	scale_red: [Callable, None]
	scale_green: [Callable, None]
	scale_blue: [Callable, None]
	prerender: [Callable, None]
	image: [Image.Image, None]
	source: [Image.Image, None]
	def __init__(self, name):
		self.name = name
		self.mask_red: [Mask, None] = None
		self.mask_green: [Mask, None] = None
		self.mask_blue: [Mask, None] = None
		self.scale_red: [Callable, None] = None
		self.scale_green: [Callable, None] = None
		self.scale_blue: [Callable, None] = None
		self.prerender: [Callable, None] = None
		self.image: [Image.Image, None] = None
		self.source: [Image.Image, None] = None
		
	def debug(self):
		print(self.scale_blue)
	def __call__(self, fp: str):
		self.image = Image.open(fp)
		self.source = self.image.split()

		if self.mask_red:
			l.debug("Applying Red Mask")
			self.red_band_mask = self.source[self.mask_red.band].point(self.mask_red.selector)
		else:
			self.red_band_mask = None

		if self.mask_green:
			l.debug("Applying Green Mask")
			self.green_band_mask = self.source[self.mask_green.band].point(self.mask_green.selector)
		else:
			self.green_band_mask = None

		if self.mask_blue:
			l.debug("Applying Blue Mask")
			self.blue_band_mask = self.source[self.mask_blue.band].point(self.mask_blue.selector)
		else:
			self.blue_band_mask = None


		if self.scale_red:
			l.debug("Applying Red Scale")
			self.red_band = self.source[R].point(self.scale_red)
		else:
			self.red_band = self.source[R]

		if self.scale_green:
			l.debug("Applying Green Scale")
			self.green_band = self.source[G].point(self.scale_green)
		else:
			self.green_band = self.source[G]

		if self.scale_blue:
			l.debug("Applying Blue Scale")
			self.blue_band = self.source[B].point(self.scale_blue)
		else:
			self.blue_band = self.source[B]

		self.source[R].paste(self.red_band, None, self.red_band_mask)
		self.source[G].paste(self.green_band, None, self.green_band_mask)
		self.source[B].paste(self.blue_band, None, self.blue_band_mask)
		if self.prerender:
			l.debug("Running prerenderer")
			self.prerender(self)

		
		output = Image.merge(self.image.mode, self.source)
		outpath = f"output_images/{self.name}/"

		os.makedirs(os.path.join(outpath, 'sample_images'),exist_ok=True)
		output.save(os.path.join(outpath, fp))

	def test(self):
		l.info("Rendering Test Image")
		self("sample_images/Reflective-color-chart-reference.png")
		l.info("Rendering Test Image 2")
		self("sample_images/gamutvision_equations_HSL_Smax_LBL.png")
		l.info("Rendering Test Image 3")
		self("sample_images/gamutvision_equations_HSV_Smax_LBL.png")

	def full_test(self):
		self.test()
		files = glob("sample_images/*.jpg")
		for i in files:
			l.info(f"Rendering {i}")
			self(i)
import numpy as np

from helper_functions import *

class Window:
	def __init__(self, render_handler, width, height, top_left, top_bar_says):
		self.render_handler = render_handler

		self.width = width
		self.height = height
		self.top_left = top_left

		self.top_bar_says = top_bar_says
		self.highlight_top_bar = False

		self.is_visible = False

	def get_img_arr(self):
		num_rows = self.height
		num_cols = self.width
		ascii_arr = np.full(shape=(num_rows, num_cols), fill_value="?")
		fg_arr = np.full(shape=(num_rows, num_cols), fill_value="white", dtype="object")
		bg_arr = np.full(shape=(num_rows, num_cols), fill_value="black", dtype="object")
		return ascii_arr, fg_arr, bg_arr

	def draw_to_scr(self, scr_arr, scr_fg_arr, scr_bg_arr):
		if not self.is_visible:
			return  
			
		ascii_arr, fg_arr, bg_arr = self.get_img_arr()
		draw_img_on_canvas(ascii_arr, scr_arr, self.top_left)
		draw_img_on_canvas(fg_arr, scr_fg_arr, self.top_left)
		draw_img_on_canvas(bg_arr, scr_bg_arr, self.top_left)

		top_bar, fg_bar, bg_bar = get_top_bar(self.top_bar_says, self.width, self.highlight_top_bar)

		left, top = self.top_left
		top -= 1
		draw_img_on_canvas(top_bar, scr_arr, (left, top))
		draw_img_on_canvas(fg_bar, scr_fg_arr, (left, top))
		draw_img_on_canvas(bg_bar, scr_bg_arr, (left, top))

	def reset_render_scheme_settings(self):
		self.highlight_top_bar = False
		self.is_visible = False
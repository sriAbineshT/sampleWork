import numpy as np

from event import *
from helper_functions import *
from window import *

class TopdownWindow(Window):
	def __init__(self, render_handler):
		super().__init__(
				render_handler=render_handler, 
				width=17, 
				height=9, 
				top_left=(1, 3),  
				top_bar_says="TopdownView"
			)

	def get_img_arr(self):
		cam_pos_event = GetCameraPosition()
		self.render_handler.game_engine.fire_event(cam_pos_event)
		camera_x = cam_pos_event.pos_x
		camera_y = cam_pos_event.pos_y

		num_rows = self.height
		num_cols = self.width
		ascii_arr = np.full(shape=(num_rows, num_cols), fill_value=" ")
		fg_color_arr = np.full(shape=(num_rows, num_cols), fill_value="white", dtype="object")
		bg_color_arr = np.full(shape=(num_rows, num_cols), fill_value="black", dtype="object")
		render_event = CallForRender(ascii_arr, fg_color_arr, bg_color_arr, camera_x, camera_y)
		self.render_handler.game_engine.fire_event(render_event)

		return ascii_arr, fg_color_arr, bg_color_arr
import numpy as np

from window import *
from helper_functions import *
from event import *

class PlayerInfoWindow(Window):
	def __init__(self, render_handler):
		super().__init__(
				render_handler=render_handler,  
				width=12, 
				height= 10,  
				top_left=(19, 1),  
				top_bar_says="PlayerInfo"
			)

	def get_img_arr(self):
		num_rows = self.height
		num_cols = self.width
		ascii_arr = np.full(shape=(num_rows, num_cols), fill_value=" ")
		fg_arr = np.full(shape=(num_rows, num_cols), fill_value="white", dtype="object")
		bg_arr = np.full(shape=(num_rows, num_cols), fill_value="black", dtype="object")

		lines = []
		get_player_info_event = GetPlayerInfo()
		engine = self.render_handler.game_engine
		engine.fire_event(get_player_info_event)
		for key, value in get_player_info_event.player_info.items():
			new_line = centre_align(key + " - " + str(value), num_cols)
			lines.append(new_line)

		for row in range(len(lines)):
			select_line = lines[row]
			for col in range(len(select_line)):
				ascii_arr[row, col] = select_line[col]

		return ascii_arr, fg_arr, bg_arr
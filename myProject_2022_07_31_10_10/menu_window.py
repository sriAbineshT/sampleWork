from window import *
from menu import *
from helper_functions import *

class MenuWindow(Window):
	def __init__(self, render_handler, width, height, top_left, top_bar_says,  
					menu_items):
		super().__init__(
				render_handler=render_handler, 
				width=width, 
				height=height, 
				top_left=top_left,  
				top_bar_says=top_bar_says
			)

		self.menu = Menu(menu_items, 1, False)

	def get_img_arr(self):
		num_rows = self.height
		num_cols = self.width

		ascii_arr = self.menu.get_ascii_arr((num_rows, num_cols), True)
		fg_arr = np.full(shape=(num_rows, num_cols), fill_value="white", dtype="object")
		bg_arr = np.full(shape=(num_rows, num_cols), fill_value="black", dtype="object")

		return ascii_arr, fg_arr, bg_arr

	def get_final_selection(self, command):
		self.menu.send_command(command)
		if self.menu.is_active:
			final_selection = None 
		else:
			final_selection = self.menu.selected_item_indices[0]
		return final_selection
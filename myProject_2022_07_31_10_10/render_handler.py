import numpy as np
import os
import time

from log_window import *
from topdown_window import *
from color_manager import *
from player_info_window import *
from main_menu_window import *
from game_menu_window import *

class RenderHandler:
	def __init__(self):
		self.game_engine = None

		self.scr_width = 80
		self.scr_height = 20

		self.topdown_window = TopdownWindow(self)
		self.log_window = LogWindow(self)
		self.player_info_window = PlayerInfoWindow(self)
		self.main_menu_window = MainMenuWindow(self)
		self.game_menu_window = GameMenuWindow(self)

		self.all_windows = [
				self.topdown_window, self.log_window, self.player_info_window,  
				self.main_menu_window, self.game_menu_window
			]

		self.minimum_refresh_gap = .4
		self.last_render_time = 0

	def render_to_screen(self):
		scr_num_rows = self.scr_height
		scr_num_cols = self.scr_width
		scr_arr = np.full(shape=(scr_num_rows, scr_num_cols), fill_value=" ")
		scr_fg_arr = np.full(shape=(scr_num_rows, scr_num_cols), fill_value="white", dtype="object")
		scr_bg_arr = np.full(shape=(scr_num_rows, scr_num_cols), fill_value="black", dtype="object")
		
		self.reset_all_windows()
		render_scheme = self.game_engine.input_handler.command_scheme
		if render_scheme == "topdown":
			visible_windows = [
					self.topdown_window, self.log_window, self.player_info_window
				]
			highlight_windows = [
					self.topdown_window, 
				]
		elif render_scheme == "in_log":
			visible_windows = [
					self.topdown_window, self.log_window, self.player_info_window
				]
			highlight_windows = [
					self.log_window, 
				]
		elif render_scheme == "in_main_menu":
			visible_windows = [
					self.topdown_window, self.log_window, self.player_info_window, 
					self.main_menu_window
				]
			highlight_windows = [
					self.main_menu_window
				]
		elif render_scheme == "in_game_menu":
			visible_windows = [
					self.topdown_window, self.log_window, self.player_info_window, 
					self.game_menu_window
				]
			highlight_windows = [
					self.game_menu_window
				]
		self.make_windows_visible(visible_windows)
		self.highlight_windows_top_bar(highlight_windows)

		self.draw_to_screen_all_windows(scr_arr, scr_fg_arr, scr_bg_arr)

		current_time = time.time()
		refresh_gap = current_time - self.last_render_time
		required_delay = max(self.minimum_refresh_gap - refresh_gap, 0)
		time.sleep(required_delay)

		os.system("cls")
		for row in range(scr_num_rows):
			for col in range(scr_num_cols):
				character = scr_arr[row, col]
				fg_color = scr_fg_arr[row, col]
				bg_color = scr_bg_arr[row, col]
				my_print(character, fg_color, bg_color, end="")
			print()

		self.last_render_time = time.time()

	def reset_all_windows(self):
		for window in self.all_windows:
			window.reset_render_scheme_settings()

	def draw_to_screen_all_windows(self, scr_arr, scr_fg_arr, scr_bg_arr):
		for window in self.all_windows:
			window.draw_to_scr(scr_arr, scr_fg_arr, scr_bg_arr)

	def make_windows_visible(self, windows):
		for window in windows:
			window.is_visible = True

	def highlight_windows_top_bar(self, windows):
		for window in windows:
			window.highlight_top_bar = True
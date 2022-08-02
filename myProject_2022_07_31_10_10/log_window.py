import numpy as np
from textwrap import wrap

from window import *
from helper_functions import *

class LogWindow(Window):
	def __init__(self, render_handler):
		super().__init__(
				render_handler=render_handler, 
				width=46, 
				height=6, 
				top_left=(1, 13),  
				top_bar_says="Log"
			)

		self.bullet = ">"

		num_x = (self.width - 1) // 2
		num_y = 2 - (self.width % 2)
		border_line = "<" * num_x + "O" * num_y + ">" * num_x
		self.all_lines = [border_line, border_line]

		self.window_state = "locked_to_bottom"
		self.start_line = 0

	def load_to_all_lines(self, msg, bullet=None):
		if bullet == None:
			bullet = self.bullet 

		new_msg_begins_at = len(self.all_lines) - 1

		bullet_msg = " " + bullet + " " + msg
		max_line_length = self.width - 2
		split_msg = wrap(bullet_msg, max_line_length)
		for i in range(len(split_msg)):
			line = split_msg[i]
			split_msg[i] = "|" + line + " " * (self.width - 2 - len(line)) + "|"
		border_line = self.all_lines[-1]
		del self.all_lines[-1]
		self.all_lines += split_msg
		self.all_lines.append(border_line)

		return new_msg_begins_at

	def get_img_arr(self):
		num_rows = self.height
		num_cols = self.width
		ascii_arr = np.full(shape=(num_rows, num_cols), fill_value=" ")
		fg_arr = np.full(shape=(num_rows, num_cols), fill_value="white", dtype="object")
		bg_arr = np.full(shape=(num_rows, num_cols), fill_value="black", dtype="object")

		if self.window_state == "locked_to_bottom":
			lines_to_display = self.all_lines[-num_rows : ]
		elif self.window_state == "use_start_line":
			lines_to_display = self.all_lines[self.start_line : self.start_line + num_rows]

		for row in range(len(lines_to_display)):
			line = lines_to_display[row]
			for col in range(len(line)):
				ascii_arr[row, col] = line[col]

		return ascii_arr, fg_arr, bg_arr

	def send_command(self, command):
		if len(self.all_lines) <= self.height:
			pass
		else:
			if command == "up":
				if self.window_state == "locked_to_bottom":
					self.window_state = "use_start_line"
					self.start_line = len(self.all_lines) - self.height - 1
				elif self.window_state == "use_start_line":
					if self.start_line >= 1:
						self.start_line -= 1
			elif command == "down":
				if self.window_state == "locked_to_bottom":
					pass
				elif self.window_state == "use_start_line":
					if self.start_line >= len(self.all_lines) - self.height - 1:
						self.window_state = "locked_to_bottom"
					else:
						self.start_line += 1
			self.render_handler.render_to_screen()

	def allow_choice(self, prompt_msg, options):
		# some work left to do
		# like disallowing multiple selections, no selection etc

		# part of highlight topbar hotfix
		input_handler_ref = self.render_handler.game_engine.input_handler
		before_command_scheme = input_handler_ref.command_scheme
		input_handler_ref.command_scheme = "in_log"

		potential_start_lines = []
		potential_start_line = self.load_to_all_lines(prompt_msg)
		potential_start_lines.append(potential_start_line)
		highlighted_option_index = 0
		selected_option_indices = []
		key_to_command = {
			"w" : "up", 
			"s" : "down", 
			"z" : "select", 
			"x" : "enter" 
		}
		self.window_state = "use_start_line"
		self.start_line = potential_start_lines[0]
		while True:
			for i, option in enumerate(options):
				if i == highlighted_option_index:
					bullet = " ->"
				else:
					bullet = "   "
				if i in selected_option_indices:
					bullet += "(+)"
				else:
					bullet += "( )"
				potential_start_line = self.load_to_all_lines(option, bullet)
				potential_start_lines.append(potential_start_line)
			if self.start_line >= len(self.all_lines) - self.height:
				self.window_state = "locked_to_bottom"
			self.render_handler.render_to_screen()
			select_command = None
			while select_command not in ["up", "down", "select", "enter"]:
				usr_key = custom_getwch()
				select_command = key_to_command.get(usr_key)
			if select_command == "up":
				if highlighted_option_index > 0:
					highlighted_option_index -= 1
					self.window_state = "use_start_line"
					self.start_line = potential_start_lines[highlighted_option_index + 1]
				else:
					self.window_state = "use_start_line"
					self.start_line = potential_start_lines[0]
			elif select_command == "down":
				if highlighted_option_index < len(options) - 1:
					highlighted_option_index += 1
					self.window_state = "use_start_line"
					self.start_line = potential_start_lines[highlighted_option_index + 1]
				else:
					self.window_state = "use_start_line"
					self.start_line = potential_start_lines[-1]
			elif select_command == "select":
				if highlighted_option_index not in selected_option_indices:
					selected_option_indices.append(highlighted_option_index)
				else:
					selected_option_indices.remove(highlighted_option_index)
			elif select_command == "enter":
				break
			del self.all_lines[-len(options) - 1 : -1]
			del potential_start_lines[-len(options) : ]
		del self.all_lines[-len(options) - 1 : -1]
		for i, option in enumerate(options):
			bullet = "   "
			if i in selected_option_indices:
				bullet += "(+)"
			else:
				bullet += "( )"
			self.load_to_all_lines(option, bullet)
		self.window_state = "locked_to_bottom"

		# part of highlight topbar hotfix
		input_handler_ref.command_scheme = before_command_scheme
		
		self.render_handler.render_to_screen()

		return selected_option_indices
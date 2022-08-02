from msvcrt import getwch, kbhit

from event import *
from helper_functions import *

key_to_command = {
	"w" : "up", 
	"a" : "left", 
	"s" : "down", 
	"d" : "right", 
	"z" : "a_button", 
	"x" : "b_button", 
	"c"	: "x_button", 
	"v" : "y_button", 
	"1" : "quick_exit"
}

class InputHandler:
	def __init__(self):
		self.game_engine = None
		self.command_scheme = "topdown"

	def listen_and_fire(self):
		while True:
			if self.command_scheme == "topdown":
				allowed_commands = ["up", "left", "down", "right", 
					"a_button", "b_button", "x_button", "y_button"]
			elif self.command_scheme == "in_log":
				allowed_commands = ["up", "down", "b_button"]
			elif self.command_scheme == "in_main_menu":
				allowed_commands = ["up", "down", "a_button"]
			elif self.command_scheme == "in_game_menu":
				allowed_commands = ["up", "down", "a_button"]

			select_command = None
			while select_command not in allowed_commands + ["quick_exit", ]:
				usr_key = custom_getwch()
				select_command = key_to_command.get(usr_key)

			if select_command == "quick_exit":
				self.game_engine.exit()

			if self.command_scheme == "topdown":
				command_to_del_numbers = {
					"up" : (0, -1), 
					"left" : (-1, 0), 
					"down" : (0, 1), 
					"right" : (1, 0)
				}
				if select_command in command_to_del_numbers.keys():
					del_x, del_y = command_to_del_numbers[select_command]
					command_event = MoveCommand(del_x, del_y)
					self.game_engine.fire_event(command_event)
				elif select_command == "a_button":
					spot_activate_command_event = SpotActivateCommand()
					self.game_engine.fire_event(spot_activate_command_event)
				elif select_command == "b_button":
					return
				elif select_command == "x_button":
					self.command_scheme = "in_game_menu"
					self.game_engine.render_to_screen()
				elif select_command == "y_button":
					self.command_scheme = "in_main_menu"
					self.game_engine.render_to_screen()
			elif self.command_scheme == "in_log":
				if select_command in ["up", "down"]:
					my_log_window = self.game_engine.render_handler.log_window
					my_log_window.send_command(select_command)
				elif select_command == "b_button":
					self.command_scheme = "topdown"
					self.game_engine.render_to_screen()
			elif self.command_scheme == "in_main_menu":
				main_menu_window_ref = self.game_engine.render_handler.main_menu_window
				command_convert_dict = {
					"up" : "up", 
					"down" : "down", 
					"a_button" : "select"
				}
				converted_command = command_convert_dict.get(select_command)
				main_menu_window_ref.send_command(converted_command)
				self.game_engine.render_to_screen()
			elif self.command_scheme == "in_game_menu":
				game_menu_window_ref = self.game_engine.render_handler.game_menu_window
				command_convert_dict = {
					"up" : "up", 
					"down" : "down", 
					"a_button" : "select"
				}
				converted_command = command_convert_dict.get(select_command)
				game_menu_window_ref.send_command(converted_command)
				self.game_engine.render_to_screen()
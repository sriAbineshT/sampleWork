from menu_window import *

class GameMenuWindow(MenuWindow):
	def __init__(self, render_handler):
		super().__init__(
				render_handler=render_handler, 
				width=10, 
				height=2, 
				top_left=(4, 6),  
				top_bar_says="GameMenu",  
				menu_items=["Log", "Back"]
			)

	def send_command(self, command):
		final_selection = self.get_final_selection(command)
		if final_selection != None:
			if final_selection == 0:
				self.menu.reset()
				input_handler_ref = self.render_handler.game_engine.input_handler
				input_handler_ref.command_scheme = "in_log"
			elif final_selection == 1:
				self.menu.reset()
				input_handler_ref = self.render_handler.game_engine.input_handler
				input_handler_ref.command_scheme = "topdown"
import sys

from render_handler import *
from input_handler import *
from entity import *
from component import *
from dialogue import * # for test
from goal import * # for test
from custom_list import *

class GameEngine:
	def __init__(self):
		self.entities = CustomList()
		self.render_handler = RenderHandler()
		self.render_handler.game_engine = self
		self.input_handler = InputHandler()
		self.input_handler.game_engine = self

	def set_things_up(self):
		# currently written for testing
		player_entity = new_player((0, 0))
		self.add_entity(player_entity)

		for i in range(3):
			self.add_entity(new_pickable((0, 0)))
		self.add_entity(new_origin())

		self.add_entity(new_goblin((2, 0), player_entity))

	def fire_event(self, event):
		entity_iterator = self.entities.get_iterator()
		while entity_iterator.is_alive():
			entity = entity_iterator.spit_out()
			entity.fire_event(event)

	def run_game(self):
		while True:
			self.fire_event(Tick())

	def add_entity(self, entity):
		self.entities.append(entity)
		entity.game_engine = self

	def log_msg(self, msg):
		# use this to log messages
		self.render_handler.log_window.load_to_all_lines(msg)
		self.render_to_screen()

	def render_to_screen(self):
		self.render_handler.render_to_screen()

	def exit(self):
		sys.exit()
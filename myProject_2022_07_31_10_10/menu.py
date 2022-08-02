import numpy as np

from helper_functions import *

class Menu:
	def __init__(self, items, max_selected_items=1000, wait_for_enter=True):
		self.items = items
		self.max_selected_items = max_selected_items
		self.wait_for_enter = wait_for_enter

		self.highlighted_item_index = 0
		self.selected_item_indices = []
		self.is_active = True 

	def send_command(self, command):
		if self.is_active == False:
			return  
		if command in ["up", "down", "select", "enter"]:
			if command == "up":
				self.highlighted_item_index = max(self.highlighted_item_index - 1, 0)
			elif command == "down":
				self.highlighted_item_index = min(self.highlighted_item_index + 1, 
														len(self.items) - 1)
			elif command == "select":
				if self.highlighted_item_index not in self.selected_item_indices:
					if len(self.selected_item_indices) < self.max_selected_items:
						self.selected_item_indices.append(self.highlighted_item_index)
				else:
					self.selected_item_indices.remove(self.highlighted_item_index)
				if self.wait_for_enter == False:
					if len(self.selected_item_indices) == self.max_selected_items:
						self.is_active = False
			elif command == "enter":
				self.is_active = False 
		else:
			return 

	def get_items_with_info(self):
		items_with_info = []
		for i, item in enumerate(self.items):
			if i == self.highlighted_item_index:
				is_highlighted = True
			else:
				is_highlighted = False
			if i in self.selected_item_indices:
				is_selected = True
			else:
				is_selected = False
			items_with_info.append((is_highlighted, is_selected, item))
		return items_with_info

	def reset(self, selected_item_indices_only=False):
		if not selected_item_indices_only:
			self.highlighted_item_index = 0
			
		self.selected_item_indices = []
		self.is_active = True 

	def get_ascii_arr(self, shape=(None, None), centre_aligned=False):
		# keep num_rows 6 or greater to guarantee atleast a shread of uniqueness
		num_rows, num_cols = shape 
		if num_rows == None:
			num_rows = len(self.items)
		if num_cols == None:
			max_item_length = 0 
			for item in self.items:
				if len(item) > max_item_length:
					max_item_length = len(item)
			num_cols = max_item_length + 2
		allowed_item_length = num_cols - 2
		new_items = []
		for item in self.items:
			length_excess = len(item) - allowed_item_length
			if length_excess > 0:
				remove_length = length_excess + 3
				item = item[ : -remove_length]
				item += "..."
			new_items.append(item) 
		lines = []
		for i, item in enumerate(new_items):
			if i == self.highlighted_item_index:
				if not centre_aligned:
					item = "> " + item  
				else:
					item = "<" + item + ">"
			else:
				if not centre_aligned:
					item = "  " + item 
				else:
					item = " " + item + " "
			if not centre_aligned:
				pass 
			else:
				item = centre_align(item, num_cols)
			lines.append(item)
		ascii_arr = np.full(shape=(num_rows, num_cols), fill_value=" ")
		for row, line in zip(range(num_rows), lines):
			for col, symbol in zip(range(num_cols), line):
				ascii_arr[row, col] = symbol
		return ascii_arr
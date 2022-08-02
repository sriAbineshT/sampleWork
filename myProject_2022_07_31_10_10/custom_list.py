import copy

class CustomList:
	def __init__(self, my_list=[]):
		self.my_list = my_list
		self.my_iterators = []

	def get_iterator(self):
		new_iterator = Iterator(self.my_list)
		self.my_iterators.append(new_iterator)
		return new_iterator

	def append(self, item):
		self.my_list.append(item)

	def remove(self, item):
		item_found = False
		delete_index = None 
		for i in range(len(self.my_list)):
			if self.my_list[i] == item:
				item_found = True
				delete_index = i 
				break 
		if item_found == True:
			del self.my_list[delete_index]
			self.introspect(delete_index)

	def introspect(self, index_deleted):
		for iterator in self.my_iterators:
			iterator.introspect(index_deleted)

	def get_list_copy(self):
		list_copy = copy.copy(self.my_list)
		return list_copy

class Iterator:
	def __init__(self, read_only_list):
		self.read_only_list = read_only_list
		self.current_index = 0
		
	def is_alive(self):
		return self.current_index < len(self.read_only_list)

	def spit_out(self):
		return_item = self.read_only_list[self.current_index]
		self.current_index += 1
		return return_item

	def introspect(self, index_deleted):
		if index_deleted < self.current_index:
			self.current_index -= 1
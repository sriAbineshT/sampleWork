from event import *
from a_star_proper import *

class Goal:
	def __init__(self):
		self.original_intent = None
		self.parent_brain = None

	def is_finished(self):
		return True

	def take_action(self):
		pass

class ApproachEntity(Goal):
	def __init__(self, entity):
		super().__init__()

		self.entity = entity

	def is_finished(self):
		get_pos_event = GetPosition()
		self.entity.fire_event(get_pos_event)
		if get_pos_event.is_modified == True:
			entity_pos_x = get_pos_event.pos_x
			entity_pos_y = get_pos_event.pos_y
			get_my_pos_event = GetPosition()
			my_entity = self.parent_brain.parent_entity
			my_entity.fire_event(get_my_pos_event)
			if get_my_pos_event.is_modified == True:
				# the neighbor check is simpler with a h_cost condition
				# look into that
				my_pos_x = get_my_pos_event.pos_x
				my_pos_y = get_my_pos_event.pos_y
				entity_neighbors = []
				for dirn in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
					dirn_x, dirn_y = dirn
					neighbor_x = entity_pos_x + dirn_x
					neighbor_y = entity_pos_y + dirn_y
					entity_neighbors.append((neighbor_x, neighbor_y))
				if (my_pos_x, my_pos_y) in entity_neighbors:
					return True
		return False

	def take_action(self):
		get_pos_event = GetPosition()
		self.entity.fire_event(get_pos_event)
		if get_pos_event.is_modified == True:
			entity_pos_x = get_pos_event.pos_x
			entity_pos_y = get_pos_event.pos_y
			get_my_pos_event = GetPosition()
			my_entity = self.parent_brain.parent_entity
			my_entity.fire_event(get_my_pos_event)
			if get_my_pos_event.is_modified == True:
				my_pos_x = get_my_pos_event.pos_x
				my_pos_y = get_my_pos_event.pos_y
				my_pos = (my_pos_x, my_pos_y)
				entity_pos = (entity_pos_x, entity_pos_y)
				game_engine_reference = my_entity.game_engine
				new_event = GetImpassableNodes()
				game_engine_reference.fire_event(new_event)
				impassable = new_event.impassable
				path_nodes = get_path_nodes(my_pos, entity_pos, impassable)
				if len(path_nodes) > 1:
					node_1_x, node_1_y = path_nodes[0]
					node_2_x, node_2_y = path_nodes[1]
					del_pos_x = node_2_x - node_1_x
					del_pos_y = node_2_y - node_1_y
					self_move_event = MoveBySelf(del_pos_x, del_pos_y)
					my_entity.fire_event(self_move_event)

class KillEntity(Goal):
	def __init__(self, entity):
		super().__init__()

		self.entity = entity

	def is_finished(self):
		engine_ref = self.parent_brain.parent_entity.game_engine
		if self.entity in engine_ref.entities.get_list_copy():
			return False
		else:
			return True

	def take_action(self):
		my_entity = self.parent_brain.parent_entity
		look_for_options_event = LookForAttackOptions()
		my_entity.fire_event(look_for_options_event)
		attack_options_found = look_for_options_event.attack_options
		if len(attack_options_found) > 0:
			first_option = attack_options_found[0]
			prepare_event = PrepareForAttack(self.entity)
			first_option.fire_event(prepare_event)
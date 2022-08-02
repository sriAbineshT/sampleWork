import time

from event import *
from goal import *
from a_star_proper import *
from helper_functions import *

class Component:
	def __init__(self):
		self.parent_entity = None

	def fire_event(self, event):
		pass

class Renderable(Component):
	def __init__(self, symbol, fg_color="white", fg_priority=0, 
			bg_color="black", bg_priority=0, row=0, col=0):
		super().__init__()

		self.symbol = symbol
		self.fg_color = fg_color
		self.fg_priority = fg_priority
		self.bg_color = bg_color
		self.bg_priority = bg_priority
		self.row = row
		self.col = col

	def fire_event(self, event):
		if event.e_id == "call_for_render":
			num_rows, num_cols = event.ascii_arr.shape
			asc_arr_cent_row = (num_rows - 1) // 2
			asc_arr_cent_col = (num_cols - 1) // 2
			new_event = GetPosition()
			self.parent_entity.fire_event(new_event)
			if new_event.is_modified == True:
				pos_x_rel_to_cam = new_event.pos_x - event.camera_x
				pos_y_rel_to_cam = new_event.pos_y - event.camera_y
				self.row = pos_y_rel_to_cam + asc_arr_cent_row
				self.col = pos_x_rel_to_cam + asc_arr_cent_col
			if self.row in range(num_rows) and self.col in range(num_cols):
				indices = (self.row, self.col)
				if self.fg_priority > event.fg_priority_arr[indices]:
					event.ascii_arr[indices] = self.symbol
					event.fg_color_arr[indices] = self.fg_color
					event.fg_priority_arr[indices] = self.fg_priority
				if self.bg_priority > event.bg_priority_arr[indices]:
					event.bg_color_arr[indices] = self.bg_color
					event.bg_priority_arr[indices] = self.bg_priority
		elif event.e_id == "set_background_color":
			self.bg_color = event.bg_color
			self.bg_priority = event.bg_priority

class Position(Component):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		
		self.pos_x = pos_x
		self.pos_y = pos_y

	def fire_event(self, event):
		if event.e_id == "get_position":
			event.pos_x = self.pos_x
			event.pos_y = self.pos_y
			event.is_modified = True
		elif event.e_id == "relative_movement":
			new_pos_x = self.pos_x + event.del_pos_x
			new_pos_y = self.pos_y + event.del_pos_y
			move_event = MoveInto(self.parent_entity, new_pos_x, new_pos_y)
			self.parent_entity.game_engine.fire_event(move_event)
			if move_event.is_successful == True:
				self.pos_x = new_pos_x
				self.pos_y = new_pos_y
				event.is_successful = True
				pos = (self.pos_x, self.pos_y)
				success_event = InNewPosition(self.parent_entity, pos)
				engine_reference = self.parent_entity.game_engine
				engine_reference.fire_event(success_event)
				engine_reference.render_to_screen()

class AutoLocomotion(Component):
	def __init__(self):
		super().__init__()

		self.ap_needed = 1

	def fire_event(self, event):
		if event.e_id == "move_by_self":
			borrow_points_event = BorrowActionPoints(self.ap_needed)
			self.parent_entity.fire_event(borrow_points_event)
			if borrow_points_event.borrow_fail == False:
				relative_move_event = RelativeMovement(event.del_x, event.del_y)
				self.parent_entity.fire_event(relative_move_event)
				if relative_move_event.is_successful == True:
					event.is_successful = True
				else:
					reimburse_event = IncreaseActionPoints(self.ap_needed)
					self.parent_entity.fire_event(reimburse_event)

class MovementController(Component):
	# this component is kinda useless... 
	# maybe i shud move the contents to player_tag component
	def __init__(self):
		super().__init__()

	def fire_event(self, event):
		if event.e_id == "move_command":
			new_event = MoveBySelf(event.del_x, event.del_y)
			self.parent_entity.fire_event(new_event)
			if not new_event.is_successful:
				get_pos_event = GetPosition()
				self.parent_entity.fire_event(get_pos_event)
				if get_pos_event.is_modified == True:
					my_pos_x = get_pos_event.pos_x
					my_pos_y = get_pos_event.pos_y
					activate_x = my_pos_x + event.del_x
					activate_y = my_pos_y + event.del_y
					self.parent_entity.game_engine.fire_event(
						ActivatePosition(activate_x, activate_y, self.parent_entity))

class AttachedCamera(Component):
	def __init__(self):
		super().__init__()

	def fire_event(self, event):
		if event.e_id == "get_camera_position":
			if event.is_modified == False:
				new_event = GetPosition()
				self.parent_entity.fire_event(new_event)
				if new_event.is_modified == True:
					event.pos_x = new_event.pos_x
					event.pos_y = new_event.pos_y
					event.is_modified = True

class Impassable(Component):
	def __init__(self):
		super().__init__()

	def fire_event(self, event):
		if event.e_id == "move_into":
			new_event = GetPosition()
			self.parent_entity.fire_event(new_event)
			if new_event.is_modified == True:
				my_pos_x = new_event.pos_x
				my_pos_y = new_event.pos_y
				if my_pos_x == event.new_pos_x and my_pos_y == event.new_pos_y:
					event.is_successful = False
		elif event.e_id == "get_impassable_nodes":
			get_pos_event = GetPosition()
			self.parent_entity.fire_event(get_pos_event)
			if get_pos_event.is_modified == True:
				my_pos_x = get_pos_event.pos_x
				my_pos_y = get_pos_event.pos_y
				my_pos = (my_pos_x, my_pos_y)
				event.impassable.append(my_pos)

class DialogueDispenser(Component):
	# work in progress
	# dialogue dispenser should choose between regular greet blahblah or quest talk...
	# ... or new rumours
	# it should have in hand these options and pick one before allowing the...
	# ... player to steer the converstn frm there 
	def __init__(self, dialogue):
		super().__init__()

		self.dialogue = dialogue

	def fire_event(self, event):
		if event.e_id == "activate_position":
			new_event = GetPosition()
			self.parent_entity.fire_event(new_event)
			if new_event.is_modified == True:
				my_pos_x = new_event.pos_x
				my_pos_y = new_event.pos_y
				if my_pos_x == event.pos_x and my_pos_y == event.pos_y:
					current_dialogue = self.dialogue
					while current_dialogue != None:
						whats_my_name_event = GetName()
						self.parent_entity.fire_event(whats_my_name_event)
						my_name = whats_my_name_event.name 
						My_name = first_capital(my_name)
						msg_to_log = My_name + ": " + current_dialogue.get_content()
						self.parent_entity.game_engine.log_msg(msg_to_log)
						current_dialogue = current_dialogue.next_dialogue

class Name(Component):
	def __init__(self, name, is_the_name=True):
		super().__init__()

		self.name = name
		# if something is "the_name", it can be appended to "the" unlike person's names etc
		self.is_the_name = is_the_name

	def fire_event(self, event):
		if event.e_id == "get_name":
			if (self.is_the_name == True) and (event.add_the == True):
				if event.the in ["a", "an"]:
					first = self.name[0].lower()
					if first in ["a", "e", "i", "o", "u"]:
						event.the = "an"
					else:
						event.the = "a"
				event.name = event.the + " " + self.name
			else:
				event.name = self.name
			event.is_modified = True

class Brain(Component):
	def __init__(self):
		super().__init__()

		self.goals = []
		self.last_action_failed = False

	def take_action(self):
		self.last_action_failed = False
		while True:
			while True:
				if self.goals == []:
					return
				if self.goals[-1].is_finished():
					del self.goals[-1]
				else:
					break
			if self.last_action_failed == True:
				return
			self.goals[-1].take_action()

	def fire_event(self, event):
		if event.e_id == "tick":
			my_own_event = SetBackgroundColor("red", 1)
			self.parent_entity.fire_event(my_own_event)
			self.take_action()
			my_own_event = SetBackgroundColor("black")
			self.parent_entity.fire_event(my_own_event)
		elif event.e_id == "push_goal":
			new_goal = event.goal
			self.add_goal(new_goal)
		elif event.e_id == "not_enough_action_points":
			self.last_action_failed = True

	def add_goal(self, goal):
		self.goals.append(goal)
		goal.parent_brain = self

class PlayerTag(Component):
	def __init__(self):
		super().__init__()

	def fire_event(self, event):
		if event.e_id == "get_player_entity":
			event.player_entity = self.parent_entity
			event.is_found = True
		elif event.e_id == "tick":
			change_bg_color_event = SetBackgroundColor("green", 1)
			self.parent_entity.fire_event(change_bg_color_event)
			game_engine_reference = self.parent_entity.game_engine
			game_engine_reference.render_to_screen()
			game_engine_reference.input_handler.listen_and_fire()
			change_bg_color_event = SetBackgroundColor("black")
			self.parent_entity.fire_event(change_bg_color_event)
		elif event.e_id == "get_player_info":
			get_health_event = GetValue("health")
			self.parent_entity.fire_event(get_health_event)
			if get_health_event.key_found == True:
				event.player_info["HP"] = get_health_event.value 
			get_ap_event = HowManyActionPoints()
			self.parent_entity.fire_event(get_ap_event)
			if get_ap_event.is_modified == True:
				event.player_info["AP"] = get_ap_event.num_action_points
		elif event.e_id == "provoke_default_melee_attack":
			attack_event = UseAttackOnEntity(event.victim_entity)
			self.parent_entity.fire_event(attack_event)
		elif event.e_id == "spot_activate_command":
			# WIP
			my_pos_event = GetPosition()
			self.parent_entity.fire_event(my_pos_event)
			my_pos_x = my_pos_event.pos_x
			my_pos_y = my_pos_event.pos_y 
			my_pos = (my_pos_x, my_pos_y)

			seek_entities_event = SeekActivableEntitiesAt(my_pos)
			engine_ref = self.parent_entity.game_engine
			engine_ref.fire_event(seek_entities_event)

			if seek_entities_event.entities_found != []:
				activable_entities_names = []
				for activable_entity in seek_entities_event.entities_found:
					get_name_event = GetName()
					activable_entity.fire_event(get_name_event)
					activable_entity_name = get_name_event.name

					activable_entities_names.append(activable_entity_name)

				log_window_ref = engine_ref.render_handler.log_window
				my_name_event = GetName(True)
				self.parent_entity.fire_event(my_name_event)
				my_name = my_name_event.name 
				prompt_msg = first_capital(
					my_name + " finds the following items on the floor-")
				selected_indices = log_window_ref.allow_choice(
						prompt_msg=prompt_msg, 
						options=activable_entities_names)

				for i, entity in enumerate(seek_entities_event.entities_found):
					if i in selected_indices:
						activate_pos_event = ActivatePosition(
								my_pos_x, my_pos_y, self.parent_entity, True)
						entity.fire_event(activate_pos_event)

class MonsterTag(Component):
	def __init__(self):
		super().__init__()

	def fire_event(self, event):
		if event.e_id == "activate_position":
			new_event = GetPosition()
			self.parent_entity.fire_event(new_event)
			if new_event.is_modified == True:
				my_pos_x = new_event.pos_x
				my_pos_y = new_event.pos_y
				if my_pos_x == event.pos_x and my_pos_y == event.pos_y:
					melee_event = ProvokeDefaultMeleeAttack(self.parent_entity)
					event.player_entity.fire_event(melee_event)

class MeleeAttack(Component):
	def __init__(self):
		super().__init__()

		self.ap_needed = 2
		self.base_power = 50

	def fire_event(self, event):
		if event.e_id == "look_for_attack_options":
			event.attack_options.append(self)
		elif event.e_id == "prepare_for_attack":
			victim_pos_event = GetPosition()
			event.victim_to_be.fire_event(victim_pos_event)
			if victim_pos_event.is_modified == True:
				victim_x = victim_pos_event.pos_x
				victim_y = victim_pos_event.pos_y
				victim_pos = (victim_x, victim_y)
				my_pos_event = GetPosition()
				self.parent_entity.fire_event(my_pos_event)
				if my_pos_event.is_modified == True:
					my_pos_x = my_pos_event.pos_x
					my_pos_y = my_pos_event.pos_y
					my_pos = (my_pos_x, my_pos_y)
					if my_pos in get_neighbors(victim_pos):
						latest_event = UseAttackOnEntity(event.victim_to_be)
						self.fire_event(latest_event)
					else:
						new_goal = ApproachEntity(event.victim_to_be)
						new_event = PushGoal(new_goal)
						self.parent_entity.fire_event(new_event)
		elif event.e_id == "use_attack_on_entity":
			borrow_points_event = BorrowActionPoints(self.ap_needed)
			self.parent_entity.fire_event(borrow_points_event)
			if not borrow_points_event.borrow_fail:
				my_the_name_event = GetName(True)
				self.parent_entity.fire_event(my_the_name_event)
				my_the_name = my_the_name_event.name
				My_the_name = first_capital(my_the_name)

				victim_the_name_event = GetName(True)
				event.entity.fire_event(victim_the_name_event)
				victim_the_name = victim_the_name_event.name

				msg = My_the_name + " attacks " + victim_the_name + "."
				self.parent_entity.game_engine.log_msg(msg)

				my_stats_event = GetCombatStats()
				self.parent_entity.fire_event(my_stats_event)
				my_stats = my_stats_event.combat_stats
				enemy_stats_event = GetCombatStats()
				event.entity.fire_event(enemy_stats_event)
				enemy_stats = enemy_stats_event.combat_stats
				level = 100
				attack_stat = my_stats.attack 
				attack_power = self.base_power 
				defense_stat = enemy_stats.defense 
				random_number = 100
				damage = (((((2 * level / 5 + 2) * 
						attack_stat * attack_power / defense_stat) / 50) + 2) * 
						random_number / 100)

				take_damage_event = TakeDamage(damage)
				event.entity.fire_event(take_damage_event)

class CombatStats(Component):
	def __init__(self, health, attack, defense, speed):
		super().__init__()

		self.health = health
		self.attack = attack
		self.defense = defense
		self.speed = speed

	def fire_event(self, event):
		if event.e_id == "get_attack_stat":
			event.attack = self.attack
		elif event.e_id == "get_combat_stats":
			event.combat_stats = self 
		elif event.e_id == "take_damage":
			last_health = self.health
			self.health = max(self.health - event.damage, 0)
			damage_taken = last_health - self.health

			my_name_event = GetName(True)
			self.parent_entity.fire_event(my_name_event)
			my_name = my_name_event.name 

			damage_msg = my_name + " loses " + str(damage_taken) + " health."
			damage_msg = first_capital(damage_msg)
			engine_ref = self.parent_entity.game_engine
			engine_ref.log_msg(damage_msg)

			if self.health == 0:
				engine_ref.entities.remove(self.parent_entity)

				my_pos_event = GetPosition()
				self.parent_entity.fire_event(my_pos_event)
				my_pos = (my_pos_event.pos_x, my_pos_event.pos_y)
				from entity import new_corpse
				engine_ref.add_entity(new_corpse(my_pos))

				death_msg = my_name + " dies."
				death_msg = first_capital(death_msg)
				engine_ref.log_msg(death_msg)
		elif event.e_id == "get_value":
			if event.key == "health":
				if event.key_found == False:
					event.value = self.health 
					event.key_found = True

class ActionPointsPool(Component):
	def __init__(self):
		super().__init__()

		self.action_points = 5

	def fire_event(self, event):
		if event.e_id == "borrow_action_points":
			if self.action_points >= event.num_points:
				self.action_points -= event.num_points
			else:
				event.borrow_fail = True
				newest_event = NotEnoughActionPoints()
				self.parent_entity.fire_event(newest_event)
		elif event.e_id == "tick":
			self.action_points = 5
		elif event.e_id == "increase_action_points":
			self.action_points += event.num_points
		elif event.e_id == "how_many_action_points":
			event.num_action_points = self.action_points
			event.is_modified = True

class PassComment(Component):
	def __init__(self):
		super().__init__()

	def fire_event(self, event):
		if event.e_id == "in_new_position":
			# the if here avoids the awkward entity passing itself notification
			if event.entity != self.parent_entity:
				get_player_event = GetPlayerEntity()
				engine_ref = self.parent_entity.game_engine
				engine_ref.fire_event(get_player_event)
				if get_player_event.is_found == True:
					player = get_player_event.player_entity
					if event.entity == player:
						my_pos_event = GetPosition()
						self.parent_entity.fire_event(my_pos_event)
						if my_pos_event.is_modified == True:
							my_pos = (my_pos_event.pos_x, my_pos_event.pos_y)
							if my_pos == event.pos:
								passer_name_event = GetName(True)
								event.entity.fire_event(passer_name_event)
								passer_name = passer_name_event.name

								my_name_event = GetName(True, "a")
								self.parent_entity.fire_event(my_name_event)
								my_name = my_name_event.name 

								my_msg = passer_name + " passes by " + my_name + "."
								my_msg = first_capital(my_msg)
								engine_ref.log_msg(my_msg)

class Pickable(Component):
	def __init__(self):
		super().__init__()

		self.parent_inventory = None 

	def fire_event(self, event):
		if event.e_id == "activate_position":
			# not required to check if parent_inventory is None...
			# this component receives non targetted events only when out of inventory
			# ie., when parent_inventory is None 
			if event.can_reach == True:
				my_pos_event = GetPosition()
				self.parent_entity.fire_event(my_pos_event)
				my_pos = (my_pos_event.pos_x, my_pos_event.pos_y)
				if (event.pos_x, event.pos_y) == my_pos:
					inventory_event = ToInventory(self.parent_entity)
					event.player_entity.fire_event(inventory_event)
		elif event.e_id == "set_value":
			if event.key == "parent_inventory":
				self.parent_inventory = event.key 

class Activable(Component):
	def __init__(self):
		super().__init__()

	def fire_event(self, event):
		if event.e_id == "seek_activable_entities_at":
			my_pos_event = GetPosition()
			self.parent_entity.fire_event(my_pos_event)
			my_pos = (my_pos_event.pos_x, my_pos_event.pos_y)

			if event.position == my_pos:
				event.entities_found.append(self.parent_entity)

class Inventory(Component):
	def __init__(self):
		super().__init__()

		self.contained_entities = []

	def fire_event(self, event):
		if event.e_id == "to_inventory":
			self.contained_entities.append(event.picked)
			set_event = SetValue("parent_inventory", self)
			event.picked.fire_event(set_event)
			engine_ref = self.parent_entity.game_engine
			engine_ref.entities.remove(event.picked)

			my_name_event = GetName(True)
			self.parent_entity.fire_event(my_name_event)
			my_name = my_name_event.name 

			picked_name_event = GetName(True)
			event.picked.fire_event(picked_name_event)
			picked_name = picked_name_event.name 

			new_msg = my_name + " picks up " + picked_name + "."
			new_msg = first_capital(new_msg)
			engine_ref.log_msg(new_msg)
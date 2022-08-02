import numpy as np

class Event:
	def __init__(self, e_id):
		self.e_id = e_id

class CallForRender(Event):
	def __init__(self, ascii_arr, fg_color_arr, bg_color_arr, camera_x, camera_y):
		super().__init__("call_for_render")

		self.ascii_arr = ascii_arr
		self.fg_color_arr = fg_color_arr
		this_shape = self.fg_color_arr.shape
		inf = 1000
		self.fg_priority_arr = np.full(shape=this_shape, fill_value=-inf)
		self.bg_color_arr = bg_color_arr
		self.bg_priority_arr = np.full(shape=this_shape, fill_value=-inf)
		self.camera_x = camera_x
		self.camera_y = camera_y

class GetPosition(Event):
	def __init__(self):
		super().__init__("get_position")

		self.pos_x = 0
		self.pos_y = 0
		self.is_modified = False

class GetName(Event):
	def __init__(self, add_the=False, the="the"):
		super().__init__("get_name")

		self.name = "???"
		self.add_the = add_the
		self.the = the
		self.is_modified = False

class RelativeMovement(Event):
	def __init__(self, del_pos_x, del_pos_y):
		super().__init__("relative_movement")

		self.del_pos_x = del_pos_x
		self.del_pos_y = del_pos_y
		self.is_successful = False

class MoveCommand(Event):
	def __init__(self, del_x, del_y):
		super().__init__("move_command")

		self.del_x = del_x
		self.del_y = del_y

class SpotActivateCommand(Event):
	def __init__(self):
		super().__init__("spot_activate_command")

class GetCameraPosition(Event):
	def __init__(self):
		super().__init__("get_camera_position")

		self.pos_x = 0
		self.pos_y = 0
		self.is_modified = False

class MoveInto(Event):
	def __init__(self, moving_entity, new_pos_x, new_pos_y):
		super().__init__("move_into")

		self.moving_entity = moving_entity
		self.new_pos_x = new_pos_x
		self.new_pos_y = new_pos_y
		self.is_successful = True

class ActivatePosition(Event):
	# only player uses this... others use the events of exact context
	def __init__(self, pos_x, pos_y, player_entity, can_reach=False):
		super().__init__("activate_position")

		self.pos_x = pos_x
		self.pos_y = pos_y
		self.player_entity = player_entity
		self.can_reach = can_reach
		self.activable_entities = []

class SeekActivableEntitiesAt(Event):
	def __init__(self, position):
		super().__init__("seek_activable_entities_at")

		self.position = position
		self.entities_found = []

class GetPlayerEntity(Event):
	def __init__(self):
		super().__init__("get_player_entity")

		self.player_entity = None
		self.is_found = False

class Tick(Event):
	# entities with the brain component listen for this
	def __init__(self):
		super().__init__("tick")

class GetImpassableNodes(Event):
	def __init__(self):
		super().__init__("get_impassable_nodes")

		self.impassable = []

class LookForAttackOptions(Event):
	def __init__(self):
		super().__init__("look_for_attack_options")

		self.attack_options = []

class PushGoal(Event):
	def __init__(self, goal):
		super().__init__("push_goal")

		self.goal = goal

class PrepareForAttack(Event):
	def __init__(self, victim_to_be):
		super().__init__("prepare_for_attack")

		self.victim_to_be = victim_to_be

class MoveBySelf(Event):
	def __init__(self, del_x, del_y):
		super().__init__("move_by_self")

		self.del_x = del_x
		self.del_y = del_y
		self.is_successful = False

class UseAttackOnEntity(Event):
	def __init__(self, entity):
		super().__init__("use_attack_on_entity")

		self.entity = entity

class BorrowActionPoints(Event):
	def __init__(self, num_points):
		super().__init__("borrow_action_points")

		self.num_points = num_points
		self.borrow_fail = False

class NotEnoughActionPoints(Event):
	def __init__(self):
		super().__init__("not_enough_action_points")

class IncreaseActionPoints(Event):
	def __init__(self, num_points):
		super().__init__("increase_action_points")

		self.num_points = num_points

class GetPlayerInfo(Event):
	def __init__(self):
		super().__init__("get_player_info")

		self.player_info = {}

class HowManyActionPoints(Event):
	def __init__(self):
		super().__init__("how_many_action_points")

		self.num_action_points = 0
		self.is_modified = False

class GetAttackStat(Event):
	def __init__(self):
		super().__init__("get_attack_stat")

		self.attack = 0

class ProvokeDefaultMeleeAttack(Event):
	def __init__(self, victim_entity):
		super().__init__("provoke_default_melee_attack")

		self.victim_entity = victim_entity

class SetBackgroundColor(Event):
	def __init__(self, bg_color, bg_priority=0):
		super().__init__("set_background_color")

		self.bg_color = bg_color 
		self.bg_priority = bg_priority

class GetCombatStats(Event):
	def __init__(self):
		super().__init__("get_combat_stats")

		self.combat_stats = None 

class TakeDamage(Event):
	def __init__(self, damage):
		super().__init__("take_damage")
		
		self.damage = damage 

class InNewPosition(Event):
	def __init__(self, entity, pos):
		super().__init__("in_new_position")

		self.entity = entity 
		self.pos = pos 

class GetValue(Event):
	def __init__(self, key):
		super().__init__("get_value")

		self.key = key 
		self.value = None 
		self.key_found = False

class ToInventory(Event):
	def __init__(self, picked):
		super().__init__("to_inventory")

		self.picked = picked

class SetValue(Event):
	def __init__(self, key, value):
		super().__init__("set_value")

		self.key = key 
		self.value = value 
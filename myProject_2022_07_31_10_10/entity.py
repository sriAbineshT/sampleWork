from component import *
from goal import *

class Entity:
	def __init__(self):
		self.components = []
		self.game_engine = None

	def fire_event(self, event):
		for component in self.components:
			component.fire_event(event)

	def add_component(self, component):
		for existing_component in self.components:
			if type(existing_component) == type(component):
				self.components.remove(existing_component)
		self.components.append(component)
		component.parent_entity = self

	def remove_component(self, component_class):
		for component in self.components:
			if isinstance(component, component_class):
				self.components.remove(component)

def new_simpleton(position):
	simpleton = Entity()

	simpleton.add_component(Renderable("s"))
	pos_x, pos_y = position
	simpleton.add_component(Position(pos_x, pos_y))
	simpleton.add_component(Name("simpleton"))

	simpleton.add_component(PassComment())

	return simpleton

def new_origin():
	origin = new_simpleton((0, 0))

	origin.add_component(Renderable("X", fg_priority=-3))
	origin.add_component(Name("origin", False))

	origin.remove_component(PassComment)

	return origin 

def new_corpse(position):
	corpse = new_simpleton(position)

	corpse.add_component(Renderable("&", fg_priority=-1))
	corpse.add_component(Name("corpse"))

	return corpse

def new_pickable(position):
	pickable = new_simpleton(position)

	pickable.add_component(Renderable("/", fg_priority=-2))
	pickable.add_component(Activable())
	pickable.add_component(Name("pickable"))

	pickable.add_component(Pickable())

	return pickable

def new_obstacle(position):
	obstacle = new_simpleton(position)

	obstacle.add_component(Renderable("#"))
	obstacle.add_component(Name("obstacle"))

	obstacle.add_component(Impassable())

	return obstacle

def new_wall(position):
	wall = new_obstacle(position)

	wall.add_component(Renderable("#", "dark_grey"))
	wall.add_component(Name("wall"))

	return wall

def new_player(position):
	player = new_obstacle(position)

	player.add_component(Renderable("@", "blue"))
	player.add_component(Name("player"))
	
	player.add_component(ActionPointsPool())
	player.add_component(AutoLocomotion())
	player.add_component(CombatStats(100, 100, 100, 100))
	player.add_component(MeleeAttack())

	player.add_component(PlayerTag())
	player.add_component(AttachedCamera())
	player.add_component(MovementController())

	# test block
	player.add_component(Inventory())
	
	return player

def new_monster(position, player):
	monster = new_obstacle(position)

	monster.add_component(Renderable("m", "light_red"))
	monster.add_component(Name("monster"))

	monster.add_component(ActionPointsPool())
	monster.add_component(AutoLocomotion())
	monster.add_component(CombatStats(50, 50, 50, 50))
	monster.add_component(MeleeAttack())

	monster.add_component(MonsterTag())
	brain = Brain()
	goal = KillEntity(player)
	brain.add_goal(goal)
	monster.add_component(brain)

	return monster 

def new_goblin(position, player):
	goblin = new_monster(position, player)

	goblin.add_component(Renderable("g", "green"))
	goblin.add_component(Name("goblin"))
	
	return goblin
import numpy as np

def get_neighbors(node):
		node_x, node_y = node
		north_node = (node_x, node_y - 1)
		west_node = (node_x - 1, node_y)
		south_node = (node_x, node_y + 1)
		east_node = (node_x + 1, node_y)
		return [north_node, west_node, south_node, east_node]

def get_h_cost(node, target_node):
		node_x, node_y = node
		target_x, target_y = target_node
		return abs(node_x - target_x) + abs(node_y - target_y)

def get_path_nodes(start_node, target_node, impassable=[]):
	# the next block is a hotfix
	if target_node in impassable:
		impassable.remove(target_node)

	open_nodes = []
	closed_nodes = []
	open_nodes.append(start_node)

	cache = {}
	g_cost = 0
	h_cost = get_h_cost(start_node, target_node)
	f_cost = g_cost + h_cost 
	parent = None
	cache[start_node] = {
		"g" : g_cost, 
		"h" : h_cost, 
		"f" : f_cost, 
		"p" : parent
	}

	while len(open_nodes) > 0:
		current = open_nodes[0]
		lowest_f_cost = cache[current]["f"]
		for node in open_nodes:
			if cache[node]["f"] < lowest_f_cost:
				current = node
				lowest_f_cost = cache[current]["f"]
		open_nodes.remove(current)
		closed_nodes.append(current)

		if current == target_node:
			break

		for neighbor in get_neighbors(current):
			if neighbor in impassable or neighbor in closed_nodes:
				continue

			g_cost = cache[current]["g"] + 1
			condition_1 = True
			if neighbor in cache.keys():
				condition_1 = g_cost < cache[neighbor]["g"]
			if condition_1 or neighbor not in open_nodes:
				h_cost = get_h_cost(neighbor, target_node)
				f_cost = g_cost + h_cost
				parent = current
				cache[neighbor] = {
					"g" : g_cost, 
					"h" : h_cost, 
					"f" : f_cost, 
					"p" : parent
				}
				if neighbor not in open_nodes:
					open_nodes.append(neighbor)

	path_nodes = []
	now_node = target_node
	while True:
		path_nodes.append(now_node)
		if cache[now_node]["p"] == None:
			break
		else:
			now_node = cache[now_node]["p"]
	path_nodes.reverse()

	return path_nodes

def help_visualise_path(path_nodes, start_node, target_node, impassable, inf=1000):
	x_min = inf 
	y_min = inf 
	x_max = -inf
	y_max = -inf

	for node in path_nodes + impassable:
		x, y = node
		x_min = min(x, x_min)
		y_min = min(y, y_min)
		x_max = max(x, x_max)
		y_max = max(y, y_max)

	num_rows = y_max - y_min + 1
	num_cols = x_max - x_min + 1

	path_arr = np.full(shape=(num_rows, num_cols), fill_value=" ")
	for node in path_nodes:
		x, y = node
		row = y - y_min
		col = x - x_min
		path_arr[row, col] = "."
	start_x, start_y = start_node
	row = start_y - y_min
	col = start_x - x_min
	path_arr[row, col] = "@"
	target_x, target_y = target_node
	row = target_y - y_min
	col = target_x - x_min
	path_arr[row, col] = "X"
	for blocking_node in impassable:
		x, y = blocking_node
		row = y - y_min
		col = x - x_min
		path_arr[row, col] = "#"

	for row in range(num_rows):
		for col in range(num_cols):
			print(path_arr[row, col], end="")
		print()
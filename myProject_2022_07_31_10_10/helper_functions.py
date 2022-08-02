import numpy as np
from msvcrt import getwch, kbhit

def find_entity_position(entity):
	get_pos_event = GetPosition()
	entity.fire_event(get_pos_event)
	if get_pos_event.is_modified == True:
		entity_pos = (get_pos_event.pos_x, get_pos_event.pos_y)
		return entity_pos
	else:
		return False

def draw_img_on_canvas(img_arr, canvas_arr, top_left):
	img_num_rows, img_num_cols = img_arr.shape
	canvas_num_rows, canvas_num_cols = canvas_arr.shape
	left, top = top_left
	bottom = top + img_num_rows - 1
	right = left + img_num_cols - 1

	if left >= canvas_num_cols or right < 0 or top >= canvas_num_rows or bottom < 0:
		return

	start_row = 0
	start_col = 0
	end_row = img_num_rows - 1
	end_col = img_num_cols - 1

	if left < 0:
		start_col = -left
		left = 0
	if right >= canvas_num_cols:
		end_col -= (right - canvas_num_cols + 1)
		right = canvas_num_cols - 1
	if top < 0:
		start_row = -top
		top = 0
	if bottom >= canvas_num_rows:
		end_row -= (bottom - canvas_num_rows + 1)
		bottom = canvas_num_rows - 1

	if start_row <= end_row and start_col <= end_col:
		canvas_arr[top : bottom + 1, left : right + 1] = img_arr[
															start_row : end_row + 1, 
															start_col : end_col + 1
															]

def get_top_bar(top_bar_says, width, highlighted=False):
	if highlighted == False:
		padding_character = "-"
		bg_color = "black"
	else:
		padding_character = "="
		bg_color = "blue"

	num_x = (width - len(top_bar_says)) % 2
	new_top_bar_says = top_bar_says + padding_character * num_x
	num_y = (width - len(new_top_bar_says)) // 2
	top_bar_content = padding_character * num_y + new_top_bar_says + padding_character * num_y

	top_bar = np.full(shape=(1, width), fill_value=" ")
	fg_bar = np.full(shape=(1, width), fill_value="white", dtype="object")
	bg_bar = np.full(shape=(1, width), fill_value=bg_color, dtype="object")
	for col in range(width):
		top_bar[0, col] = top_bar_content[col]
	
	return top_bar, fg_bar, bg_bar

def centre_align(text, length, left_biased=True):
	# if left_biased text is more to the left in clashing cases
	num_x = (length - len(text)) % 2
	if left_biased:
		new_text = text + " " * num_x
	else:
		new_text = " " * num_x + text
	num_y = (length - len(new_text)) // 2
	final_text = " " * num_y + new_text + " " * num_y
	return final_text

def centre_align_vertical(lines, height, top_biased=True):
	# if top_biased text is more to the top in clashing cases
	num_x = (height - len(lines)) % 2
	if top_biased:
		new_lines = lines + ["", ] * num_x
	else:
		new_lines = ["", ] * num_x + lines 
	num_y = (height - len(new_lines)) // 2
	final_lines = ["", ] * num_y + new_lines + ["", ] * num_y
	return final_lines 

def centre_align_both(lines, length, height, left_biased=True, top_biased=True):
	vertical_aligned_lines = centre_align_vertical(lines, height, top_biased)
	for i, line in enumerate(vertical_aligned_lines):
		horizontal_aligned_line = centre_align(line, length, left_biased)
		vertical_aligned_lines[i] = horizontal_aligned_line
	return vertical_aligned_lines

def first_capital(text):
	T = text[0].upper()
	ext = text[1 : ]
	Text = T + ext 
	return Text

def custom_getwch():
	while kbhit() == True:
		getwch()
	usr_key = getwch().lower()
	return usr_key

def print_ascii_arr(ascii_arr):
	num_rows, num_cols = ascii_arr.shape 
	for row in range(num_rows):
		for col in range(num_cols):
			print(ascii_arr[row, col], end="")
		print()
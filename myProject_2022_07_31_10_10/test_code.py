from menu import *
from helper_functions import *

n = 10
items = ["x" * (n - i) for i in range(n)]
test_menu = Menu(items)
for i in range(5, 15):
	print_ascii_arr(test_menu.get_ascii_arr(centre_aligned=False, shape=(None, i)))
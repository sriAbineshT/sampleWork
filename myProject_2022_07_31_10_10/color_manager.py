import os

os.system("")

reset = '\033[0m'
fg_colors_dict = {
	"black" : '\033[30m', 
    "red" : '\033[31m', 
    "green" : '\033[32m', 
    "orange" : '\033[33m', 
    "blue" : '\033[34m', 
    "purple" : '\033[35m', 
    "cyan" : '\033[36m', 
    "light_grey" : '\033[37m', 
    "dark_grey" : '\033[90m', 
    "light_red" : '\033[91m', 
    "light_green" : '\033[92m', 
    "yellow" : '\033[93m', 
    "light_blue" : '\033[94m', 
    "pink" : '\033[95m', 
    "light_cyan" : '\033[96m'
}
bg_colors_dict = {
    "black" : '\033[40m', 
    "red" : '\033[41m', 
    "green" : '\033[42m', 
    "orange" : '\033[43m', 
    "blue" : '\033[44m', 
    "purple" : '\033[45m', 
    "cyan" : '\033[46m', 
    "light_grey" : '\033[47m'
}

def my_print(text, fg_color=None, bg_color=None, end="\n"):
    prefix = fg_colors_dict.get(fg_color, "") + bg_colors_dict.get(bg_color, "")
    suffix = reset
    my_text = prefix + text + suffix
    print(my_text, end=end)
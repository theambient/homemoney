
def print_color(color, text):
	print('\033[{}m{}\033[0m'.format(color, text))

def print_yellow(text):
	print_color('33', text)

def print_red(text):
	print_color('31', text)

def print_dim(text):
	print_color('2', text)

def print_green(text):
	print_color('32', text)

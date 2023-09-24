import time
import random
import curses
from curses import wrapper 


def start_screen(stdscr):
	#stdscr.addstr(1 , 0, "Hello world!",curses.color_pair(1))
		#skips one line & starts at the character of index 0 (line=1,index=0)
	stdscr.clear()
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)
	stdscr.addstr(1, 0, f"WPM: {wpm}")

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)

def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def wpm_test(stdscr):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True) #Don't wait for the user to input a key

	while True:
		time_elapsed = max(time.time() - start_time, 1) # to avoid dividing by 0
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5) # average word has 5 letters

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh() 

		#converts a list to a string / combines every single character of the list with the "delimitor/Separator"
		if "".join(current_text)  == target_text:
			stdscr.nodelay(False)
			break
		# Try/Except to avoid the Error raised by stdscr.nodelay()/stdscr.getkey()
		try:
			key = stdscr.getkey() 
		# This acts like a block, just like the input() function
		except:
			continue

		if ord(key) == 27: # ASCII code for escape character
			break

		#To check for the backspace character in different OS
		if key in ("KEY_BACKSPACE", '\b', '\x7f'):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)

def main(stdscr):
	#must do it inside the scope of the function after initializing curses
	#1 is the id of this pair of foreground & background colors
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) 
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
	while True:
		wpm_test(stdscr)
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
		key = stdscr.getkey()

		if ord(key) == 27:
			break

wrapper(main) 
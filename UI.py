# This file covers UI classes and user input handling
# It is intended as the main file to be run

import tkinter as tk
from tkinter import font as tkfont
import sys
import shelve

import locations


class Game(tk.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.geometry('1500x800')
		self.config(background='black')

		self.world = None
		self.player = None
		self.current_game = 'Unsaved Game'
		self.game_screen = GameScreen(self)
		self.game_screen.grid(row=0, column=0)

		self.game_screen.player_input.focus_force()

		self.bind_game_keys()


	# ---------- Text handling methods ------------

	def display_text_output(self, text, command_readback = False):

		self.game_screen.text_output.configure(state='normal')

		if command_readback == True:
			text = text + '\n'

		else:
			text = text + '\n> '

		self.game_screen.text_output.insert('end', text)
		self.game_screen.text_output.configure(state='disabled')

		self.game_screen.text_output.see('end')

# ---- Keybound functions ----
	def execute_player_command(self, event):
		player_action_command = self.parse_player_action_command()
		self.execute_command(player_action_command)

# ---- Command Processing ----

	def execute_command(self, action_command):

		# if action_command:
		# 	print('verb: ' + action_command.verb)
		# 	print('target: ' + action_command.target)
		# 	print('IO: ' + action_command.direct_object)
		# 	print('quantity: ' + str(action_command.quantity))
		# 	print(action_command.system_command)
		# else:
		# 	print('no action_command object generated')

		# ---- Handle system commands ----


		# Special handlings
		if action_command.verb in ['n','north','e','east','s','south','w','west']:
			action_command.target = action_command.verb
			action_command.verb = 'go'

		if action_command.system_command:
			if action_command.system_command == 'main menu':
				self.game_screen.player_input.configure(state='disabled')
				self.main_menu()
			if action_command.system_command == 'quit':
				self.quit()
			if action_command.system_command == 'pause':
				pass


		# ---- Handle Verbs ----

		if action_command.verb == 'look':
			if not action_command.target:
				self.display_text_output(self.player.location.describe())
			else:
				self.display_text_output(action_command.target.describe())

			# Now check inventory, items in location, people in location, features in location, anything that can currently be looked at. Might need a function that returns a dictionary of names of these items matched to the object.
			#if action_command.target in

		elif action_command.verb == 'go':

			if not action_command.target:
				self.display_text_output('Where do you want to go?')

			elif action_command.target in ['n','e','w','s','north','east','west','south']:
				if action_command.target == 'n':
					action_command.target = 'north'
				if action_command.target == 'e':
					action_command.target = 'east'
				if action_command.target == 'w':
					action_command.target = 'west'
				if action_command.target == 's':
					action_command.target = 'south'

				if action_command.target in action_command.subject.location.get_exits():
					action_command.subject.move(direction=action_command.target)
				else:
					self.display_text_output('You can\'t go that way!')

			elif action_command.target:
				for es in action_command.subject.location.special_exits:
					if action_command.target == es.name:
						action_command.subject.move(exit=es)

			else:
				self.display_text_output('I\'m not sure where you want to go.')

			if action_command.subject == self.player:
				self.display_text_output(self.player.location.describe())

		# Player only verbs
		elif action_command.verb == 'i' or 'inv' or 'inventory':
			self.player.get_inventory()


		# Subject verbs
		elif action_command.verb == 'eat':
			pass

		elif action_command.verb == 'get' or 'take':
			if action_command.direct_object:
				action_command.subject.get_item(action_command.direct_object, target=action_command.target)
			else:
				action_command.subject.get_item(action_command.target)



	def parse_player_action_command(self):

		system_commands = ['main menu', 'pause', 'quit']
		
		# If verb lists gets very large, possibly make them global so they are not constantly destroyed and recreated
		player_only_verbs = ['i', 'inv', 'inventory']
		world_verbs = ['look', 'go', 'n', 'north', 'e', 'east', 'w', 'west', 's', 'south']
		subject_verbs = ['eat', ' drink'] # Subject acts on self
		social_verbs = ['talk', 'shop', 'buy', 'sell', 'give'] # Involves other people
		item_verbs = ['get', 'take', 'drop']
		verblist = world_verbs + subject_verbs + social_verbs + item_verbs

		player_command = ActionCommand(self)
		player_command.subject = self.player

		player_input = self.get_player_input()
		self.display_text_output(player_input, command_readback=True)
		words = player_input.split()

		if player_input in system_commands:
			player_command.system_command = player_input
			return player_command

		if len(words) == 0:
			self.display_text_output('Please enter something.')
			return None
 
		if words[0] not in verblist:
			self.display_text_output('I don\'t understand what you\'re trying to do')
			return None

		# ---- Begin parse ----

		for p in self.player.location.denizens:
			if action_command.target == p.name:
				action_command.target = p

		# If 1 word, it's just a verb
		# If 2 words it's a verb and a target

		player_command.verb = words[0]

		# Single verb commands
		if len(words) == 1:
			return player_command

		if len(words) == 2:
			player_command.target = words[1]

		# Quantity
		for w in words:
			if w.isdigit():
				# -- checks --
				# ensure DO follows
				if words.index(w) == len(words)-1:
					self.display_text_output(player_command.verb + ' ' + w + ' of what?')
					return None
				# ensure only 1 number. Improve by checking full words[] for any 2 numbers
				if words[words.index(w)+1].isdigit():
					player_command.not_understood()
					return None
				player_command.quantity = w

		# Sentence flow words
		if 'for' in words:
			player_command.indirect_object = words[words.index('for')+1]

		if 'at' in words:
			player_command.target = words[words.index('at')+1]

		if 'to' in words:
			if player_command.verb == 'give': # Verb requires DO
				player_command.direct_object = words[words.index('to')-1]
			player_command.target = words[words.index('to')+1]

		# Handle getting item from a container, interactable's container, stealing
		if 'from' in words:
			if player_command.verb == 'get' or 'take': # Verbs that require DO
				player_command.direct_object = words[words.index('from')-1]
			player_command.target = words[words.index('from')+1]

		# Verb grouping defaults
		if player_command.verb in subject_verbs:
			player_command.target = self.player

		# Before returning command, make sure target is valid

		present_stuff = self.player.inventory + self.player.location.items + self.player.location.special_exits + self.player.location.denizens + self.player.location.harvestables + self.player.location.interactables
		for ps in present_stuff:
			if player_command.target == ps.name:
				player_command.target = ps
			else:
				self.display_text_output('I can not find "'+ player_command.target + '" here.')
				return None

		return player_command

		# Unhandled:
		# Under, In, as in "look under bed". A position attribute for the items "under" the bed or "in" the drawer?	
		# From, as in "drink from fountain"

	def get_player_input(self):

		player_input_text = self.game_screen.player_input.get(1.0, 'end-2l lineend')
		self.game_screen.player_input.delete(1.0, 'end')

		return player_input_text


# ---- Game system methods ----

	def bind_game_keys(self):
		self.bind('<Escape>', self.escape_main_menu)
		self.bind('<Return>', self.execute_player_command)

	def unbind_game_keys(self):
		self.unbind('<Escape>')
		self.unbind('<Return>')

	def new_game(self):
		pass

	def main_menu(self):
		self.unbind_game_keys()
		self.menu = MainMenu(self)
		self.menu.grid(row=0, column=0, rowspan=3, columnspan=5, sticky='nsew')

	def escape_main_menu(self, event):
		
		self.main_menu()

	def start(self):
		self.main_menu()
		self.mainloop()

	def quit(self):
		self.destroy()


class MainMenu(tk.Frame):

	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent

		self.base_path = locations.os.path.dirname(locations.os.path.realpath(__file__))
		self.save_path = locations.os.path.join(self.base_path, 'saves')
		if not locations.os.path.exists(self.save_path):
			locations.os.makedirs(self.save_path)

		self.heading_font = tkfont.Font(family='Helvetica', size=18, weight='bold')
		self.button_font = tkfont.Font(family='Helvetica', size=13)
		self.current_game_font = tkfont.Font(family='Helvetica', size=10, slant='italic')

		self.configure(background = 'blue')
	
		self.parent.bind('<Escape>', self.escape_to_menu)
		
		self.heading = tk.Label(self, text='Hearthfire', font=self.heading_font)
		self.heading.pack(side='top', pady=30)
		self.create_widgets()

	def resume(self):
		# This might not be kosher by Uncle Bob's 
		self.parent.bind_game_keys()
		self.parent.game_screen.player_input.configure(state='normal')
		self.parent.game_screen.player_input.focus_set()

		self.destroy()

	def quit(self):
		self.parent.quit()

	def start_new_game(self):

		self.parent.world = locations.World()
		self.parent.current_game = 'unsaved new game'
		self.parent.player = locations.people.Player(game=self.parent, name='player', location=self.parent.world.map[(10,10)].map[(5,5)])

		self.resume()
		self.parent.display_text_output(self.parent.player.location.describe())

	def open_save_menu(self):

		# Still needs "back to main menu" button
		self.destroy_widgets()
		self.create_save_menu_widgets()
		self.save_name_entry.focus_set()

	def save_game(self, event):
		save_name = self.save_name_entry.get()

		d = shelve.open(self.save_path+'/'+save_name)
		d['world'] = self.parent.world
		d['player'] = self.parent.player
		self.parent.current_game = save_name

		self.destroy_save_menu_widgets()
		self.create_widgets()

	def open_load_menu(self):

		self.destroy_widgets()
		self.create_load_game_menu_widgets()

	def load_game(self, event):

		w = event.widget
		load_name = w.get(int(w.curselection()[0]))

		d = shelve.open(self.save_path+'/'+load_name)

		self.parent.world = d['world']
		self.parent.player = d['player']
		setattr(self.parent.player, 'game', self.parent)
		setattr(self.parent, 'current_game', load_name)

		self.parent.player.show_location()
		self.destroy_load_game_menu_widgets()
		self.create_widgets()

	def delete_saved_game(self):
		
		self.delete_popup = tk.Toplevel(self)
		self.delete_popup.title=('Delete game?')
		delete_popup_message = tk.Message(self.delete_popup, text='You are about to delete your game. The entire world, including your self, will be permanently destroyed. Are you sure you wish to do this?')
		confirm_delete = tk.Button(self.delete_popup, text='Yes, destroy everything.', command=self.confirm_delete)
		cancel_delete = tk.Button(self.delete_popup, text='No, I can\'t, I won\'t do it!', command=self.delete_popup.destroy)
		
		delete_popup_message.pack()
		confirm_delete.pack()
		cancel_delete.pack()

	def confirm_delete(self):
		index = int(self.saved_games_list.curselection()[0])
		delete_name = self.saved_games_list.get(index)
		for file in locations.os.listdir(self.save_path):
			if file[0:-4] == delete_name:
				locations.os.remove(self.save_path+'/'+file)
					
		self.delete_popup.destroy()
		self.refresh_saved_games_list()

	def show_game_info(self, event):

		w = event.widget
		game_name = w.get(int(w.curselection()[0]))

		d = shelve.open(self.save_path+'/'+game_name)
		load_player = d['player']
		player_name = load_player.__dict__['name']
		self.saved_game_info_box.config(text='Player: '+player_name)

	def create_widgets(self):

		self.resume_button = tk.Button(self, text='Resume Game', font=self.button_font, command=lambda: self.resume())
		self.new_game_button = tk.Button(self, text='New Game', font=self.button_font, command=lambda: self.start_new_game())
		self.quit_button = tk.Button(self, text='Quit Game', font=self.button_font, command=lambda: self.quit())
		self.save_button = tk.Button(self, text='Save Game', font=self.button_font, command=lambda: self.open_save_menu())
		self.load_button = tk.Button(self, text='Load Game', font=self.button_font, command=lambda: self.open_load_menu())

		self.current_game_label = tk.Label(self, text='Current game file: ' + self.parent.current_game, font=self.current_game_font)

		if self.parent.world:
			self.current_game_label.pack()

		if self.parent.world:
			self.resume_button.pack(pady=10)
		if self.parent.world:
			self.save_button.pack(pady=10)
		self.new_game_button.pack(pady=10)
		self.load_button.pack(pady=10)
		self.quit_button.pack(pady=10)

	def destroy_widgets(self):

		self.resume_button.destroy()
		self.new_game_button.destroy()
		self.quit_button.destroy()
		self.save_button.destroy()
		self.load_button.destroy()
		self.current_game_label.destroy()

	def toggle_save_button(self, *args):
		x = self.saveEntryVar.get()
		if len(x) > 0:
			self.save_game_button.config(state='normal')
		if len(x) == 0:
			self.save_game_button.config(state='disabled')

	def create_save_menu_widgets(self):
		self.create_saved_games_list('save')

		self.saveEntryVar = tk.StringVar()
		self.saveEntryVar.trace('w', self.toggle_save_button)
		self.save_name_entry = tk.Entry(self, textvariable=self.saveEntryVar)
		self.save_game_button = tk.Button(self, text='Save Game', command=lambda:self.save_game(event=None))

		# Do lists and for loop to pack
		self.saved_games_list.pack()
		self.delete_button.pack()
		self.saved_game_info_box.pack()
		self.save_name_entry.pack()
		self.save_game_button.pack()
		

	def create_load_game_menu_widgets(self):
		self.create_saved_games_list('load')

		self.saved_game_info_box.pack()
		self.saved_games_list.pack()
		self.delete_button.pack()

	def destroy_save_menu_widgets(self):
		
		self.saved_games_list.destroy()
		self.saved_game_info_box.destroy()
		self.delete_button.destroy()
		self.save_name_entry.destroy()
		self.save_game_button.destroy()

	def destroy_load_game_menu_widgets(self):

		self.saved_games_list.destroy()
		self.saved_game_info_box.destroy()
		self.saved_game_info_box.destroy()
		self.delete_button.destroy()

	def create_saved_games_list(self, mode):
		self.saved_games_list = tk.Listbox(self)
		self.saved_game_info_box = tk.Label(self)
		self.delete_button = tk.Button(self, text='Delete Game', command=self.delete_saved_game)
		self.refresh_saved_games_list()

		self.saved_games_list.bind('<<ListboxSelect>>', self.show_game_info)
		if mode == 'load':
			self.saved_games_list.bind('<Return>', self.load_game)
			self.saved_games_list.bind('<Double-Button-1>', self.load_game)
		if mode == 'save':
			self.saved_games_list.bind('<Return>', self.save_game)
			self.saved_games_list.bind('<Double-Button-1>', self.save_game)
			self.saved_games_list.bind('<<ListboxSelect>>', self.enter_selected_game_name)

	def enter_selected_game_name(self, event):
		w = event.widget # try condensing w
		game_name = w.get(int(w.curselection()[0]))
		self.save_name_entry.delete(0, 'end')
		self.save_name_entry.insert(0, game_name)
		self.save_name_entry.focus_set() # This isn't working

	
	def refresh_saved_games_list(self):
		self.saved_games_list.delete(0, 'end')
		
		saves_list = self.get_saves() # try reading directly into loop
		for s in saves_list:
			self.saved_games_list.insert('end', s)

	def get_saves(self):
		saves_list = []
		for file in locations.os.listdir(self.save_path):
			if file.endswith('dir'):
				saves_list.append(file[0:-4])
		return saves_list

	def return_to_menu(self):
		# Next two lines of code prevent certain widgets from being refreshed, but seems like a lot of code for this.
		widgets_to_preserve = [self.heading]
		for w in [i for i in self.parent.menu.winfo_children() if i not in widgets_to_preserve]:
			w.destroy()
		self.create_widgets()

	def escape_to_menu(self, event):
		self.return_to_menu()


class GameScreen(tk.Frame):

	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent

		self.create_widgets()

	def create_widgets(self):

		# Borders
		self.left_border = tk.Frame(self, height=800, width=25, bg='thistle4')
		self.middle_border = tk.Frame(self, height=800, width=25, bg='thistle4')
		self.right_border = tk.Frame(self, height=800, width=25, bg='thistle4')

		self.top_border_left = tk.Frame(self, height=20, width=850, bg='thistle4')
		self.top_border_right = tk.Frame(self, height=20, width=575, bg='thistle4')
		self.bottom_border_left = tk.Frame(self, height=20, width=850, bg='thistle4')
		self.bottom_border_right = tk.Frame(self, height=20, width=575, bg='thistle4')

		self.left_border.grid(row=0, column=0, rowspan=3)
		self.middle_border.grid(row=0, column=2, rowspan=3)
		self.right_border.grid(row=0, column=4, rowspan=3)

		self.top_border_left.grid(row=0, column=1, sticky='n')
		self.top_border_right.grid(row=0, column=3, sticky='n')
		self.bottom_border_left.grid(row=2, column=1, sticky='s')
		self.bottom_border_right.grid(row=2, column=3, sticky='s')

		# Container Frames
		self.text_frame = tk.Frame(self, height=760, width=850, bg='black')
		self.visual_frame = tk.Frame(self, height=760, width=575, bg='thistle3')

		self.text_frame.grid(row=1, column=1, sticky='nsew')
		self.visual_frame.grid(row=1, column=3)

		# I am still a little confused. These lines I assume apply to the text_frame as it occupies this grid location and it affects how the contained packed widget - text_output.pack(expand=True, fill='y') - fills the grid cell. It does what I want though.  3/4 - It's because the containing frame (being referened in these lines), also needs to be expandable in order for the packed widgets contained within to operate as such.
		# At a later time, I want to make the entire GUI stretchable so the user can resize up to fullscreen. The text elements should take up the new space rather than visual.
		
		self.columnconfigure(1, weight=1)
		self.rowconfigure(1, weight=1)

		# Text Panels

		self.text_output = OutputText(self.text_frame, width=105, bg='black', foreground='white', wrap='word', relief='sunken', state='disabled')
		self.player_input = tk.Text(self.text_frame, height=2, width=105, bg='black', foreground='white', relief="sunken")
		self.text_output.pack(expand=True, fill='y')
		self.player_input.pack()


class OutputText(tk.Text):
	def __init__(self, *args, **kwargs):
		tk.Text.__init__(self, *args, **kwargs)

		# ---- Put tags here ----

		self.tag_configure('red', foreground='#ff0000')

	def display_output(self, text):
		pass

	def highlight_pattern(self, pattern, tag, start='1.0', end='end', regexp=False):

		start = self.index(start)
		end = self.index(end)

		self.mark_set('matchStart', start)
		self.mark_set('matchEnd', start)
		self.mark_set('searchLimit', end)

		count = tk.IntVar() # initiates at 0
		while True:
			index = self.search(pattern, 'matchEnd', 'searchLimit', count=count, regexp=regexp)
			if index == '': 
				break
			if count.get() == 0: 
				break
			self.mark_set('matchStart', index)
			self.mark_set('matchEnd', '%s+%sc' % (index, count.get()))
			self.tag_add(tag, 'matchStart', 'matchEnd')


class ActionCommand:
	def __init__(self, controller): # Add subject assignment
		self.subject = None
		self.verb = None
		self.target = None
		self.direct_object = None
		self.quantity = 0
		self.system_command = None
		self.controller = controller

	def not_understood(self):
		self.controller.display_text_output('I don\'t understand what you\'re trying to do.')

# ---- Functions ----

# Used to match words[] strings to name variables from a list of objects by returning a dictionary of all object names as keys, and objects references as values.
def get_names_from_object_list(object_list):
	matching_dict = {}
	for o in object_list:
		matching_dict[o.name] = o
	return matching_dict

Game().start()
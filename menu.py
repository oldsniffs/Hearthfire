import os
import shelve
import tkinter as tk
from tkinter import font as tkfont

import locations


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
		self.parent.player = locations.people.Player(game=self.parent, name='player', location=self.parent.world.map[(10,10)].map[(5,5,0)])

		print(locations.people.all_people_names)

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
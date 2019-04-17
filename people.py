import items
import random

# What they spend their time doing. Might only want 1 per person
class Vocation():
	def __init__(self):
		self.name = ''

class Person():
	def __init__(self, game, name='random', location='default'): # vocation, skills, attributes): # 

		self.game = game
		self.name = name
		self.location = location
		# if location == 'default':
		# 	self.location =  # Location class
		self.daily_calories = 0

		self.personal_xy = list(self.location.xy)
		# self.vocation = vocation # Vocation class
		# self.skills = skills # Skill dict
		# self.attributes = attributes # Attribute dict

		self.inventory = []


		# Biometrics
		self.gender = ''
		self.height = 0
		self.weight = 0 # weight formula tbd

		if name == 'random':
			self.randomize_person()
		# else:
		# 	self.readin_person()


	def talk(self):
		pass

	def generate_person(self):
		if random.randint(0,1) == 0:
			self.gender = 'female'
		else:
			self.gender = 'male'

		if self.gender == 'female':
			self.weight = 120
			self.height = 60
		else:
			self.weight = 180
			self.height = 72



	def describe(self):
		pass
		# Height, weight, etc adjectives based on biometric values. Clothes as well?

	def absorb_calories(self):
		# daily_caloric_needs formula to be designed later. 2000 default for now
		daily_caloric_needs = 2000
		calorie_balance = daily_calories - daily_caloric_needs
		weight_change = calorie_balance/9

# ---- Actions ----

	def get_item(self, item, target=None):
		# Needs to handle quantities: get stangets, get 2 stangets
		if target==None:
			self.inventory.append(item)
			self.location.items.remove(item)

		else:
			self.inventory.append(item)
			target.items.remove(item)


	def eat(self, food):
		pass

	def move(self, direction=None, exit=None):

		if exit != None:
			self.location = exit.destination

		# Directional move action will need if statement in case a new zone is entered
		elif direction != None:
			if direction == 'north':
				self.personal_xy[1] += 1
			if direction == 'east':
				self.personal_xy[0] += 1
			if direction == 'west':
				self.personal_xy[0] -= 1
			if direction == 'south':
				self.personal_xy[1] -= 1
			new_xy = tuple(self.personal_xy)
			self.location = self.location.zone.map[new_xy]


	# ---- Supporting methods ----

	def add_to_denizens(self):
		self.locations.denizens.append(self)

	def get_inventory(self): # Check through bags
		pass

	def __getstate__(self):
		state = self.__dict__.copy()
		del state['game']
		return state

	

class Player(Person):

	def __init__(self, game, name, location):
		super().__init__(game, name, location)  # Compare this to the Document_Selector object from QTracker and look up what's going on with super()
		self.inventory = []

	def show_location(self):
		current_location = 'You are at ' + self.location.zone.name + ', ' + self.location.name + '.'
		return current_location


# ---- if __name__ == '__main__' ----

if __name__ == '__main__':
	pass

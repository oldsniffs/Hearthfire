# This file includes all map related objects

import people
import os
import xml.etree.ElementTree as et

base_path = os.path.dirname(os.path.realpath(__file__))
locations_xml = os.path.join(base_path, 'data\\locations.xml')
locations_tree = et.parse(locations_xml)

world_tree = locations_tree.getroot()

class World:
	def __init__(self):
		self.map = {}
		self.load_map()

		self.populate()

	def load_map(self):
		for zone in world_tree:
			new_zone_xy = eval('(' + zone[0].text + ')')
			new_zone_type = zone[1].text
			new_zone_name = zone[2].text
			new_zone_description = zone[3].text

			self.map[new_zone_xy] = Zone(new_zone_xy, new_zone_type, new_zone_name, new_zone_description)

			# Instantiate location objects from locations.xml
			for location in zone[4]:
				new_location_xy = eval('(' + location[0].text + ')')
				new_location_zone = self.map[new_zone_xy]
				new_location_name = location[1].text
				new_location_physical_description = location[2].text
				new_location_distant_description = location[3].text

				new_location_items = []
				# This could be done as a loop
				if location[4].text == None:
					new_location_harvestables = ''
				else:
					new_location_harvestables = location[4].text.split(',')
				if location[5].text == None:
					new_location_interactables = ''
				else:
					new_location_interactables = location[5].text.split()
				if location[6].text == None:
					new_location_items = []
				else:
					for i in location[6]:
						new_item_class = ''
						new_item_dict = {}
						for e in i:
							if e.tag == 'class_type':
								new_item_class = e.text
							else:
								new_item_dict[e.tag] = e.text
								# Still need a line to e.text convert to appropriate digit
						new_location_items.append(self.item_dict_to_item(new_item_class, new_item_dict))

				self.map[new_zone_xy].map[new_location_xy] = Location(new_location_xy, new_location_zone, new_location_name, new_location_physical_description, new_location_distant_description, new_location_harvestables, new_location_interactables, new_location_items)


			# This cycles through names of locations in the zone
			# for location in zone[4]:
			# 	print(location[1].text)

	def item_dict_to_item(self, item_class, item_dict):
		new_item_dict = item_dict # This copy might not be needed


		new_item = eval('people.items.' + item_class + '()')

		for key, value in new_item_dict:
			new_item.key = value

		return new_item

	def populate(self):
		pass



class Zone:
	def __init__(self, xy, zone_type, name, description):
		self.xy = xy
		self.zone_type = zone_type
		self.name = name
		self.description = description
		self.map = {} # Key is (x,y) tuple, value is Location object


class Location:
	def __init__(self, xy, zone, name, physical_description, distant_description, harvestables, interactables, items):
		self.xy = xy
		self.zone = zone
		self.name = name
		# Denizens also have a current_location attribue so they know where they are
		self.denizens = []
		self.physical_description = physical_description
		self.distant_description = distant_description
		self.harvestables = harvestables
		self.interactables = interactables
		self.items = items
		self.buildings = []
		self.special_exits = [] # For special exits where directional movement does not apply

	def get_exits(self): 

		exits = []

		west_xy = (self.xy[0]-1, self.xy[1])
		east_xy = (self.xy[0]+1, self.xy[1])
		south_xy = (self.xy[0], self.xy[1]-1)
		north_xy = (self.xy[0], self.xy[1]+1)

		if west_xy in self.zone.map.keys():
			exits.append('west')
		if east_xy in self.zone.map.keys():
			exits.append('east')
		if south_xy in self.zone.map.keys():
			exits.append('south')
		if north_xy in self.zone.map.keys():
			exits.append('north')

		for se in self.special_exits:
			if se.detected == True:
				exits.append(se.name)

		return exits

	def describe(self, target=None):

		items = []
		for i in self.items:
			# Add item detection check
			items.append(i.name)
		capitalized_exits = []
		for e in self.get_exits():
			capitalized_exits.append(e.capitalize())

		best_description = self.zone.name + ', ' + self.name + ': ' + self.physical_description  + '\nAvailable exits: ' + ', '.join(capitalized_exits) + '.'
		return best_description

class special_exit:
	def __init__(self):
		pass

class Building:
	def __init__(self):
		self.name = ''
		self.size = 0
		self.rooms = {}

class Room: # Possible inheritance from Location
	def __init__(self):
		self.name = ''
		self.size = 0


# ---- Testing functions ----

def main_test():

	world=World()
	print(world.map[(10,10)].map[(6,5)].items)

if __name__ == '__main__':
	main_test()
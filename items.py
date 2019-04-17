import os
import xml.etree.ElementTree as et

base_path = os.path.dirname(os.path.realpath(__file__))
items_xml = os.path.join(base_path, 'data\\items.xml')
items_parse = et.parse(items_xml)
items_root = items_parse.getroot()


class Item:

	def describe(self):
		best_description = self.description
		return best_description

	# This method is commented out because items probably won't need to use Game()'s display_text_output. If they do, a way to get a reference in will be needed.
	# def __getstate__(self):
	# 	state = self.__dict__.copy()
	# 	del state['game']
	# 	return state

class Consumable(Item):
	def __init__(self):
		super().__init__()
		#consumable have calories

class Food(Consumable):
	def __init__(self):
		super().__init__()

class Fish(Food): 
	def __init__(self):
		super().__init__()

	# if cooked, that should be reflected in name, display name, or description

class Stanget(Fish):
	def __init__(self):
		super().__init__()

class Cremip(Fish):
	def __init__(self):
		super().__init__()


# Checks each subclass for readin attribute. If present, starts reading in data.
def readin_item_data(the_class, node):
	for sc in the_class.__subclasses__():
		for child in node:
			if class_to_tag(sc) == child.tag:
				if 'readin' in child.attrib:
					for attr_elem in child:
						value = attr_elem.text
						if attr_elem.text.isdigit() == False:
							value = '\''+value+'\''
						exec(sc.__name__+'.'+attr_elem.tag+' = property(lambda self: '+value+')')
						# There is a drawback: These dynamically added vars aren't mapped to the item __dict__.  A custom mapping function could add them to a list if needed.
				readin_item_data(sc, child)

def class_to_tag(a_class):
	# Fix this method to account for new plural name attribute

	class_name = a_class.__name__.lower()
	no_change_for_plural = ['fish'] 

	# Makes sure tags for classes without subs remain in singular form
	if a_class.__subclasses__() == [] or class_name in no_change_for_plural:
		return class_name

	else:
		result = class_name + 's'

	return result

def class_var_from_element():
	pass

readin_item_data(Item, items_root)

# Multiple inheritance like cookables and consumables?

# ---- if __name__ == '__main__' ----

if __name__ == '__main__':

	stanget = Stanget()
	print(stanget.__dict__)
	vars(stanget)
	# print(items_root)
	# for child in items_root:
	# 	print(child.tag, child.attrib)
	# print(class_to_tag(Item))
	# print(Item.__name__)
	# print(Item.__subclasses__())
	# print(Fish.__subclasses__())
	# fish = Fish()
	# print(fish.__dict__)

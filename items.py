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
		self.calories = 0

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
				# print(child.tag + ' matched. Attributes:', child.attrib)
				if 'readin' in child.attrib:
					# print('time to read in', sc.__name__, 'class variables')
					for gc in child:
						# print(gc.tag, gc.text)
						setattr(sc, gc.tag, gc.text)


				readin_item_data(sc, child)


def class_to_tag(a_class):

	class_name = a_class.__name__.lower()
	no_change_for_plural = ['fish']

	if a_class.__subclasses__() == []:
		return class_name

	# Since a_class has subclasses, tag needs to be plural

	if class_name in no_change_for_plural:
		return class_name
	else:
		result = class_name + 's'

	return result

def class_var_from_element():
	pass


# Multiple inheritance like cookables and consumables?

# ---- if __name__ == '__main__' ----
readin_item_data(Item, items_root)
if __name__ == '__main__':

	readin_item_data(Item, items_root)
	stanget = Stanget()
	print(stanget.name)

	# print(items_root)
	# for child in items_root:
	# 	print(child.tag, child.attrib)
	# print(class_to_tag(Item))
	# print(Item.__name__)
	# print(Item.__subclasses__())
	# print(Fish.__subclasses__())
	# fish = Fish()
	# print(fish.__dict__)

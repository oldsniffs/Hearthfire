# This file includes all classes related to acquiring and producing goods
# including equipment, interactables




# Havestables

class Body_Of_Water:
	def __init__(self):
		self.name = ''
		self.fish_proportion = {} # For replenishment. Type: generation weight
		self.fish = {} # Extant fish. Type: quantity

	def replenish(self):
		pass

class River(Body_Of_Water):
	def __init__(self):
		super().__init__()


# Interactable
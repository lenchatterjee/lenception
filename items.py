from random import randint 	# Used to generate random integers.

class Item:
	name = "Do not create raw Item objects!"

	description = "You should define a description for items in their subclass."
	dropped_description = "You should define the description for this item after it is dropped in its subclass."

	is_dropped = False	# This is going to store the status of whether this item has been picked up and dropped before.


	def __init__(self, description = ""):
		if(description):
			self.intro_description = description
		else:
			self.intro_description = self.dropped_description

	def __str__(self):
		return self.name

	def room_text(self):
		if(not self.is_dropped):					# We may want to have a different description for a weapon the first time it is encountered vs. after it has been dropped.
			return self.intro_description
		else:
			return self.dropped_description

	def check_text(self):
		return self.description

	def drop(self):
		self.is_dropped = True

	def pick_up(self):
		self.is_dropped = False

	def handle_input(self, verb, noun1, noun2, inventory):
		return [False, None, inventory]


class Acceptance_Letter(Item):
	name = "Letter of Acceptance"

	description = "A letter of Acceptance to Palazzo Purdueoso. It looks like it would open a massive door."
	dropped_description = "An acceptance letter is lying on the ground."


class Consumable(Item):
	consume_description = "You should define flavor text for consuming this item in its subclass."

	healing_value = 0		# Define this appropriately in your subclass.

	def consume(self):
		return [self.consume_description, self.healing_value]


class Pizza(Consumable):
	name = "Pepperoni and Cheese Pizza"
	healing_value = 30

	description = " Irresistable slice of Wonder ."
	dropped_description = "A piece of fresh aromatic heavenly bread from the kitchens of Len's Palazzo Purdueoso is lying on a gold plane on the floor."

class PurdueScholarship_Potion(Consumable):
	name = "Purdue Scholarship potion"
	healing_value = 75

	description = "A bottle of welcoming, glowing money potion. Take it, it's good for ya BET."
	dropped_description = "A bottle of oozing money potion is glowing on the ground."





class Weapon(Item):
	equip_description = "You should define flavor text for equipping this item in its subclass."
	attack_descriptions = ["You should define one or more attack descriptions as a list in your subclass.", "This is an example secondary attack description"]

	damage = 0		# Define this appropriately in your subclass.

	def equip_text(self):
		return self.equip_description

	def attack(self):
		return [self.attack_descriptions[randint(0, len(self.attack_descriptions))], self.damage]		# Return damage and a random attack description from your list.



class Test_tube(Weapon):
	name = "Test tube"

	description = "A rudimentary test tube for close comabat. Smashed glass damage is Lit af."
	dropped_description = "A shiny test tube lies on the ground. It looks like it would be suitable for close combat someone."
	equip_description = "You arm yourself with the test tube lmao."
	attack_descriptions = ["You swing the test tube as hard as you can. Crack!", "You wind up and crush the test tube at the poor chap's face. LeL."]

	damage = 5


class Micropippette(Weapon):
	name = "micropippette"

	description = "A small dagger-like equipment with not-so-good liquid stuff in it. It looks pretty um u know..."
	dropped_description = "A micropippette lies on the ground. It looks somewhat more dangerous than a test tube."
	equip_description = "You take the micropippette in your hand."
	attack_descriptions = ["You lunge forward with the micropippette.", "You jab wildly with the micropippette.", "You swing the micropippette at your foe."]

	damage = 15


class Rusty_Scalpel(Weapon):
	name = "rusty scalpel"

	description = "A rusty scalpel. Old but rustier the better."
	dropped_description = "There is a rusty scalpel lying on the ground."
	equip_description = "You arm yourself with the rusty scalpel."
	attack_descriptions = ["You slash with your rusty scalpel.", "Your rusty scalpel connects mightily with your enemy.", "You swing the rusty scalpel with all your might."]

	damage = 20


class Gold(Item):
	value = 0		# Define this appropriately in your subclass.

	def obtain_text(self):
		return "%i gold was added to your inventory." % value


class Gold_Coins(Gold):
	name = "gold coins"
	value = 5

	description = "A small handful of gold coins."
	dropped_description = "A shiny handful of gold coins is lying on the ground."


class Mountain_of_Gold(Gold):
	name = "mountain of gold"
	value = 100

	description = "A lustrous mountain of gold coins."
	dropped_description = "A lustrous mountain of gold coins is lying on the ground."


class Container:
	name = "Do not create raw Container objects!"

	closed_description = "You should define a closed description for containers in their subclass."
	open_description = "You should define an open description for containers in their subclass."

	closed = True

	contents = []

	def __init__(self, items = []):
		for item in items:
			if(len(self.contents) == 0):
				self.contents = [item]
			else:
				self.contents.append(item)

	def add_item(self, item):
		if(len(self.contents) == 0):
			self.contents = [item]		# Initialize the list if it is empty.
		else:
			self.contents.append(item)	# Add to the list if it is not empty.

	def remove_item(self, item):
		removal_index = -1
		for index in range(len(self.contents)):
			if(self.contents[index].name == item.name):
				removal_index = index
		if(removal_index >= 0):
			self.contents.pop(removal_index)


	def __str__(self):
		return self.name

	def room_text(self):
		if(self.closed):					# We may want to have a different description for a container if it is open or closed.
			return self.closed_description
		else:
			return self.open_description

	def check_text(self):
		if(self.closed):
			return self.closed_description
		else:
			if(len(self.contents) > 0):
				print("The %s contains:" % self.name)
				for item in self.contents:
					print('* ' + str(item).title())
			else:
				return "The %s is empty." % self.name

	def handle_input(self, verb, noun1, noun2, inventory):
		return [False, "", inventory]


class Old_Chest(Container):
	name = "old chest"
	closed_description = "A battered old chest sits against the far wall, its lid shut tightly."
	open_description = "A battered old chest sits against the far wall, its lid open wide."

	def handle_input(self, verb, noun1, noun2, inventory):
		if(noun1 == self.name):
			if(verb == 'check'):
				return [True, self.check_text(), inventory]
			if(verb == 'open'):
				if(self.closed == True):
					self.closed = False
					return [True, "You pry the lid of the battered old chest open.", inventory]
				else:
					return [True, "The old chest is already wide open.", inventory]
			if(verb == 'close'):
				if(self.closed == False):
					self.closed = True
					return [True, "You push down the lid of the old chest and it closes with a bang.", inventory]
				else:
					return [True, "The old chest is already closed.", inventory]
		elif(noun1):
			if(verb == 'take'):
				if(not self.closed):
					for index in range(len(self.contents)):
						if(self.contents[index].name.lower() == noun1):
							if(isinstance(self.contents[index], Item)):
								pickup_text = "You took the %s from the old chest and added it to your inventory." % self.contents[index].name
								inventory.append(self.contents[index])
								self.contents.pop(index)
								return [True, pickup_text, inventory]
							else:
								return [True, "The %s is too heavy to pick up." % self.contents[index].name, inventory]
			if(verb == 'check'):
				if(not self.closed):
					for index in range(len(self.contents)):
						if(self.contents[index].name.lower() == noun1):
							if(isinstance(self.contents[index], Item)):
								return [True, self.contents[index].check_text(), inventory]
		return [False, None, inventory]

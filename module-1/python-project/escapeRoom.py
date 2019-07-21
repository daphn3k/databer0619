################# CLASSES ####################

class Furniture:
	'''
	Furniture has a name and can have a key
	args: str-name, 0/key - default no key

	listKey(): returns name of key as str
	'''

	def __init__(self, name, hasKey = []):
		self.name = name
		self.hasKey = hasKey

	def listKey(self, hasKey):
		return listObject(hasKey)


class Key:
	''' 
	args: str-name, door: the door it unlocks, furniture: the furniture it's found in
	
	unlockDoor(): changes the state of door it unlocks to true
	''' 
	def __init__(self, name, door):
		self.name = name
		self.door = door
		#self.furniture = furniture

	def unlockDoor(self, door):
		door.state = True
		return door.state


class Door:
	'''
	arg: str-name, bool-False for locked True for unlocked
	'''
	def __init__(self, name, state = False):
		self.name = name
		self.state = state


class Room:
	''' Room by default has no furnitures or doors
	args: str-name, list- furniture(s), list- door(s)
	
	listFurn & listDoor: return str  with the correspoding objects of the room
	'''
	def __init__(self, name, furniture=[], door=[]):
		self.name = name
		self.furniture = furniture
		self.door = door

	def listFurn(self, furniture):
		return listObject(furniture)

	def listDoor(self, door):
		return listObject(door)

	
class GameState:
	'''
	used to save the state of the game
	'''
	def __init__(self, room, collectedKeys = []):
		super(GameState, self).__init__()
		self.room = room
		self.collectedKeys = collectedKeys

	def updateGameState(collectedKeys):
		pass


################# FUNCTIONS ####################

def listObject(obj):
	f = ''
	try:
		for el in obj:
			if len(obj) != 0:
				f += el.name + '\n'
	except TypeError:
		f += obj.name +'\n'

	return f


def action(room, updatedState):
	furns = room.listFurn(room.furniture) 
	doors = room.listDoor(room.door)

	intendedAction = input("What would you like to do?\n\nType 1 to explore the room and 2 to examine an object: ")
	
	if intendedAction == '1':
		explore(room, updatedState)
	elif intendedAction == '2':
		examine(room, furns, doors, updatedState)
	else:
		print("I didn't quite get that.")
		action(room, updatedState)
	return 


def explore(room, updatedState):
	furns = room.listFurn(room.furniture) 
	doors = room.listDoor(room.door)
	print('In this room you find:\n%s%s' %(furns, doors))
	examine(room, furns, doors, updatedState)
	
	return [furns, doors]

def examine(room, furns, doors, updatedState):
	exam = input('Which object would you like to examine?: ')
	if exam in furns or exam in doors:
	# if object to examine is furniture say if key was found
	# update game state
	# update door state  
		for f in room.furniture:
			if exam == f.name:
				if f.hasKey == []:
					print('\nThere is nothing interesting here')
					action(room, updatedState)
				else:
					print('You found %s' % (f.listKey(f.hasKey)))
					updatedState.collectedKeys.append(f.hasKey)
					f.hasKey.door.state = True
					action(room, updatedState)


		# if object to examine is door
		# if key is present, unlock door, move to new room - or report that door is locked. 
		for d in room.door:
			if exam == d.name:
				if d.state == True:
					# move Room, update game state 
					updatedState.room = moveRooms(d, updatedState.room) 
					# check if outside is reached
					if updatedState.room == outside: 
						print('You found the exit!\nYou are outside\nEnjoy the sunshine :D')
						return	
					else:
					#inform user of new room	
						print('You are in now in the %s' %(updatedState.room.name)) 
						action(updatedState.room, updatedState)
				else:
					print('this door is locked')
					action(room, updatedState)

	else:
		print('\nThe item you requested is not found in this room')
		action(room, updatedState)			
	
	return

def moveRooms(door, currentRoom):

	roomDoor = {
	'door A' : [gameRoom, bedroom1],
	'door B' : [bedroom1, bedroom2],
	'door C' : [bedroom1, livingRoom],
	'door D' : [livingRoom, outside],
	}

	# find door in dict roomDoor
	for el in roomDoor: 
		if door.name == el: 
			#check which room I'm in and update game state to other possible room
			if currentRoom == roomDoor[el][0]:	
				newRoom = roomDoor[el][1]
			else:
				newRoom = roomDoor[el][0]

	return newRoom



def startGame():

	initState = GameState(room=gameRoom)
	updatedState = GameState(room=gameRoom)
	print("Welcome to the Escape Room\nFollow the instructions on the screen\nType carefully!\n")

	print("\n\nYou wake up on a couch and find yourself in a strange house with no windows which you have never been to before. \nYou don't remember why you are here and what had happened before. \nYou feel some unknown danger is approaching and you must get out of the house, NOW!")
	print("\nYou are in the " + gameRoom.name)

	action(gameRoom, updatedState)
	return



################# CLASS INSTANCES ####################

### Doors ###
# args: str-name
# if new doors are added, remember to update the dict in moveRooms()
doorA = Door('door A')
doorB = Door('door B')
doorC = Door('door C')
doorD = Door('door D')

### Keys ###
# args: str-name, name of door it opens, object holding it
keyA = Key('key A', doorA)
keyB = Key('key B', doorB)
keyC = Key('key C', doorC)
keyD = Key('key D', doorD)

### Furnitures without keys ###
# args: str-name
couch = Furniture('couch') 
table = Furniture('dining table')

### Furnitures with keys ###
# args: str-name, key
piano = Furniture('piano', keyA)
qBed = Furniture('queen bed', keyB)
dBed = Furniture('double bed', keyC)
dresser = Furniture('dresser', keyD)

### Rooms ###
# args: str-name, list- furniture(s), list- door(s)
outside = Room('outside', [], [doorD])
gameRoom = Room('Game Room', [couch, piano], [doorA])
bedroom1 = Room('Bedroom1', [qBed], [doorA, doorB, doorC])
bedroom2 = Room('Bedroom2', [dBed, dresser], [doorB])
livingRoom = Room('Living room', [table], [doorD])

################### CALLS #############################
import time

if __name__ == '__main__':
	start_time = time.time()
	startGame()
	print('\nYou were for %f minutes in the house' % (round((time.time() - start_time)/60, 2)))

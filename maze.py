def getOppositeDirection(directionInput):
	oppositeDirectionSet = {
		North:South,
		South:North,
		East:West,
		West:East,
		None:None
	}
	return oppositeDirectionSet[directionInput]

def explorePossibleDirections():
	directionList = [North,East,South,West] #this contains all move directions
	possibleDirectionList = [] #this will contain all successful move directions
	
	for dir in directionList:
		if(move(dir) == True): #explore this position in this direction
			move(getOppositeDirection(dir)) #move back to explore position
			possibleDirectionList.append(dir) 
	return possibleDirectionList

def getPosFromDirection(x,y,dir):
	returnX = x
	returnY = y

	if(dir == North):
		returnY = returnY+1
	elif(dir == South):
		returnY = returnY-1
	elif(dir == East):
		returnX = returnX+1
	elif(dir == West):
		returnX = returnX-1
	return returnX,returnY

def getCreateItem():
	return Items.Weird_Substance

def getCreateAmount():
	return get_world_size() * num_unlocked(Unlocks.Mazes)

def canAffordCreate():
	substanceItem = getCreateItem()
	substanceAmount = getCreateAmount()
	if(substanceAmount > num_items(substanceItem)):
		return False
	return True

def createMaze():
	if(canAffordCreate() == False):
		return False

	plant(Entities.Bush)
	use_item(getCreateItem(), getCreateAmount())
	return True

def autoPathFind():
	if(createMaze() == False):
		return False

	directionsDict = {}
	lastDirectionDict = {}

	directionsDict[(get_pos_x(),get_pos_y())] = explorePossibleDirections() 
	firstDirections = directionsDict[(get_pos_x(),get_pos_y())]
	moveDirection = firstDirections[0] 
	
	while(get_entity_type() != Entities.Treasure):
		lastDirectionDict[(get_pos_x(),get_pos_y())] = moveDirection
		move(moveDirection)
		moveDirection = None

		if not( (get_pos_x(),get_pos_y()) in directionsDict ):
			directionsDict[(get_pos_x(),get_pos_y())] = explorePossibleDirections()
		possibleDirections = directionsDict[(get_pos_x(),get_pos_y())]
		
		if(len(possibleDirections) == 1): #dead end
			moveDirection = possibleDirections[0]
			removePos = getPosFromDirection(get_pos_x(),get_pos_y(),moveDirection)
			removeDirection = getOppositeDirection(moveDirection)
			
			if ( (removePos[0],removePos[1]) in directionsDict ):
				possibleDirections = directionsDict[(removePos[0],removePos[1])]
				possibleDirections.remove(removeDirection)
				directionsDict[(removePos[0],removePos[1])] = possibleDirections
		elif(len(possibleDirections) > 1): #more than 1 way possible
			for dir in possibleDirections:
				nextPos = getPosFromDirection(get_pos_x(),get_pos_y(),dir)
				if not(nextPos[0],nextPos[1]) in lastDirectionDict: 
					moveDirection = dir #next uncovered position found
					break

		if(moveDirection == None):
			break

	isSuccess = get_entity_type() == Entities.Treasure
	if(isSuccess == False):
		clear() #clear the maze
	else:
		harvest() #harvest the treasure, this removes the maze
	return isSuccess
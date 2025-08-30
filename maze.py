import misc

isInitialized = False
successDirectionSet = set() # {(x,y,direction)}
unknownDirectionSet = set() # {(x,y,direction)}
lastDirectionDict = {} # {(x,y)} = direction

def init( doOptimization ):
	preTick = get_tick_count()
	quick_print("maze.init() was called")

	global isInitialized
	global successDirectionSet # {(x,y,direction)}
	global unknownDirectionSet # {(x,y,direction)}
	global lastDirectionDict # {(x,y)} = direction
	
	isInitialized = True
	successDirectionSet = set()
	unknownDirectionSet = set()
	lastDirectionDict = {}
	
	directionList = [North,East,South,West]
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	

	addUnknownCount = 0
	for idx in range( misc.getEntityMaxCount() ):
		x = (idx % get_world_size())
		y = (idx / get_world_size()) // 1
		
		for dir in directionList:
			if( doOptimization ):
				if(	(x == minX and dir == West) or (x == maxX and dir == East) or (y == minY and dir == South) or (y == maxY and dir == North)	):
					continue	
			
			unknownDirectionSet.add((x,y,dir))
			addUnknownCount = addUnknownCount+1
	
	quick_print("DEBUG: maze.init() executed in", get_tick_count()-preTick, "ms", "with doOptimization =",doOptimization)
	return addUnknownCount
	
def saveMove(moveSuccessful, moveDirection, fromPos):
	(fromX,fromY) = fromPos
	
	#remove unknown
	if( (fromX,fromY,moveDirection) in unknownDirectionSet):
		unknownDirectionSet.remove( (fromX,fromY,moveDirection) )

	if( moveSuccessful == True ):
		#MOVE SUCCESSFUL
		
		successDirectionSet.add( (fromX,fromY,moveDirection) )

	elif( moveSuccessful == False ):
		#MOVE FAILED or REMOVE DEAD END

		if( (fromX,fromY,moveDirection) in successDirectionSet ):
			successDirectionSet.remove( (fromX,fromY,moveDirection) )

	return True #success


def canAffordCreate():
	substanceAmountRequired = get_world_size() * num_unlocked(Unlocks.Mazes)
	if(substanceAmountRequired > num_items(Items.Weird_Substance)):
		return False
	return True

def getPosFromDirection(fromPos, direction):
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	(fromX,fromY) = fromPos
	toX = fromX
	toY = fromY
	
	if( direction == North):
		toY = toY+1
		if(toY > maxY):
			toY = maxY
	elif( direction == South):
		toY = toY-1
		if(toY < minY):
			toY = minY
	elif( direction == East):
		toX = toX+1
		if(toX > maxX):
			toX = maxX
	elif( direction == West):
		toX = toX-1
		if(toX < minX):
			toX = minX
	else:
		return (None,None) #unknown direction
	return (toX,toY)

def turnDegrees(direction, degrees):
	directionList = [North,East,South,West]
	directionIdx = None
	
	for idx in range( len(directionList) ):
		if(directionList[idx] == direction):
			directionIdx = idx
			break

	if(directionIdx == None):
		return None #direction not found

	if(degrees % 90 != 0):
		return None #must be divideable by 90 without remainder

	degrees = degrees % 360 #fixes degrees, for example: -90 = 270, (360+90) = 90
	turnCount = (degrees / 90) #amount of 90 degree turns
	newIndex = (directionIdx + turnCount) % 4 #new direction index
	return directionList[newIndex] #new direction

def getUnknownDirectionsAtPos(x,y):
	directionList = [North,East,South,West]
	unknownDirectionList = []

	for dir in directionList:
		if ((x,y,dir) in unknownDirectionSet):
			unknownDirectionList.append(dir)
	return unknownDirectionList

def getSuccessDirectionsAtPos(x,y):
	directionList = [North,East,South,West]
	successDirectionList = []

	for dir in directionList:
		if ((x,y,dir) in successDirectionSet):
			successDirectionList.append(dir)
	return successDirectionList

def listToSet(inputList):
	returnSet = set()
	for stuff in inputList:
		returnSet.add(stuff)
	return returnSet
	
def createMaze():
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, get_world_size() * num_unlocked(Unlocks.Mazes))
	return True

def autoPathFind( ):
	if(createMaze() == False):
		return False

	init( False )
	
	getEntity = get_entity_type()
	fromX = get_pos_x()
	fromY = get_pos_y()

	while( getEntity != Entities.Treasure ):
		eraseDeadEnd = False
		moveDirection = None

		while(moveDirection == None):
			unknownDir = getUnknownDirectionsAtPos(fromX,fromY)
			successDir = getSuccessDirectionsAtPos(fromX,fromY)
			
			#get last direction at this position
			lastDirection = None
			if( (fromX,fromY) in lastDirectionDict ):
				lastDirection = lastDirectionDict[(fromX,fromY)]
				
			if( len(unknownDir) > 0 ):
				#unknown direction(s) found, trying
				moveDirection = unknownDir[0]
			
			elif( len(unknownDir) == 0 and len(successDir) == 1):
				moveDirection = successDir[0] #only one way to go
				eraseDeadEnd = True #dead-end, erase from data to avoid returning

			elif( len(unknownDir) == 0 and len(successDir) > 1):
				#several ways to go
				if(lastDirection == None):
					randomIdx = (random() * len(successDir)) // 1
					moveDirection = successDir[randomIdx] 
				else:
					moveDirection = turnDegrees(lastDirection, 90)
					successSet = listToSet(successDir) #get successful directions, but in a set

					while( not moveDirection in successSet ):
						moveDirection = turnDegrees(moveDirection, 90)	
						
			elif( len(unknownDir) == 0 and len(successDir) == 0 ):
				break #all paths are explored but all failed (error)

		if(moveDirection == None):
			init( False )
			quick_print("failed to find a move")
			continue

		moveSuccessful = move(moveDirection) # attempt move

		if(eraseDeadEnd == True):
			saveMove(False, moveDirection, (fromX,fromY) ) #erase this movement
			
			(nextX,nextY) = getPosFromDirection( (fromX,fromY), moveDirection )
			if( (nextX,nextY) != (fromX,fromY) ):
				oppositeDirection = turnDegrees(moveDirection, 180)
				saveMove(False, oppositeDirection, (nextX,nextY) ) #erase this opposite movement	
		else:
			saveMove(moveSuccessful, moveDirection, (fromX,fromY) ) #save this movement
			
			(nextX,nextY) = getPosFromDirection((fromX,fromY), moveDirection)
			if( (nextX,nextY) != (fromX,fromY) ):
				oppositeDirection = turnDegrees(moveDirection, 180)
				saveMove(moveSuccessful, oppositeDirection, (nextX,nextY) ) #save this opposite movement
		
		if( moveSuccessful == False ):
			continue

		#save this direction in this position for later
		lastDirectionDict[(fromX,fromY)] = moveDirection
		
		(fromX,fromY) = getPosFromDirection( (fromX,fromY), moveDirection )
#		if( (fromX,fromY) != ( get_pos_x(),get_pos_y() ) ):
#			quick_print("ERROR position is off!")

		getEntity = get_entity_type()

	harvest()
	return getEntity == Entities.Treasure
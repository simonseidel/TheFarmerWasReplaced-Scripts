import misc

isInitialized = False
overlapList = []
overlapList = []
circuitList = []
zigZagList = []
zigZagReverseList = []
usedWorldSize = None

def init( ):
	quick_print("mover.init() was called")

	if( misc.isOdd( get_world_size() ) ):
		quick_print("mover: world decreased to even size")
		set_world_size( get_world_size()-1 )
	
	global isInitialized
	global overlapList
	global circuitList
	global zigZagList
	global zigZagReverseList
	global usedWorldSize
	
	isInitialized = True
	overlapList = []
	circuitList = []
	zigZagList = []
	zigZagReverseList = []
	usedWorldSize = get_world_size()
	
	overlapList = getOverlapDirectionList()
	circuitList = getCircuitDirectionList()
	zigZagList = getZigZagDirectionList(True)
	zigZagReverseList = getZigZagDirectionList(False)

def getOverlapStartPos():
	return (0,0)

def getCircuitEndPos():
	return (0,0)

def getCircuitStartPos():
	return (1,0)

def getZigZagStartPos():
	return (0,0)

def getZigZagEndPos():
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	if( misc.isEven( get_world_size() ) ):
		return (minX,maxY)
	else:
		return (maxX,maxY)

def getOverlapDirectionList():
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	currentPos = getOverlapStartPos()
	returnList = []
	
	while( True ):
		if( currentPos[1] == minY ):
			while( currentPos[1] < maxY ):
				returnList.append(North)
				currentPos = (currentPos[0],currentPos[1]+1)

		if( currentPos[1] == maxY ):
			returnList.append(North) #next row
			returnList.append(East) #next column
			
			if( currentPos[0] == maxX ):
				currentPos = getOverlapStartPos()
				break
			else:
				currentPos = (currentPos[0]+1,minY)

	return returnList

def getCircuitDirectionList():
	if misc.isOdd( usedWorldSize ):
		return None #not possible

	returnList = []
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()

	currentPos = getCircuitStartPos()
	while( currentPos[0] < maxX ):
		returnList.append(East)
		currentPos = (currentPos[0]+1,currentPos[1])

	while( currentPos != getCircuitEndPos() ):
		if(currentPos[0] == maxX and currentPos[1] < maxY):
			#go north, then west
			returnList.append(North)
			currentPos = (currentPos[0],currentPos[1]+1)
			while(True):
				returnList.append(West)
				currentPos = (currentPos[0]-1,currentPos[1])
				if( currentPos == (minX,maxY) ):
					break
				elif( currentPos[0] == minX+1 and currentPos[1] < maxY ):
					break
	
		if(currentPos[0] == minX+1 and currentPos[1] < maxY):
			#go north, then east
			returnList.append(North)
			currentPos = (currentPos[0],currentPos[1]+1)
			while( currentPos[0] < maxX ):
				returnList.append(East)
				currentPos = (currentPos[0]+1,currentPos[1])

		if( currentPos == (minX,maxY) ):
			#go south to finish point
			while( currentPos != getCircuitEndPos() ):
				returnList.append(South)
				currentPos = (currentPos[0],currentPos[1]-1)


	returnList.append(East) #last direction connects start to end	
	return returnList

def getZigZagDirectionList(inForward):
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	currentPos = getZigZagStartPos()
	directionList = []

	while( True ):
		if(currentPos == getZigZagStartPos()):
			#go east from starting point to maxX
			while( True ):
				directionList.append(East)
				currentPos = (currentPos[0]+1,currentPos[1])
				if( currentPos[0] == maxX ):
					break

		if(currentPos[0] == maxX and currentPos[1] < maxY):
			#go north, then west
			directionList.append(North)
			currentPos = (currentPos[0],currentPos[1]+1)
			while(True):
				directionList.append(West)
				currentPos = (currentPos[0]-1,currentPos[1])
				if( currentPos[0] == minX ):
					break
	
		if(currentPos[0] == minX and currentPos[1] < maxY):
			#go north, then east
			directionList.append(North)
			currentPos = (currentPos[0],currentPos[1]+1)
			while(True):
				directionList.append(East)
				currentPos = (currentPos[0]+1,currentPos[1])
				if(currentPos[0] == maxX):
					break

		if( currentPos == (minX,maxY) or currentPos == (maxX,maxY) ):
			break #end reached

	if( inForward == True ):
		directionList.append(None) #add End, otherwise one crop gets left out when planting/harvesting at move
		return directionList

	reverseDirectionList = []

	oppositeDirectionSet = {North:South, South:North, East:West, West:East}

	while ( len(directionList) > 0 ):
		direction =	directionList.pop()
		oppositeDirection = oppositeDirectionSet[direction]
		reverseDirectionList.append(oppositeDirection)

	reverseDirectionList.append(None)
	return reverseDirectionList

def getDirectionList(startPos, targetPos):
	directionList = []

	(x,y) = startPos
	(targetX,targetY) = targetPos
	
	while(True):
		if(targetY > y ):
			y = y+1
			directionList.append(North)
		elif(targetY < y ):
			y = y-1
			directionList.append(South)
		
		if(targetX > x ):
			x = x+1
			directionList.append(East)
		elif(targetX < x ):
			x = x-1
			directionList.append(West)

		if(x == targetX and y == targetY):
			break

	return directionList

def moveToPos(targetPos):
	directionList = getDirectionList((get_pos_x(),get_pos_y()), targetPos)
	
	if( len(directionList) == 0):
		return False

	for dir in directionList:
		if( dir != None ):
			move(dir)
	return True

def moveWithDirectionList(directionList):
	if( len(directionList) == 0):
		return False

	for dir in directionList:
		if( dir != None ):
			move(dir)
	return True

def doBenchmark():
	pos = getOverlapStartPos()
	moveToPos(pos)
	
	preTick = get_tick_count()
	for dir in overlapList:
		move(dir)
	postTick = get_tick_count()
	quick_print("overlap took",postTick-preTick,"ms")
	
	pos = getCircuitStartPos()
	moveToPos(pos)
	
	preTick = get_tick_count()
	for dir in circuitList:
		move(dir)
	postTick = get_tick_count()
	quick_print("circuit took",postTick-preTick,"ms")

	pos = getZigZagStartPos()
	moveToPos(pos)
	
	preTick = get_tick_count()
	for dir in zigZagList:
		if(dir != None):
			move(dir)
	postTick = get_tick_count()
	quick_print("zigzag took",postTick-preTick,"ms")

	pos = getZigZagEndPos()
	moveToPos(pos)
	
	preTick = get_tick_count()
	for dir in zigZagReverseList:
		if(dir != None):
			move(dir)
	postTick = get_tick_count()
	quick_print("zigzag in reverse took",postTick-preTick,"ms")

if( isInitialized == False ):
	init()
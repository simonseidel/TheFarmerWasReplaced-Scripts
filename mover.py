import misc

usedWorldSize = None
overlapDict = {} #(x,y) = [directions]
circuitDict = {} #(x,y) = direction
zigZagDict = {} #(x,y,isForward) = direction

def init( ):
	quick_print("mover.init() was called")

	global usedWorldSize
	global overlapDict
	global circuitDict
	global zigZagDict

	usedWorldSize = get_world_size()
	overlapDict = {}
	circuitDict = {}
	zigZagDict = {}
	
	buildOverlapDirections()
	buildCircuitDirectionList()
	buildZigZagDirectionList()

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

def buildOverlapDirections():
	global overlapDict
	overlapDict = {}
	
	if( num_unlocked(Unlocks.Expand) == 0): 
		return False #Unlocks.Expand 0 = 1 square
	
	currentPos = getOverlapStartPos()
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	
	if(num_unlocked(Unlocks.Expand) == 1):
		#Unlocks.Expand 1 = 3 squares vertical
		overlapDict[ (0,0) ] = [North]
		overlapDict[ (0,1) ] = [North]
		overlapDict[ (0,2) ] = [North]
		return True

	while( True ):
		if( currentPos[1] == minY ):
			while( currentPos[1] < maxY ):
				overlapDict[currentPos] = [North]
				currentPos = (currentPos[0],currentPos[1]+1)

		if( currentPos[1] == maxY ):
			overlapDict[currentPos] = [North,East]			
				
			if( currentPos[0] == maxX ):
				break
			else:
				currentPos = (currentPos[0]+1,minY)
	return True

def buildCircuitDirectionList():
	global circuitDict
	circuitDict = {}

	if misc.isOdd( usedWorldSize ):
		return False #not possible

	if( num_unlocked(Unlocks.Expand) == 0): 
		return False #Unlocks.Expand 0 = 1 square

	elif(num_unlocked(Unlocks.Expand) == 1): 
		return False #Unlocks.Expand 1 = 3 squares vertical

	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()	
	currentPos = getCircuitStartPos()

	while( currentPos[0] < maxX ):
		circuitDict[currentPos] = East
		currentPos = (currentPos[0]+1,currentPos[1])
	
	while( currentPos != getCircuitEndPos() ):
		if(currentPos[0] == maxX and currentPos[1] < maxY):
			#go north, then west
			circuitDict[currentPos] = North
			currentPos = (currentPos[0],currentPos[1]+1)
			while(True):
				circuitDict[currentPos] = West
				currentPos = (currentPos[0]-1,currentPos[1])
				if( currentPos == (minX,maxY) ):
					break
				elif( currentPos[0] == minX+1 and currentPos[1] < maxY ):
					break
		
		if(currentPos[0] == minX+1 and currentPos[1] < maxY):
			#go north, then east
			circuitDict[currentPos] = North
			currentPos = (currentPos[0],currentPos[1]+1)
			while( currentPos[0] < maxX ):
				circuitDict[currentPos] = East
				currentPos = (currentPos[0]+1,currentPos[1])
	
		if( currentPos == (minX,maxY) ):
			#go south to finish point
			while( currentPos != getCircuitEndPos() ):
				circuitDict[currentPos] = South
				currentPos = (currentPos[0],currentPos[1]-1)	
	
	circuitDict[ getCircuitEndPos() ] = East #last direction connects end to start	
	return True

def buildZigZagDirectionList():
	global zigZagDict
	zigZagDict = {}
	
	if( num_unlocked(Unlocks.Expand) == 0 ): 
		return False #Unlocks.Expand 0 = 1 square

	if( num_unlocked(Unlocks.Expand) == 1):
		#Unlocks.Expand 1 = 3 squares vertical
		zigZagDict[ (0,0,True) ] = North
		zigZagDict[ (0,0,False) ] = None
		
		zigZagDict[ (0,1,True) ] = North
		zigZagDict[ (0,1,False) ] = South
		
		zigZagDict[ (0,2,True) ] = None
		zigZagDict[ (0,2,False) ] = South
		return True

	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	currentPos = getZigZagStartPos()
	
	endX,endY = getZigZagEndPos()
	zigZagDict[ (endX,endY,True) ] = None #add none direction to forward end

	startX,startY = getZigZagStartPos()
	zigZagDict[ (startX,startY,False) ] = None #add none direction to backwards end
	
	while( True ):
		if(currentPos == getZigZagStartPos()):
			#go east from starting point to maxX
			while( True ):
				zigZagDict[ (currentPos[0],currentPos[1],True) ] = East	
				currentPos = (currentPos[0]+1,currentPos[1])
				zigZagDict[ (currentPos[0],currentPos[1],False) ] = West

				if( currentPos[0] == maxX ):
					break

		if(currentPos[0] == maxX and currentPos[1] < maxY):
			#go north, then west
			zigZagDict[ (currentPos[0],currentPos[1],True) ] = North
			currentPos = (currentPos[0],currentPos[1]+1)
			zigZagDict[ (currentPos[0],currentPos[1],False) ] = South

			while(True):
				zigZagDict[ (currentPos[0],currentPos[1],True) ] = West
				currentPos = (currentPos[0]-1,currentPos[1])
				zigZagDict[ (currentPos[0],currentPos[1],False) ] = East

				if( currentPos[0] == minX ):
					break
	
		if(currentPos[0] == minX and currentPos[1] < maxY):
			#go north, then east
			zigZagDict[ (currentPos[0],currentPos[1],True) ] = North
			currentPos = (currentPos[0],currentPos[1]+1)
			zigZagDict[ (currentPos[0],currentPos[1],False) ] = South
			
			while(True):
				zigZagDict[ (currentPos[0],currentPos[1],True) ] = East
				currentPos = (currentPos[0]+1,currentPos[1])
				zigZagDict[ (currentPos[0],currentPos[1],False) ] = West

				if(currentPos[0] == maxX):
					break

		if( currentPos == getZigZagEndPos() ):
			break #end reached
	return True

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
		move(dir)
	return True
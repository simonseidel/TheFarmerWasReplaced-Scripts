import worldsize

def getCircuitEndPos():
	return (0,0)

def getCircuitStartPos():
	return (1,0)

def getZigZagStartPos():
	return (0,0)
	
def getCircuitDirectionList():
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()
	currentPos = getCircuitStartPos()
	returnList = []
	
	while( True ):
		if(currentPos == getCircuitStartPos()):
			#go east from starting point to maxX
			while( True ):
				returnList.append(East)
				currentPos = (currentPos[0]+1,currentPos[1])
				if( currentPos[0] == maxX ):
					break

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
			while(True):
				returnList.append(East)
				currentPos = (currentPos[0]+1,currentPos[1])
				if(currentPos[0] == maxX):
					break

		if( currentPos == (minX,maxY) ):
			#go south to finish point
			while( True ):
				returnList.append(South)
				currentPos = (currentPos[0],currentPos[1]-1)
				if( currentPos == getCircuitEndPos() ):
					break

		if( currentPos == getCircuitEndPos() ):
			returnList.append(East) #last direction connects start to end
			break
					
	return returnList

def getZigZagDirectionList():
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()
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
			break

	directionList.append(None)
	return directionList


def reverseZigZag(directionList):
	reverseDirectionList = []
	
	oppositeDirectionSet = {North:South, South:North, East:West, West:East}
		
	while (len(directionList) > 0):
		direction =	directionList.pop()
		if(direction in oppositeDirectionSet):
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
		if( move(dir) == False ):
			return False
	return True

def moveWithDirectionList(directionList):
	if( len(directionList) == 0):
		return False

	for dir in directionList:
		if( move(dir) == False):
			return False
	return True
	
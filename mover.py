import worldsize

def moveTowardsXY(x,y):
	direction = None
	if(get_pos_y() > y):
		direction = South
	elif(get_pos_y() < y):
		direction = North
	elif(get_pos_x() > x):
		direction = West
	elif(get_pos_x() < x):
		direction = East

	moveSuccess = False
	if(direction != None):
		moveSuccess = move(direction)
	return moveSuccess 


def getNextXY(currentX, currentY):
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()
	nextX = currentX
	nextY = currentY
	
	if(get_pos_x() == minX and get_pos_y() == maxY):
		#go to finish point
		nextX = minX
		nextY = minY
	elif(get_pos_x() == minX and get_pos_y() == minY):
		#go from finish to start point
		nextX = minX+1
		nextY = minY
	elif(get_pos_x() == minX+1 and get_pos_y() == minY):
		#go from starting point
		nextX = maxX
		nextY = get_pos_y()
	elif(get_pos_x() == maxX and get_pos_y() < maxY):
		#go up then left
		nextY = get_pos_y()+1
		if(nextY == maxY):
			nextX = minX
		else:
			nextX = minX + 1
	elif(get_pos_x() == minX+1 and get_pos_y() < maxY):
		#go up then right
		nextX = maxX
		nextY = get_pos_y()+1
	return nextX,nextY
	
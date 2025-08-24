import worldsize
import mover

def getCostItem():
	costDict = get_cost(Entities.Apple)
	for item in costDict:
		return item
	return None		

def getCostAmount():
	costDict = get_cost(Entities.Apple)
	for item in costDict:
		return costDict[item]
	return None

def canAffordGame():
	costItem = getCostItem()
	costAmount = getCostAmount() * worldsize.getEntityMaxCount()
	if( costAmount > num_items(costItem) ):
		return False
	return True

def runGame(runState = 0, applePos = None):
	if(runState < 0 or runState > 1):
		return False

	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()

	movePos = minX+1,minY #go to starting point
	while(mover.moveTowardsXY(movePos[0],movePos[1])):
		pass

	gameRunning = True
	while gameRunning == True:
		if(runState == 0): #tilling State
			if(get_ground_type() != Grounds.Soil):
				till()
		elif(runState == 1):
			if(applePos == None):
				gameRunning = False
				break
			
			if(applePos != None and get_pos_x() == applePos[0] and get_pos_y() == applePos[1]):
				applePos = measure()

		if(get_pos_x() == minX and get_pos_y() == minY): #end point reached
			if(runState == 0):
				change_hat(Hats.Dinosaur_Hat) #apply "snake hat"
				if(applePos == None):
					applePos = measure()
				return runGame(runState+1, applePos) #tilling done, start game
			elif(runState == 1):
				return runGame(runState, applePos) #run again, not finished
		else:
			moveFailCount = 0
			while(mover.moveTowardsXY(movePos[0],movePos[1]) == False):
				moveFailCount = moveFailCount+1 #move failed +1
					
				if(moveFailCount >= 2):
					gameRunning = False
					break

				movePos = mover.getNextXY(movePos[0],movePos[1]) #get next pos target
	
	if(runState == 1 and gameRunning == False):
		change_hat(Hats.Straw_Hat) #remove "snake hat"
	
	return True	
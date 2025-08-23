import entitydata
import worldsize
import mover
import plant
import fertilizer

def autoSwap(minX, maxX, minY, maxY):
	x = get_pos_x()
	y = get_pos_y()
	swapCount = 0
	
	if(x > minX and measure(West) > measure() and swap(West)):
		swapCount = swapCount + 1	
	if(x < maxX and measure(East) < measure() and swap(East)):
		swapCount = swapCount + 1
	if(y > minY and measure(South) > measure() and swap(South)):
		swapCount = swapCount + 1
	if(y < maxY and measure(North) < measure() and swap(North)):
		swapCount = swapCount + 1
	return swapCount

def autoFarm(runState = 0):
	if(runState < 0 or runState > 2):
		return False

	if(runState == 0):
		entitydata.init()

	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()

	movePos = minX+1,minY #go to starting point
	while(mover.moveTowardsXY(movePos[0],movePos[1])):
		pass

	while True:
		if(runState == 0):
			if(plant.putHere(Entities.Cactus) == False):
				return False
		elif(runState == 1):
			totalCount = 0
			while(True):
				thisCount = autoSwap(minX, maxX, minY, maxY)
				if(thisCount == 0):
					break
				totalCount = totalCount + thisCount

			if(totalCount > 0):
				entitydata.swapDict[(get_pos_x(),get_pos_y())] = totalCount
			elif(totalCount == 0):
				if( (get_pos_x(),get_pos_y()) in entitydata.swapDict):
					entitydata.swapDict.pop( (get_pos_x(),get_pos_y()) )			
		elif(runState == 2):
			fertilizer.undoHere()

		if(get_pos_x() == minX and get_pos_y() == minY): #end point reached
			if(runState == 0):
				return autoFarm(runState+1)
			elif(runState == 1):
				if(entitydata.countSwap() > 0):
					return autoFarm(runState) 
				return autoFarm(runState+1)
			elif(runState == 2):
				if(can_harvest()):
					plant.harvestHere() 
				return True
		else:
			moveFailCount = 0
			while(mover.moveTowardsXY(movePos[0],movePos[1]) == False):
				moveFailCount = moveFailCount+1 #move failed +1
				if(moveFailCount >= 2):
					return False
				movePos = mover.getNextXY(movePos[0],movePos[1]) #get next pos target

	return True
	
import entitydata
import worldsize
import mover
import plant
import fertilizer

def autoFarm(runState = 0):
	if(runState < 0 or runState > 2):
		return False

	biggestSize = None
	if(runState == 0):
		entitydata.init()

	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()

	movePos = minX+1,minY #go to starting point
	while(mover.moveTowardsXY(movePos[0],movePos[1])):
		pass

	while True:
		if(runState == 0):
			if(plant.putHere(Entities.Sunflower) == False):
				return False
			entitydata.sizeDict[(get_pos_x(),get_pos_y())] = measure()
		elif(runState == 1):
			fertilizer.undoHere()
		elif(runState == 2):
			if(biggestSize == None):
				biggestSize = entitydata.getBiggest()

			if( (get_pos_x(),get_pos_y()) in entitydata.sizeDict):
				if(can_harvest() and measure() >= biggestSize):
					plant.harvestHere()

					if(entitydata.countSize() == 0):
						return True

		if(get_pos_x() == minX and get_pos_y() == minY): #end point reached
			if(runState == 0):
				return autoFarm(runState+1) 
			elif(runState == 1):
				return autoFarm(runState+1)
			elif(runState == 2):
				return autoFarm(runState)
		else:
			moveFailCount = 0
			while(mover.moveTowardsXY(movePos[0],movePos[1]) == False):
				moveFailCount = moveFailCount+1 #move failed +1
				if(moveFailCount >= 2):
					return False
				movePos = mover.getNextXY(movePos[0],movePos[1]) #get next pos target

	return True #finished
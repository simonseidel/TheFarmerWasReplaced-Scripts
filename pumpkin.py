import entitydata
import worldsize
import mover
import plant

def autoFarm(runState = 0):
	if(runState < 0 or runState > 1):
		return False

	if(runState == 0):
		entitydata.init()

	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()

	movePos = minX+1,minY #go to starting point
	while(mover.moveTowardsXY(movePos[0],movePos[1])):
		pass

	while True:
		if(runState == 0):
			if(plant.putHere(Entities.Pumpkin) == False):
				return False
		elif(runState == 1):
			if(get_entity_type() == None):
				entitydata.initEntity( (get_pos_x(),get_pos_y()) )
				return autoFarm(0) #plant again
			
			fertilizer.undoHere()
		if(get_pos_x() == minX and get_pos_y() == minY): #end point reached
			if(runState == 0):
				return autoFarm(runState+1)
			elif(runState == 1):
				if(entitydata.countType() == worldsize.getEntityMaxCount()):
					if(can_harvest()):
						plant.harvestHere()
					return True
				else:
					return autoFarm(runState)
		else:
			moveFailCount = 0
			while(mover.moveTowardsXY(movePos[0],movePos[1]) == False):
				moveFailCount = moveFailCount+1 #move failed +1
				if(moveFailCount >= 2):
					return False
				movePos = mover.getNextXY(movePos[0],movePos[1]) #get next pos target
	
	return True #finished
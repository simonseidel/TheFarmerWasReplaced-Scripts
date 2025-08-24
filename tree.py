import worldsize
import mover
import entitydata
import helper
import plant
import fertilizer

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
		if(runState == 0): #plant tree
			if( helper.isEven(get_pos_x()) and helper.isEven(get_pos_y()) ):
				if(plant.putHere(Entities.Tree, True) == False):
					return False #error
				
				fertilizer.undoHere()

				myCompanion = get_companion()
				if( myCompanion != None):
					(myCompanionEntity, (myCompanionX,myCompanionY)) = myCompanion
					entitydata.companionDict[(myCompanionX,myCompanionY)] = (myCompanionEntity,False)

		elif(runState == 1): #plant companions
			if( helper.isEven(get_pos_x()) and helper.isEven(get_pos_y()) ):
				#remove this companion because it can not be planted here
				if( (get_pos_x(),get_pos_y()) in entitydata.companionDict):			
					entitydata.companionDict.pop( (get_pos_x(),get_pos_y()) )
			else:
				#companion plants are allowed here
				companionCreated = False
				if( (get_pos_x(),get_pos_y()) in entitydata.companionDict):
					(companionEntity,companionIsPlanted) = entitydata.companionDict[ (get_pos_x(),get_pos_y()) ]

					if(not companionIsPlanted and plant.canAffordToPlant(companionEntity, 1)):
						companionCreated = plant.putHere(companionEntity, False)

					if(companionCreated == False):
						#remove this companion because it could not be planted
						entitydata.companionDict.pop( (get_pos_x(),get_pos_y()) )
					else:
						#update companion dictionary to isCreated = True
						entitydata.companionDict[ (get_pos_x(),get_pos_y()) ] = (companionEntity,companionCreated)

				if(companionCreated == False): 
					#no companion here, plant a bush instead
					if(plant.putHere(Entities.Bush, False) == False):
						return False #error
		elif(runState == 2): #harvest
			if( can_harvest() and (get_pos_x(),get_pos_y()) in entitydata.typeDict):
				plant.harvestHere()
				
				if(entitydata.countType() == 0):
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

	return True	
import worldsize
import entitydata
import mover
import fertilizer
import helper

def getItemEntities(item):
	itemDict = {
		Items.Hay:[Entities.Grass],
		Items.Wood:[Entities.Tree,Entities.Bush],
		Items.Carrot:[Entities.Carrot],
		Items.Pumpkin:[Entities.Pumpkin],
		Items.Cactus:[Entities.Cactus],
		Items.Bone:[Entities.Apple,Entities.Dinosaur],
		Items.Weird_Substance:[None],
		Items.Gold:[Entities.Bush,Entities.Hedge,Entities.Treasure],
		Items.Water:[None],
		Items.Fertilizer:[None],
		Items.Power:[Entities.Sunflower]
		#Items.Piggy:[None]		
	}
	entityList = [None]
	if(item in itemDict):
		entityList = itemDict[item]
	return entityList

def getItemEntity(item):
	entityList = getItemEntities(item)
	randomIdx = random() * len(entityList) // 1
	return entityList[randomIdx]


def canAffordToPlant(plantEntity, entityAmount):
	entityCostDict = {
		Entities.Apple:{Items.Pumpkin:16},
		Entities.Cactus:{Items.Pumpkin:14},
		Entities.Carrot:{Items.Hay:12,Items.Wood:12},
		Entities.Pumpkin:{Items.Carrot:10},
		Entities.Sunflower:{Items.Carrot:1},
	}
	
	if not plantEntity in entityCostDict:
		return True #free plant

	entityCost = entityCostDict[plantEntity]
	for item in entityCost:
		cost = entityCost[item] * entityAmount
		if( cost > num_items(item) ):
			return False #costs, and can not afford
	return True #costs, but can afford

def putHere(entity, fertilize = False):
	if not(get_ground_type() == Grounds.Soil):
		till()

	if(not can_harvest() and get_water() < 1 and num_items(Items.Water) > 0):
		use_item(Items.Water)

	if not(get_entity_type() == None):
		return False
	
	if(plant(entity) == False):
		return False

	entitydata.typeDict[(get_pos_x(),get_pos_y())] = entity		
	if( fertilize == True ):
		fertilizer.putHere()
	return True
	
def harvestHere():
	if(harvest() == False):
		return False

	entitydata.initEntity( (get_pos_x(),get_pos_y()) )
	return True

def autoTill(setGroundtype):
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()

	movePos = minX+1,minY #go to starting point
	while(mover.moveTowardsXY(movePos[0],movePos[1])):
		pass

	while True:
		if(get_ground_type() != setGroundtype):
			till()
		else:
			if(get_entity_type() != None):
				harvest()

		if(get_pos_x() == minX and get_pos_y() == minY): #end point reached
			break
		else:
			moveFailCount = 0
			while(mover.moveTowardsXY(movePos[0],movePos[1]) == False):
				moveFailCount = moveFailCount+1 #move failed +1
				if(moveFailCount >= 2):
					return False
				movePos = mover.getNextXY(movePos[0],movePos[1]) #get next pos target
	return True	


def autoFarmEntity(entity, runState = 0):
	if(runState < 0 or runState > 3):
		return False

	if(runState == 0):
		entitydata.init()
	
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()

	movePos = minX+1,minY #go to starting point
	while(mover.moveTowardsXY(movePos[0],movePos[1])):
		pass

	skippedCount = 0
	
	while True:
		if(runState == 0): #plant main entity
			if(putHere(entity, False) == False):
				return False #error
				
			myCompanion = get_companion()
			if( myCompanion != None):
				(myCompanionEntity, (myCompanionX,myCompanionY)) = myCompanion
				entitydata.companionDict[(myCompanionX,myCompanionY)] = (myCompanionEntity,False)
		elif(runState == 1): #plant companions
			if( (get_pos_x(),get_pos_y()) in entitydata.companionDict):
				#companion here			
				(companionEntity,companionIsPlanted) = entitydata.companionDict[ (get_pos_x(),get_pos_y()) ]
				if(companionIsPlanted == False):
					if(canAffordToPlant(companionEntity, 1)):
						if(can_harvest()):
							harvestHere()
							if(putHere(companionEntity, False) == False):
								return False #error
							entitydata.companionDict[ (get_pos_x(),get_pos_y()) ] = (companionEntity,True)
						else:
							skippedCount = skippedCount+1				
					else:
						#remove this companion because it could not be planted
						entitydata.companionDict.pop( (get_pos_x(),get_pos_y()) )
				else:
					pass #already planted this companion
		elif(runState == 2): #harvest main
			if( (get_pos_x(),get_pos_y()) in entitydata.typeDict and not (get_pos_x(),get_pos_y()) in entitydata.companionDict):
				if( can_harvest() ):
					harvestHere()
				else:
					skippedCount = skippedCount+1
		elif(runState == 3): #harvest all the rest
			if( can_harvest() and (get_pos_x(),get_pos_y()) in entitydata.typeDict):
				harvestHere()
				if( entitydata.countType() == 0):
					return True
		if(get_pos_x() == minX and get_pos_y() == minY): #end point reached
			if(runState == 0):
				return autoFarmEntity(entity, runState+1)
			elif(runState == 1):
				if( skippedCount > 0 ):
					return autoFarmEntity(entity, runState)
				else:
					return autoFarmEntity(entity, runState+1)
			elif(runState == 2):
				if( skippedCount > 0 ):
					return autoFarmEntity(entity, runState)
				else:
					return autoFarmEntity(entity, runState+1)
			elif(runState == 3):
				return autoFarmEntity(entity, runState)
		else:
			moveFailCount = 0
			while(mover.moveTowardsXY(movePos[0],movePos[1]) == False):
				moveFailCount = moveFailCount+1 #move failed +1
				if(moveFailCount >= 2):
					return False
				movePos = mover.getNextXY(movePos[0],movePos[1]) #get next pos target

	return True	
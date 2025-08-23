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
		#Items.Bone:[None],
		#Items.Weird_Substance:[None],
		#Items.Gold:[None],
		#Items.Water:[None],
		#Items.Fertilizer:[None],
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

def getMinInventoryItem():
	minItem = None
	for item in Items:
		entity = getItemEntity(item)
		if(entity == None):
			continue #skip, this is not a plant
	
		if(entity == Entities.Sunflower):
			continue #skip, power will always be lower than other items
			
		if not( canAffordToPlant(entity, worldsize.getEntityMaxCount()) ):
			continue #skip, cannot afford to plant this
	
		if(minItem == None or num_items(item) < num_items( minItem )):
			minItem = item
	return minItem


def canAffordToPlant(plantEntity, entityAmount):
	entityCostDict = {
		Entities.Apple:{Items.Pumpkin:16},
		Entities.Cactus:{Items.Pumpkin:14},
		Entities.Carrot:{Items.Hay:12,Items.Wood:12},
		Entities.Pumpkin:{Items.Carrot:10},
		Entities.Sunflower:{Items.Carrot:1},
	}
	
	if not(plantEntity in entityCostDict):
		return True #free plant

	entityCost = entityCostDict[plantEntity]
	for item in entityCost:
		cost = entityCost[item] * entityAmount
		if( cost > num_items(item) ):
			return False #costs, and can not afford
	return True #costs, but can afford

def putHere(entity):
	if not(get_ground_type() == Grounds.Soil):
		till()

	if(not can_harvest() and get_water() < 1 and num_items(Items.Water) > 0):
		use_item(Items.Water)

	if not(get_entity_type() == entity):
		if(plant(entity) == False):
			return False

	entitydata.typeDict[(get_pos_x(),get_pos_y())] = entity	
	fertilizer.putHere()
	return True
	
def harvestHere():
	if(harvest() == False):
		return False

	entitydata.initEntity( (get_pos_x(),get_pos_y()) )
	return True
	
def autoFarmEntity(entity, runState = 0):
	if(runState < 0 or runState > 4):
		return False

	if(runState == 0):
		entitydata.init()
	
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()

	movePos = minX+1,minY #go to starting point
	while(mover.moveTowardsXY(movePos[0],movePos[1])):
		pass

	while True:
		if(runState == 0): #plant main entity
			if( helper.isEven(get_pos_x()) and helper.isEven(get_pos_y()) ):
				if(putHere(entity) == False):
					return False #error
				
				fertilizer.undoHere()

				myCompanion = get_companion()
				if( myCompanion != None):
					(myCompanionEntity, (myCompanionX,myCompanionY)) = myCompanion
					entitydata.companionDict[(myCompanionX,myCompanionY)] = myCompanionEntity
			else:
				pass
		elif(runState == 1): #plant companions
			if( helper.isEven(get_pos_x()) and helper.isEven(get_pos_y()) ):
				if( (get_pos_x(),get_pos_y()) in entitydata.companionDict):		
					#remove this companion because it can not be planted here
					entitydata.companionDict.pop( (get_pos_x(),get_pos_y()) )
			else:
				companionSuccessful = False
				#companion plants are allowed here
				if( (get_pos_x(),get_pos_y()) in entitydata.companionDict):
					#companion here			
					companionEntity = entitydata.companionDict[ (get_pos_x(),get_pos_y()) ]

					if(canAffordToPlant(companionEntity, 1)):
						companionSuccessful = putHere(companionEntity)

					if(companionSuccessful == False):
						#remove this companion because it could not be planted
						entitydata.companionDict.pop( (get_pos_x(),get_pos_y()) )

				if(companionSuccessful == False): 
					#no companion here, plant something else
					plantEntity = entity
					if(entity == Entities.Tree):
						#trees must grow sparse, plant a bush
						plantEntity = Entities.Bush 

					if(putHere(plantEntity) == False):
						return False #error
		elif(runState == 2):
			fertilizer.undoHere()
		elif(runState == 3): #harvest main
			if( helper.isEven(get_pos_x()) and helper.isEven(get_pos_y()) ):
				if( (get_pos_x(),get_pos_y()) in entitydata.typeDict):
					if(can_harvest()):
						harvestHere()
			else:
				pass
		elif(runState == 4): #harvest all the rest
			if( (get_pos_x(),get_pos_y()) in entitydata.typeDict):
				if(can_harvest()):
					harvestHere()
				
				if(entitydata.countType() == 0):
					return True
		if(get_pos_x() == minX and get_pos_y() == minY): #end point reached
			if(runState < 4):
				return autoFarmEntity(entity, runState+1)
			elif(runState == 4):
				return autoFarmEntity(entity, runState)
		else:
			moveFailCount = 0
			while(mover.moveTowardsXY(movePos[0],movePos[1]) == False):
				moveFailCount = moveFailCount+1 #move failed +1
				if(moveFailCount >= 2):
					return False
				movePos = mover.getNextXY(movePos[0],movePos[1]) #get next pos target

	return True	
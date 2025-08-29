import worldsize
import mover
import misc

isPlantedSet = set() #a set containing only planted entities
fertilizedSet = set() #a set containing only fertilized entitites
infectedSet = set() #a set containing only infected entities

def init():
	isPlantedSet = set() 
	fertilizedSet = set() 
	infectedSet = set() 

def initEntity(pos):
	if pos in isPlantedSet:
		isPlantedSet.remove(pos)
	if pos in infectedSet:
		infectedSet.remove(pos)
	if pos in fertilizedSet:
		fertilizedSet.remove(pos)

def canAffordFertilize( fertilizerInventory ):
	return fertilizerInventory >= worldsize.getEntityMaxCount()

def canAffordUnfertilize( weirdsubstanceInventory ):
	return weirdsubstanceInventory >= worldsize.getEntityMaxCount()

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

def getIrrigateLevel( waterItemCount ):
	waterRequired = worldsize.getEntityMaxCount()

	if(   waterItemCount >= waterRequired*4 ):
		irrigateLevel = 4*0.25
	elif( waterItemCount >= waterRequired*3 ):
		irrigateLevel = 3*0.25
	elif( waterItemCount >= waterRequired*2):
		irrigateLevel = 2*0.25
	elif( waterItemCount >= waterRequired*1):
		irrigateLevel = 1*0.25
	else:
		irrigateLevel = 0
	return irrigateLevel

def irrigateHere( waterLevel ):
	if(waterLevel < 0):
		waterLevel = 0
	elif(waterLevel > 1):
		waterLevel = 1

	while(get_water() < waterLevel and num_items(Items.Water) > 0):
		use_item(Items.Water)

def plantHere(entity):
	if not(get_ground_type() == Grounds.Soil):
		till()
	
	if not(get_entity_type() == None):
		return False
	
	if(plant(entity) == False):
		return False

	isPlantedSet.add( (get_pos_x(),get_pos_y()) )
	return True


def harvestHere():
	if(harvest() == False):
		return False

	if( get_entity_type() == Entities.Grass ):
		till()

	initEntity( (get_pos_x(),get_pos_y()) )
	return True

def autoTill(setGroundType):
	mover.moveToPos( mover.getCircuitStartPos() )
	
	directionList = mover.getCircuitDirectionList()
	
	for dir in directionList:
		if(get_ground_type() != setGroundType):
			till()
		else:
			if(get_entity_type() != None):
				harvest()
	
		move(dir)
	return True #error



def getAffectedSet(x,y):
	affectedSet = set()
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()
	
	pos = (x,y) #here
	if( pos in isPlantedSet ):
		affectedSet.add(pos)

	if(x < maxX):
		pos = (x+1,y) #east
		if( pos in isPlantedSet ):
			affectedSet.add(pos) 
	if(x > minX):
		pos = (x-1,y) #west
		if( pos in isPlantedSet ):
			affectedSet.add(pos) 
	if(y < maxY):
		pos = (x,y+1) #north
		if( pos in isPlantedSet ):
			affectedSet.add(pos) 
	if(y > minY):
		pos = (x,y-1) #south
		if( pos in isPlantedSet ):
			affectedSet.add(pos) 
	return affectedSet

def getInfectedInSet(inputSet):
	returnSet = set()
	for pos in inputSet:
		if( pos in infectedSet):
			returnSet.add(pos)
	return returnSet

def fertilizeHere():
	if( get_entity_type() == Entities.Bush):
		return False #don't fertilize - bushes can't be unfertilized

	if( ( get_pos_x(),get_pos_y() ) in fertilizedSet ):
		return False #already fertilized

	if(num_items(Items.Fertilizer) > 0):
		use_item(Items.Fertilizer)
		infectedSet.add( (get_pos_x(),get_pos_y()) )
		fertilizedSet.add( (get_pos_x(),get_pos_y()) )
	return True

def unFertilizeHere():
	if(get_entity_type() == Entities.Bush):
		return False #this would create a maze

	affectedSet = getAffectedSet(get_pos_x(),get_pos_y())
	if(len(affectedSet) == 0):
		return False

	infectedInSet = getInfectedInSet(affectedSet)
	nonInfectedCount = len(affectedSet) - len(infectedInSet)
	if(nonInfectedCount > 0):
		return False #non-infected plants would be affected
	
	if(num_items(Items.Weird_Substance) == 0):
		return False
	
	use_item(Items.Weird_Substance)
	for pos in affectedSet:
		if( pos in infectedInSet ):
			infectedSet.remove(pos)
		else:
			infectedSet.add(pos)	

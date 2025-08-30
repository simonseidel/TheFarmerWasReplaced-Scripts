import mover
import misc

isInitialized = False #has init been run?
isPlantedSet = set() #plant or empty
fertilizedSet = set() #a set containing only fertilized entitites
infectedSet = set() #a set containing only infected entities
entityTypeDict = {} #dictionary containing all of the planted entities
groundTypeDict = {} #dictionary containing all of the ground types
waterLevelDict = {} #dictionary containing latest water level

def init():
	quick_print("planter.init() was called")

	global isInitialized
	global isPlantedSet
	global fertilizedSet
	global infectedSet
	global entityTypeDict 
	global groundTypeDict
	global waterLevelDict
	
	isInitialized = True
	isPlantedSet = set()
	fertilizedSet = set() 
	infectedSet = set() 
	entityTypeDict = {}
	groundTypeDict = {}
	waterLevelDict = {}

	clear()

	for idx in range( misc.getEntityMaxCount() ):
		x = (idx % get_world_size())
		y = (idx / get_world_size()) // 1

		groundTypeDict[(x,y)] = Grounds.Grassland
		entityTypeDict[(x,y)] = Entities.Grass
		isPlantedSet.add((x,y))

def canAffordFertilize( fertilizerInventory ):
	return fertilizerInventory >= misc.getEntityMaxCount()

def canAffordUnfertilize( weirdsubstanceInventory ):
	return weirdsubstanceInventory >= misc.getEntityMaxCount()

def canAffordToPlant(plantEntity, entityAmount):
	entityCost = get_cost(plantEntity)
	if( entityCost == None or len(entityCost) == 0 ):
		return True #not plantable or free
	
	for item in entityCost:	
		cost = entityCost[item] * entityAmount
		if( cost > num_items(item) ):
			return False #costs, and can not afford
	return True #costs, but can afford

def getIrrigateLevel( waterItemCount ):
	waterRequired = misc.getEntityMaxCount()

	if( waterItemCount >= waterRequired*4 ):
		irrigateLevel = 1
	elif( waterItemCount >= waterRequired*3 ):
		irrigateLevel = 0.75
	elif( waterItemCount >= waterRequired*2):
		irrigateLevel = 0.5
	elif( waterItemCount >= waterRequired*1):
		irrigateLevel = 0.25
	else:
		irrigateLevel = 0
	return irrigateLevel

def irrigateHere( waterLevel, updateData ):
	if(waterLevel < 0):
		waterLevel = 0
	elif(waterLevel > 1):
		waterLevel = 1

	while(get_water() < waterLevel and num_items(Items.Water) > 0):
		use_item(Items.Water)

	if( updateData ):
		waterLevelDict[ (get_pos_x(),get_pos_y()) ] = get_water()

def plantHere(entity):
	tillHere(Grounds.Soil)

	if not(get_entity_type() == None):
		return False

	if(entity == Entities.Tree):
		thisSet = getSurroundingSet( get_pos_x(),get_pos_y() )
		for pos in thisSet:
			if not pos in entityTypeDict:
				continue

			thisEntity = entityTypeDict[pos]
			if(thisEntity == Entities.Tree):
				return False #trees must be planted sparse

	if(plant(entity) == False):
		return False

	pos = (get_pos_x(),get_pos_y())
	isPlantedSet.add(pos)
	entityTypeDict[pos] = entity
	
	return True

def harvestHere():
	if(harvest() == False):
		return False

	thisGroundType = get_ground_type()
	pos = ( get_pos_x(),get_pos_y() )

	if( thisGroundType != Grounds.Grassland):
		entityTypeDict[pos] = None
		if pos in isPlantedSet:
			isPlantedSet.remove(pos)

	if pos in infectedSet:
		infectedSet.remove(pos)

	if pos in fertilizedSet:
		fertilizedSet.remove(pos)
	
	return True

def tillHere(targetGroundType):
	thisGroundType = get_ground_type()
	thisEntity = get_entity_type()
	shouldTill = thisGroundType != targetGroundType

	if( shouldTill ):
		till()

	if( shouldTill == False and thisGroundType != Grounds.Grassland and thisEntity != None ):
		harvest()

	if( shouldTill ):
		pos = ( get_pos_x(),get_pos_y() )
		groundTypeDict[pos] = targetGroundType

		if( targetGroundType == Grounds.Grassland ):
			entityTypeDict[pos] = Entities.Grass
		else:
			entityTypeDict[pos] = None
			if pos in isPlantedSet:
				isPlantedSet.remove(pos)

	return shouldTill
	
def autoTill(targetGroundType):
	mover.moveToPos( mover.getZigZagStartPos() )
	for dir in mover.zigZagList:
		tillHere(targetGroundType)
		if(dir != None):
			move(dir)
	return True

def getSurroundingSet(x,y):
	affectedSet = set()
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	
	pos = (x,y) #here
	if pos in isPlantedSet:
		affectedSet.add(pos)

	if(x < maxX):
		pos = (x+1,y) #east
		if pos in isPlantedSet:
			affectedSet.add(pos)
	if(x > minX):
		pos = (x-1,y) #west
		if pos in isPlantedSet:
			affectedSet.add(pos)
	if(y < maxY):
		pos = (x,y+1) #north
		if pos in isPlantedSet:
			affectedSet.add(pos)
	if(y > minY):
		pos = (x,y-1) #south
		if pos in isPlantedSet:
			affectedSet.add(pos)
	return affectedSet

def getInfectedInSet(inputSet):
	returnSet = set()
	for pos in inputSet:
		if( pos in infectedSet):
			returnSet.add(pos)
	return returnSet

def fertilizeHere( ):
	if( get_entity_type() == Entities.Bush):
		return False #don't fertilize - bushes can't be unfertilized

	if( ( get_pos_x(),get_pos_y() ) in fertilizedSet ):
		return False #already fertilized

	if(num_items(Items.Fertilizer) > 0):
		use_item(Items.Fertilizer)
		infectedSet.add( (get_pos_x(),get_pos_y()) )
		fertilizedSet.add( (get_pos_x(),get_pos_y()) )
	return True

def unFertilizeHere( ):
	if(get_entity_type() == Entities.Bush):
		return False #this would create a maze

	affectedSet = getSurroundingSet(get_pos_x(),get_pos_y())
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

if(isInitialized == False):
	init()
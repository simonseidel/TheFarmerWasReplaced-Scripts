def isOdd(n):
	return n % 2 != 0

def isEven(n):
	return n % 2 == 0

def waitForSeconds(seconds):
	startTime = get_time()
	finishTime = startTime + seconds
	while( get_time() < finishTime ):
		pass
	return True

def getEntityMaxCount():
	expandUnlocked = num_unlocked(Unlocks.Expand)
	if(expandUnlocked == 0):
		return 1
	elif(expandUnlocked == 1):
		return get_world_size()
	else:
		return (get_world_size() * get_world_size())

def getWorldMinMaxXXYY():
	#return tuple (minx,maxx,miny,maxy)
	minX = 0
	maxX = get_world_size()-1
	minY = 0
	maxY = get_world_size()-1
	return minX,maxX,minY,maxY

def getItemEntity(item):
	itemDict = {
		Items.Hay:Entities.Grass,
		Items.Wood:Entities.Tree,
		Items.Carrot:Entities.Carrot,
		Items.Pumpkin:Entities.Pumpkin,
		Items.Cactus:Entities.Cactus,
		Items.Bone:Entities.Apple,
		Items.Gold:Entities.Bush,
		Items.Power:Entities.Sunflower
	}

	if not item in itemDict:
		return None

	entity = itemDict[item]
	if( entity == Entities.Tree and num_unlocked(Unlocks.Trees) == 0 ):
		entity = Entities.Bush

	return entity

def listToSet(inputList):
	returnSet = set()
	for stuff in inputList:
		returnSet.add(stuff)
	return returnSet
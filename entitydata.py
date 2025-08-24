typeDict = {} #location and entity type
companionDict = {} #companion location and (entityType,isPlanted)
sizeDict = {} #location and size
swapDict = {} #amount of swaps performed
infectedSet = set() #a set containing infected entities

def init():
	typeDict = {}
	companionDict = {} 
	sizeDict = {} 
	swapDict = {} 
	infectedSet = set()

def initEntity(pos):
	if pos in typeDict:
		typeDict.pop(pos)
	if pos in companionDict:
		companionDict.pop(pos)
	if pos in sizeDict:
		sizeDict.pop(pos)
	if pos in swapDict:
		swapDict.pop(pos)
	if pos in infectedSet:
		infectedSet.remove(pos)

def getBiggest():
	biggestSize = None
	for pos in sizeDict:
		thisSize = sizeDict[pos]
		if(biggestSize == None or thisSize > biggestSize):
			biggestSize = thisSize
	return biggestSize

def countCompanion():
	return len(companionDict)
	
def countSize():
	return len(sizeDict)

def countSwap():
	return len(swapDict)

def countType():
	return len(typeDict)

import plant
import maze
import snake
import worldsize
import sunflower
import pumpkin
import cactus

def attemptAutoUnlock():
	unlockCount = 0
	for u in Unlocks:
		costDict = get_cost(u)
		if( len(costDict) == 0):
			continue
		
		isUnlockable = True
		for i in costDict:
			cost = costDict[i]
			if( cost > num_items(i) ):
				isUnlockable = False

		if(isUnlockable):
			quick_print("unlocked",u)
			unlock(u)
			unlockCount = unlockCount+1
	return unlockCount

def getUnlocksLeft():
	unlockSet = set()

	for u in Unlocks:
		costDict = get_cost(u)
		for i in costDict:
			unlockSet.add(u)
	return unlockSet

def getUnlockItems():
	itemDict = {}
	for u in Unlocks:
		costDict = get_cost(u)
		for i in costDict:
			if(i in itemDict):
				itemDict[i] = itemDict[i] + costDict[i]
			else:
				itemDict[i] = costDict[i]
	return itemDict
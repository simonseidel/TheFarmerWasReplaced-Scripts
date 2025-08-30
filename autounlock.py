def attemptAutoUnlock():
	unlockSet = getUnlocksLeft()
	unlockCount = 0

	for unlock in unlockSet:
		costDict = get_cost(unlock)
		isUnlockable = True

		for item in costDict:
			cost = costDict[item]
			if( cost > num_items(item) ):
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
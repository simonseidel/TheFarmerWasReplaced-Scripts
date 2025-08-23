import plant
import maze
import snake
import worldsize
import sunflower
import pumpkin
import cactus

def autoRun():
	while(True):
		attemptAutoUnlock() #attempt to unlock anything possible

		itemDict = getUnlockItems() #get items and amount required for unlocks
		if( len(itemDict) == 0 ):
			return True #no more items required for unlocks = everything is unlocked
		
		unlockItem = None
		for i in itemDict:
			cost = itemDict[i]
			if( cost > num_items(i) ):
				if(i == Items.Gold and not maze.canAffordCreate()):
					continue
				if(i == Items.Bone and not snake.canAffordGame()):
					continue

				entity = plant.getItemEntity(unlockItem)
				if( plant.canAffordToPlant(entity, worldsize.getEntityMaxCount()) == False):
					continue

				unlockItem = i
				break #item found
	
		if(unlockItem == None):
			unlockItem = plant.getMinInventoryItem()

		if( plant.canAffordToPlant(Entities.Sunflower, worldsize.getEntityMaxCount()) and num_items(Items.Power) < 500):
			sunflower.autoFarm()
		elif(unlockItem == Items.Gold ):
			maze.autoPathFind()
		elif(unlockItem == Items.Bone ):
			snake.runGame()
		elif(unlockItem == Items.Pumpkin):
			pumpkin.autoFarm()
		elif(unlockItem == Items.Cactus):
			cactus.autoFarm()
		elif(unlockItem != None):
			plant.autoFarmEntity( plant.getItemEntity(unlockItem) )
		else:
			break #error
	return False #error


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
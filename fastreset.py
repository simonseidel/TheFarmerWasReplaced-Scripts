import autocollect
import planter
import misc
import sunflower
import maze
import snake
import pumpkin
import cactus
import polyculture
import weirdsubstance

def getAvailableUnlocks():
	unlockList = []
	
	for u in Unlocks:
		unlockCost = get_cost(u)
		if( len(unlockCost) == 0):
			continue #already unlocked
		
		isUnlockable = True
		for requiredItem in unlockCost:
			if( num_unlocked(requiredItem) == 0 ): #item required is not unlocked!
				isUnlockable = False

		if( isUnlockable == False):
			continue #not possible to unlock
		
		unlockList.append(u)

	return unlockList

def getNextUnlock():
	unlockList = getAvailableUnlocks()

	for u in unlockList:
		if( u == Unlocks.Expand ):
			return u #select this as first priority

	savedAmount = 0
	savedUnlock = None

	for u in unlockList:
		thisAmount = 0
		unlockDict = get_cost(u)

		for item in unlockDict:
			thisAmount = thisAmount + unlockDict[item]
			
		if(savedUnlock == None or thisAmount < savedAmount):
			savedUnlock = u
			savedAmount = thisAmount
	
	return savedUnlock
	
def getItemLowInventory():
	itemAmountDict = {
		Items.Hay:2*12*misc.getEntityMaxCount(),
		Items.Wood:2*12*misc.getEntityMaxCount(),
		Items.Carrot:4*10*misc.getEntityMaxCount(),
		Items.Pumpkin:2*20*misc.getEntityMaxCount(),
		Items.Weird_Substance:10*get_world_size()*num_unlocked(Unlocks.Mazes)
	}

	for item in itemAmountDict:
		if( item == Items.Wood and num_unlocked(Unlocks.Plant) == 0):
			continue
		
		if( item == Items.Carrot and num_unlocked(Unlocks.Carrots) == 0):
			continue
		
		if( item == Items.Pumpkin and num_unlocked(Unlocks.Pumpkins) == 0):
			continue

		if( item == Items.Weird_Substance and num_unlocked(Unlocks.Fertilizer) == 0 ):
			continue

		requiredAmount = itemAmountDict[item]
		if( num_items(item) < requiredAmount):
			return item

def autoRun(filename, speedup):
	if( num_unlocked(Unlocks.Leaderboard) > 0 ):
		leaderboard_run(Leaderboards.Fastest_Reset, filename, speedup)
	
	while( num_unlocked(Unlocks.Leaderboard) == 0 ):
		thisUnlock = getNextUnlock()
		if(thisUnlock == None):
			break

		thisCostDict = get_cost(thisUnlock)
		canPlant = num_unlocked(Unlocks.Plant) > 0
		canMove = num_unlocked(Unlocks.Expand) > 0
		canZigZag = num_unlocked(Unlocks.Expand) > 1

		for item in thisCostDict:
			entity = misc.getItemEntity(item)
			lastItem = None
			while( num_items(item) < thisCostDict[item] ):	
				lowItem = getItemLowInventory()
				if( lowItem != None or item == Items.Hay or item == Items.Wood or item == Items.Carrot ):
					if( lowItem == None ):
						plantItem = item
					else:
						plantItem = lowItem
					if( plantItem == Items.Pumpkin ):
						pumpkin.autoFarm()
					elif( plantItem == Items.Weird_Substance):
						weirdsubstance.autoFarm()
					elif( canZigZag ):
						polyculture.autoFarmEntity( misc.getItemEntity(plantItem) )
					else:
						entity = misc.getItemEntity(plantItem)
	
						if( can_harvest() ):
							harvest()
	
						entityType = get_entity_type()
						if( canPlant == True and entityType != entity and (entityType == None or entityType == Entities.Grass) ):
							plant(entity)
					
						if( canMove ):
							move(North)
				elif( item == Items.Power ):
					if( sunflower.autoFarm() == False ):
						break

				elif(item == Items.Gold ):
					if( maze.findTreasure() == False ):
						break

				elif( item == Items.Bone ):
					tillFirst = (minItem != lastItem)
					if(snake.runGame(tillFirst) == False ):
						break

				elif( item == Items.Pumpkin ):
					if( pumpkin.autoFarm() == False ):
						break

				elif( item == Items.Cactus ):
					if( cactus.autoFarm() == False ):
						break
				else:
					break
				lastItem = item

		unlockSuccess = unlock(thisUnlock)
		quick_print(thisUnlock, "unlock", unlockSuccess)

	return num_unlocked(Unlocks.Leaderboard) > 0
import maze
import cactus
import planter
import sunflower
import snake
import pumpkin
import polyculture
import misc
import weirdsubstance

def getMinInventoryItem():
	checkItemSet = {
		Items.Hay,
		Items.Wood,
		Items.Carrot,
		Items.Pumpkin,
		Items.Cactus,
		Items.Bone,
		Items.Weird_Substance,
		Items.Gold,
		Items.Power
	}

	plantableItemSet = {
		Items.Hay,
		Items.Wood,
		Items.Carrot,
		Items.Pumpkin,
		Items.Cactus,
		Items.Bone,
		Items.Power
	}

	savedItem = None
	for item in checkItemSet:
		if item in plantableItemSet:
			entity = misc.getItemEntity(item)
			maxEntityCount = misc.getEntityMaxCount()
			if not( planter.canAffordEntity(entity, maxEntityCount) ):
				continue #skip, cannot afford to plant this

		if(savedItem == None or num_items(item) < num_items( savedItem )):
			savedItem = item
	return savedItem

def fillInventory( harvestItem = None ):
	polycultureSet = {
		Items.Hay,
		Items.Wood,
		Items.Carrot
	}
	
	lastItem = None
	while(True):
		if( harvestItem == None ):
			minItem = getMinInventoryItem()	
		else:
			minItem = harvestItem

		if( minItem == Items.Power ):
			if( sunflower.autoFarm() == False):
				break

		elif(minItem == Items.Gold ):
			if( maze.findTreasure() == False):
				break

		elif( minItem == Items.Bone ):
			tillFirst = (minItem != lastItem)
			if( snake.runGame(tillFirst) == False ):
				break

		elif( minItem == Items.Weird_Substance ):
			if( weirdsubstance.autoFarm() == False ):
				break

		elif( minItem == Items.Pumpkin ):
			if( pumpkin.autoFarm() == False ):
				break

		elif( minItem == Items.Cactus ):
			if( cactus.autoFarm() == False ):
				break
		
		elif( minItem in polycultureSet ):
			if( polyculture.autoFarmEntity(misc.getItemEntity(minItem)) == False ):
				break 
		else:
			break #error
		lastItem = minItem

	return False
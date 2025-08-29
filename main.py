import maze
import cactus
import planter
import mover
import sunflower
import worldsize
import snake
import pumpkin
import misc
import polyculture

def getItemEntities(item):
	itemDict = {
		Items.Hay:[Entities.Grass],
		Items.Wood:[Entities.Tree,Entities.Bush],
		Items.Carrot:[Entities.Carrot],
		Items.Pumpkin:[Entities.Pumpkin],
		Items.Cactus:[Entities.Cactus],
		Items.Bone:[Entities.Apple,Entities.Dinosaur],
		Items.Weird_Substance:[None],
		Items.Gold:[Entities.Bush,Entities.Hedge,Entities.Treasure],
		Items.Water:[None],
		Items.Fertilizer:[None],
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
	checkItemSet = {
		Items.Hay,
		Items.Wood,
		Items.Carrot,
		Items.Pumpkin,
		Items.Cactus,
		Items.Bone,
		Items.Gold,
		Items.Power
	}

	plantableItemSet = {
		Items.Hay,
		Items.Wood,
		Items.Carrot,
		Items.Pumpkin,
		Items.Cactus,
		Items.Power
	}

	savedItem = None
	for item in checkItemSet:
		if item in plantableItemSet:
			entity = getItemEntity(item)
			maxEntityCount = worldsize.getEntityMaxCount()
			if not( planter.canAffordToPlant(entity, maxEntityCount) ):
				continue #skip, cannot afford to plant this
				
		if(item == Items.Gold and not maze.canAffordCreate()):
			continue

		if(item == Items.Bone and not snake.canAffordGame()):
			continue

		if(savedItem == None or num_items(item) < num_items( savedItem )):
			savedItem = item
	return savedItem

def main():
	planter.autoTill(Grounds.Soil)
	
	if(worldsize.setEven()):
		quick_print("world decreased to even size")
	
	while(True):
		#minItem = getMinInventoryItem()	
		minItem = Items.Gold
		
		if( minItem == Items.Power ):
			sunflower.autoFarm()
		elif(minItem == Items.Gold ):
			maze.autoPathFind()
		elif( minItem == Items.Bone ):
			snake.runGame()
		elif( minItem == Items.Pumpkin):
			pumpkin.autoFarm()
		elif( minItem == Items.Cactus):
			cactus.autoFarm()
		elif( minItem != None):
			polyculture.autoFarmEntity( planter.getItemEntity(minItem) )
		else:
			break #error
	return False	

clear()
main()

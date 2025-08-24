import entitydata
import maze
import cactus
import plant
import mover
import sunflower
import worldsize
import snake
import autounlock
import pumpkin
import fertilizer
import helper
import tree

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

	minItem = None
	for item in checkItemSet:
		if item in plantableItemSet:
			entity = plant.getItemEntity(item)
			maxEntityCount = worldsize.getEntityMaxCount()
			if not( plant.canAffordToPlant(entity, maxEntityCount) ):
				break #skip, cannot afford to plant this
			
		if(item == Items.Power and num_items(Items.Power) < 1000):
			return Items.Power
		
		if(item == Items.Gold and not maze.canAffordCreate()):
			continue

		if(item == Items.Bone and not snake.canAffordGame()):
			continue

		if(minItem == None or num_items(item) < num_items( minItem )):
			if(item == Items.Power):
				continue
			minItem = item
	return minItem

def main():
	plant.autoTill(Grounds.Soil)
	
	if(worldsize.setEven()):
		quick_print("world decreased to even size")
	
	while(True):
		minItem = getMinInventoryItem()	
		
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
		elif( minItem == Items.Wood):
			tree.autoFarm()
		elif( minItem != None):
			plant.autoFarmEntity( plant.getItemEntity(minItem) )
		else:
			break #error
	return False

main()



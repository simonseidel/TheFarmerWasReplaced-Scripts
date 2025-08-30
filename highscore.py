import maze
import cactus
import planter
import mover
import sunflower
import snake
import pumpkin
import misc
import polyculture
import highscore

def competeNow(leaderboard, dryRun = False, filename = "main", speedup = 256):
#	if( leaderboard == Leaderboards.Fastest_Reset):
#		leaderboard_run(Leaderboards.Fastest_Reset, filename, speedup)
#		fastresetDict = {Unlocks.Leaderboard:1}

	if( leaderboard == Leaderboards.Maze):	

		if( dryRun == False ):
			leaderboard_run(Leaderboards.Maze, filename, speedup)

		itemRequired = Items.Gold
		amountRequired = num_items(itemRequired) + 300000
		if( dryRun == False):
			amountRequired = 300000

		while( num_items(itemRequired) < amountRequired ):
			maze.autoPathFind()

		return True
	
	elif( leaderboard == Leaderboards.Dinosaur):
		planter.autoTill(Grounds.Soil)

		if( dryRun == False ):
			leaderboard_run(Leaderboards.Dinosaur, filename, speedup)
		
		itemRequired = Items.Bone
		amountRequired = num_items(itemRequired) + 98010
		if( dryRun == False):
			amountRequired = 98010
		
		while ( num_items(itemRequired) < amountRequired ):
			snake.runGame(True)
		
		return True
	
	elif(leaderboard == Leaderboards.Polyculture):
	
		itemRequiredDict = {
			Items.Wood:100000,
			Items.Carrot:100000,
			Items.Hay:100000
		}
		
		itemEntityDict = {
			Items.Wood:Entities.Tree,
			Items.Carrot:Entities.Carrot,
			Items.Hay:Entities.Grass
		}
			
		planter.autoTill(Grounds.Soil)
		
		if(dryRun == False):
			leaderboard_run(Leaderboards.Polyculture, filename, speedup)

		for item in itemRequiredDict:
			if(dryRun == False):
				continue
			requiredAmount = itemRequiredDict[item]
			currentAmount = num_items(item)
			amountGoal = requiredAmount+currentAmount
			amountDifference = amountGoal-currentAmount
			itemRequiredDict[item] = amountGoal
	
		while(True):
			goalReachedCount = 0
			for item in itemRequiredDict:
				requiredAmount = itemRequiredDict[item]		
				if( num_items(item) >= requiredAmount ):
					goalReachedCount = goalReachedCount+1

			if( goalReachedCount == len(itemRequiredDict) ):
				return True

			plantItem = None
			if( num_items(Items.Hay) < 10000 ):
				plantItem = Items.Hay
			elif ( num_items(Items.Wood) < 10000 ):
				plantItem = Items.Wood
			else:
				for item in itemRequiredDict:
					if(plantItem == None or num_items(item) < num_items( plantItem )):
						plantItem = item

			if not( plantItem in itemEntityDict):
				return False

			amountGoal = itemRequiredDict[plantItem]
			amountCurrent = num_items(plantItem)
			amountLeft = amountGoal - amountCurrent
			plantEntity = itemEntityDict[plantItem]

			quick_print("carrots",num_items(Items.Carrot), "hay",num_items(Items.Hay), "wood",num_items(Items.Wood))
			quick_print("planting",plantItem)
			
			polyculture.autoFarmEntity( plantEntity )

		return True

	elif(leaderboard == Leaderboards.Cactus):
	
		planter.autoTill(Grounds.Soil)
		
		if(dryRun == False):
			leaderboard_run(Leaderboards.Cactus, filename, speedup)

		itemRequired = Items.Cactus
		amountRequired = num_items(itemRequired) + 100000
		if(dryRun == False):
			amountRequired = 100000
	
		while ( num_items(itemRequired) < amountRequired ):
			cactus.autoFarm()

		return True
	
	elif(leaderboard == Leaderboards.Sunflowers):
		planter.autoTill(Grounds.Soil)

		if(dryRun == False):
			leaderboard_run(Leaderboards.Sunflowers, filename, speedup)

		itemRequired = Items.Power
		amountRequired = num_items(itemRequired) + 100000
		if(dryRun == False):
			amountRequired = 100000
		
		while( num_items(itemRequired) < amountRequired ):
			sunflower.autoFarm()

		return True

	elif(leaderboard == Leaderboards.Pumpkins):
	
		planter.autoTill(Grounds.Soil)
		
		if(dryRun == False):
			leaderboard_run(Leaderboards.Pumpkins, filename, speedup)

		itemRequired = Items.Pumpkin
		amountRequired = num_items(itemRequired) + 100000
		if(dryRun == False):
			amountRequired = 100000
	
		while( num_items(itemRequired) < amountRequired ):
			pumpkin.autoFarm()
		
		return True
	
	elif(leaderboard == Leaderboards.Wood):

		planter.autoTill(Grounds.Soil)

		if(dryRun == False):
			leaderboard_run(Leaderboards.Wood, filename, speedup)

		itemRequired = Items.Wood
		entityRequired = Entities.Tree
		amountRequired = num_items(itemRequired) + 100000
		if(dryRun == False):
			amountRequired = 100000
		
		while( num_items(itemRequired) < amountRequired ):
			polyculture.autoFarmEntity( entityRequired )

		return True
	
	elif(leaderboard == Leaderboards.Carrots):
	
		planter.autoTill(Grounds.Soil)

		if(dryRun == False):
			leaderboard_run(Leaderboards.Carrots, filename, speedup)

		itemRequired = Items.Carrot
		entityRequired = Entities.Carrot
		amountRequired = num_items(itemRequired) + 100000
		if(dryRun == False):
			amountRequired = 100000
		
		while( num_items(itemRequired) < amountRequired ):
			if( num_items(Items.Wood) < 5000):
				polyculture.autoFarmEntity(Entities.Tree)
			elif( num_items(Items.Hay) < 5000):
				polyculture.autoFarmEntity(Entities.Grass)
			else:
				polyculture.autoFarmEntity(entityRequired)
		
		return True
	
	elif(leaderboard == Leaderboards.Hay):
		planter.autoTill(Grounds.Soil)
	
		if(dryRun == False):
			leaderboard_run(Leaderboards.Hay, filename, speedup)
		
		itemRequired = Items.Hay
		entityRequired = Entities.Grass
		amountRequired = num_items(itemRequired) + 100000
		if(dryRun == False):
			amountRequired = 100000

		while( num_items(itemRequired) < amountRequired):
			polyculture.autoFarmEntity(entityRequired)

		return True
	return False
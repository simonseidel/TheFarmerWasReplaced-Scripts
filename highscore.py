import maze
import cactus
import sunflower
import snake
import pumpkin
import polyculture
import fastreset

def competeNow(leaderboard, filename = "highscore", speedup = 16):
	if( leaderboard == Leaderboards.Fastest_Reset):
		return fastreset.autoRun(filename, speedup)	
	if( leaderboard == Leaderboards.Maze):	
		leaderboard_run(Leaderboards.Maze, filename, speedup)

		itemRequired = Items.Gold
		amountRequired = 300000

		while( num_items(itemRequired) < amountRequired ):
			if( maze.findTreasure() == False ):
				break

		return num_items(itemRequired) >= amountRequired
	
	elif( leaderboard == Leaderboards.Dinosaur):
		leaderboard_run(Leaderboards.Dinosaur, filename, speedup)
		
		itemRequired = Items.Bone
		amountRequired = 98010

		tillFirst = True
		while ( num_items(itemRequired) < amountRequired ):
			if( snake.runGame(tillFirst) == False ):
				break
			tillFirst = False

		return num_items(itemRequired) >= amountRequired
	
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
					
		leaderboard_run(Leaderboards.Polyculture, filename, speedup)

		goalReachedCount = 0
		while( goalReachedCount < len(itemRequiredDict) ):
			
			goalReachedCount = 0
			for item in itemRequiredDict:
				requiredAmount = itemRequiredDict[item]		
				if( num_items(item) >= requiredAmount ):
					goalReachedCount = goalReachedCount+1

			if( goalReachedCount == len(itemRequiredDict) ):
				break

			plantItem = None
			if( num_items(Items.Hay) < 10000 ):
				plantItem = Items.Hay
			elif ( num_items(Items.Wood) < 10000 ):
				plantItem = Items.Wood
			else:
				for item in itemRequiredDict:
					if(plantItem == None or num_items(item) < num_items( plantItem )):
						plantItem = item

			plantEntity = itemEntityDict[plantItem]
			
			if( polyculture.autoFarmEntity( plantEntity ) == False):
				break

		return goalReachedCount >= len(itemRequiredDict)

	elif(leaderboard == Leaderboards.Cactus):		
		leaderboard_run(Leaderboards.Cactus, filename, speedup)

		itemRequired = Items.Cactus
		amountRequired = 100000

		while ( num_items(itemRequired) < amountRequired ):
			if( cactus.autoFarm() == False ):
				break

		return num_items(itemRequired) >= amountRequired

	elif(leaderboard == Leaderboards.Sunflowers):
		leaderboard_run(Leaderboards.Sunflowers, filename, speedup)

		itemRequired = Items.Power
		amountRequired = 100000

		while( num_items(itemRequired) < amountRequired ):
			if( sunflower.autoFarm() == False ):
				break

		return num_items(itemRequired) >= amountRequired

	elif(leaderboard == Leaderboards.Pumpkins):	
		leaderboard_run(Leaderboards.Pumpkins, filename, speedup)

		itemRequired = Items.Pumpkin
		amountRequired = 100000

		while( num_items(itemRequired) < amountRequired ):
			if( pumpkin.autoFarm() == False):
				break

		return num_items(itemRequired) >= amountRequired
	
	elif(leaderboard == Leaderboards.Wood):
		leaderboard_run(Leaderboards.Wood, filename, speedup)

		itemRequired = Items.Wood
		amountRequired = 100000

		while( num_items(itemRequired) < amountRequired ):
			if( polyculture.autoFarmEntity( Entities.Tree ) == False ):
				break

		return num_items(itemRequired) >= amountRequired
	
	elif(leaderboard == Leaderboards.Carrots):
		leaderboard_run(Leaderboards.Carrots, filename, speedup)

		itemRequired = Items.Carrot
		amountRequired = 100000

		while( num_items(itemRequired) < amountRequired ):
			entity = None
			if( num_items(Items.Wood) < 5000):
				entity = Entities.Tree
			elif( num_items(Items.Hay) < 5000):
				entity = Entities.Grass
			else:
				entity = Entities.Carrot
			
			if(entity == None):
				break
			
			if( polyculture.autoFarmEntity(entity) == False ):
				break

		return num_items(itemRequired) >= amountRequired
	
	elif(leaderboard == Leaderboards.Hay):	
		leaderboard_run(Leaderboards.Hay, filename, speedup)
		
		itemRequired = Items.Hay
		amountRequired = 100000

		while( num_items(itemRequired) < amountRequired ):
			if( polyculture.autoFarmEntity(Entities.Grass) == False ):
				break

		return num_items(itemRequired) >= amountRequired
	return False
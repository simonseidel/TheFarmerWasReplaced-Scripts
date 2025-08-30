import mover
import planter
import misc

isInitialized = False
mainSet = set() #only planted main entities
companionSet = set() #only planted companions
companionDict = set() #unplanted companions

def init():
	quick_print("polyculture.init() was called")
	
	global isInitialized
	global mainSet #only planted main entities
	global companionSet #only planted companions
	global companionDict #unplanted companions

	isInitialized = True
	mainSet = set()
	companionSet = set() 
	companionDict = {}

def autoFarmEntity(entity):
	runCount = 0
	runState = 0
	moveList = []
	mover.moveToPos( mover.getZigZagStartPos() )

	useFertilizer = planter.canAffordFertilize( num_items(Items.Fertilizer) )
	useUnFertilizer = useFertilizer == True and planter.canAffordUnfertilize( num_items(Items.Weird_Substance) )
	irrigateLevel = planter.getIrrigateLevel( num_items(Items.Water) )
	
	while( runState < 5):
		if( misc.isEven(runCount) ):
			moveList = mover.zigZagList
		else:
			moveList = mover.zigZagReverseList
		runCount = runCount+1 #next movements will be in opposite direction

		for dir in moveList:
			if(runState == 0): #plant
				if( entity == Entities.Tree and planter.plantHere(Entities.Tree) == False ):
					planter.plantHere(Entities.Grass)
				elif(entity != Entities.Tree):
					planter.plantHere(entity)
		
				mainSet.add( (get_pos_x(),get_pos_y()) )
		
				myCompanion = get_companion()
				if( myCompanion != None):
					(myCompanionEntity, (myCompanionX,myCompanionY)) = myCompanion
					companionDict[(myCompanionX,myCompanionY)] = myCompanionEntity
				
				if(irrigateLevel > 0):
					planter.irrigateHere(irrigateLevel, False)
			
				if(useFertilizer == True):
					planter.fertilizeHere()

			elif(runState == 1): #un-fertilize
				planter.unFertilizeHere()

			elif(runState == 2): #plant companions
				pos = ( get_pos_x(),get_pos_y() ) 
				if( pos in companionDict ):	
					companionEntity = companionDict[pos]
					if not( planter.canAffordToPlant(companionEntity, 1) ):
						companionDict.pop(pos)
					else:
						if( can_harvest() ):
							planter.harvestHere()
							mainSet.remove(pos)
		
							if( companionEntity == Entities.Tree and planter.plantHere(Entities.Tree) == False ):
								planter.plantHere(Entities.Grass)
							elif(companionEntity != Entities.Tree):
								planter.plantHere(companionEntity)
	
							companionDict.pop(pos)
							companionSet.add(pos)
	
				if(len(companionDict) == 0): #out of companions to plant
					runState = runState+1 
		
			elif(runState == 3): #harvest main
				pos = (get_pos_x(),get_pos_y())
				if( pos in mainSet ):
					if( can_harvest() ):
						planter.harvestHere()
						mainSet.remove(pos)
	
				if( len(mainSet) == 0): #out of main crops to harvest
					runState = runState+1

			elif(runState == 4): #harvest companions
				pos = (get_pos_x(),get_pos_y())
				if( pos in companionSet ):
					if( can_harvest() ):
						planter.harvestHere()
						companionSet.remove(pos)
					
				if( len(companionSet) == 0):
					runState = runState+1
					break

			if(dir != None):
				move(dir)

		if(runState == 0): #plant main crops
			if(useUnFertilizer == True):
				runState = 1 #do unfertilize
			else:
				runState = 2 #skip unfertilize
		
		elif(runState == 1): #unfertilize
			runState = runState+1
		elif(runState == 2): #plant companions
			pass
		elif(runState == 3): #harvest main
			pass
		elif(runState == 4): #harvest companion
			pass
		elif(runState == 5): #finished (unused)
			break

	return True
	
if(isInitialized == False):
	init()
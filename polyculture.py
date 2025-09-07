import mover
import planter
import misc

mainSet = set() #only planted main entities
companionSet = set() #only planted companions
companionDict = {} #unplanted companions

def init():
	quick_print("polyculture.init() was called")
	
	global mainSet #only planted main entities
	global companionSet #only planted companions
	global companionDict #unplanted companions

	mainSet = set()
	companionSet = set()
	companionDict = {}

def autoFarmEntity(entity):
	if( planter.canAffordEntity(entity, misc.getEntityMaxCount() ) == False ):
		return False

	if( planter.usedWorldSize != get_world_size() ):
		planter.init()
	
	if( mover.usedWorldSize != get_world_size() ):
		mover.init()

	init() #init polyculture
	
	runState = 0
	moveForward = True

	togglePoly = num_unlocked(Unlocks.Polyculture) > 0

	useFertilizer = num_unlocked(Unlocks.Fertilizer) > 0 and planter.canFertilize( misc.getEntityMaxCount() )

	useUnFertilizer = useFertilizer == True and planter.canUnfertilize( misc.getEntityMaxCount() )

	irrigateLevel = 0
	if( num_unlocked(Unlocks.Watering) > 0 ):
		irrigateLevel = planter.getIrrigateLevel( misc.getEntityMaxCount() )

	mover.moveToPos( mover.getZigZagStartPos() )
	
	while( runState < 5):
		moveToggled = True
		
		while( moveToggled == True ):
			if(runState == 0): #plant
				planter.harvestHere()

				if( entity == Entities.Tree and planter.plantHere(Entities.Tree) == False ):
					planter.plantHere(Entities.Grass)
				elif(entity != Entities.Tree):
					planter.plantHere(entity)
		
				mainSet.add( (get_pos_x(),get_pos_y()) )
		
				if( togglePoly == True ):
					myCompanion = get_companion()
					if( myCompanion != None):
						(myCompanionEntity, (myCompanionX,myCompanionY)) = myCompanion
						companionDict[(myCompanionX,myCompanionY)] = myCompanionEntity

				if(irrigateLevel > 0):
					planter.irrigateHere(irrigateLevel)
			
				if(useFertilizer == True):
					planter.fertilizeHere()

			elif(runState == 1): #un-fertilize
				planter.unFertilizeHere()

			elif(runState == 2): #plant companions
				pos = ( get_pos_x(),get_pos_y() ) 
				if( pos in companionDict ):	
					companionEntity = companionDict[pos]
					if not( planter.canAffordEntity(companionEntity, 1) ):
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
	
				if( len(companionDict) == 0 ): #out of companions to plant
					runState = runState+1 
		
			elif( runState == 3 ): #harvest main
				pos = (get_pos_x(),get_pos_y())
				if( pos in mainSet ):
					if( can_harvest() ):
						planter.harvestHere()
						mainSet.remove(pos)
	
				if( len(mainSet) == 0): #out of main crops to harvest
					if(togglePoly == True):
						runState = 4
					else:
						runState = 5
						moveToggled = False

			elif(runState == 4): #harvest companions
				pos = (get_pos_x(),get_pos_y())
				if( pos in companionSet ):
					if( can_harvest() ):
						planter.harvestHere()
						companionSet.remove(pos)

				if( len(companionSet) == 0):
					runState = runState+1
					moveToggled = False
			
			moveDirection = mover.zigZagDict[ (get_pos_x(), get_pos_y(), moveForward) ]
			if( moveDirection == None ):
				moveToggled = False
				moveForward = not moveForward
			
			if( moveToggled == True ):
				move(moveDirection)

		if(runState == 0): #plant main crops
			if(useUnFertilizer == True):
				runState = 1
			else:
				if( togglePoly == True ):
					runState = 2 
				else:
					runState = 3

		elif(runState == 1): #unfertilize
			if( togglePoly == True ):
				runState = 2
			else:
				runState = 3

		elif(runState == 2): #plant companions
			pass
		elif(runState == 3): #harvest main
			pass
		elif(runState == 4): #harvest companion
			pass
		elif(runState == 5): #finished (unused)
			pass

	return True
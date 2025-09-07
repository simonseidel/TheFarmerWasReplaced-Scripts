import mover
import planter
import misc

timeDict = {} #stores the time when planted
sizeDict = {} #stores the size of the sunflower
	
def init():
	quick_print("sunflower.init() was called")
	
	global timeDict #stores the time when planted
	global sizeDict #stores the size of the sunflower
	timeDict = {}
	sizeDict = {}

def getHarvestSet( ):
	#this set will contain all of the unique sizes on the grid, in unsorted order
	unsortedSizeSet = set()
	for sunflowerPos in sizeDict:
		thisSize = sizeDict[sunflowerPos]
		unsortedSizeSet.add( thisSize )

	#sizes sorted in descending order
	sortedSizeSet = set()
	
	while( len(unsortedSizeSet) > 0):
		savedSize = None
		for size in unsortedSizeSet:
			if(savedSize == None or size > savedSize):
				savedSize = size

		sortedSizeSet.add(savedSize)
		unsortedSizeSet.remove(savedSize)
	
	#this set will contain the biggest sizes in descending order, with growtime in descending order
	# example: 
	# 0: size=15 growtime 3
	# 1: size=15 growtime 2
	# 2: size=14 growtime 5
	# 3: size=14 growtime 4
	sortedHarvestSet = set()

	for size in sortedSizeSet:

		#this set will contain all entities with this size, in unsorted order
		unsortedHarvestSet = set()
		
		for sunflowerPos in sizeDict:
			thisSize = sizeDict[sunflowerPos]
			if(thisSize == size):
				unsortedHarvestSet.add( sunflowerPos )

		while( len(unsortedHarvestSet) > 0):
			savedGrowTime = None
			savedPos = None
		
			for sunflowerPos in unsortedHarvestSet:
				plantTime = timeDict[sunflowerPos]
				growTime = get_time() - plantTime
				if( savedPos == None or growTime > savedGrowTime):
					savedPos = sunflowerPos
					savedGrowTime = growTime
			
			unsortedHarvestSet.remove(savedPos)
			sortedHarvestSet.add(savedPos)

	return sortedHarvestSet

def autoFarm():
	if( num_unlocked(Unlocks.Sunflowers) == 0):
		return False

	if( planter.canAffordEntity(Entities.Sunflower, misc.getEntityMaxCount() ) == False):
		return False
 
	if( planter.usedWorldSize != get_world_size() ):
		planter.init()
	if( mover.usedWorldSize != get_world_size() ):
		mover.init()

	init() #sunflower initialize default values

	mover.moveToPos( mover.getZigZagStartPos() )
	
	fertilizeAll = num_unlocked(Unlocks.Fertilizer) > 0 and planter.canFertilize( misc.getEntityMaxCount() )

	unfertilizeAll = fertilizeAll == True and planter.canUnfertilize( misc.getEntityMaxCount() ) 

	irrigateLevel = planter.getIrrigateLevel( misc.getEntityMaxCount() )
	
	runState = 0
	goForward = True

	while( runState < 2 ):
		moveToggled = True
		while( moveToggled == True ):
			if(runState == 0):
				harvest()
				
				if( get_ground_type() != Grounds.Soil):
					till()

				if( planter.canAffordEntity(Entities.Sunflower, 1) == False ):
					return False

				planter.plantHere(Entities.Sunflower)

				pos = ( get_pos_x(),get_pos_y() )
				timeDict[pos] = get_time()
				sizeDict[pos] = measure()

				if(fertilizeAll == True):
					planter.fertilizeHere()

				if(irrigateLevel > 0):
					planter.irrigateHere(irrigateLevel)
			elif(runState == 1):
				planter.unFertilizeHere()
			
			moveDirection = mover.zigZagDict[(get_pos_x(),get_pos_y(),goForward)]
			if( moveDirection == None):
				moveToggled = False
				goForward = not goForward
			
			if(moveToggled == True):
				move(moveDirection)

		if(runState == 0): #plant and fertilize
			if( unfertilizeAll == True):
				runState = 1 # do un-fertilize
			else:
				runState = 2 # skip un-fertilize
		elif(runState == 1): #un-fertilize
			runState = 2
		elif(runState == 2): #harvest (unused state)
			pass

	harvestSet = getHarvestSet()
	for pos in harvestSet:
		mover.moveToPos(pos)

		while( can_harvest() == False ):
			planter.irrigateHere(irrigateLevel)

		if( planter.harvestHere() == True ):
			if( pos in timeDict):
				timeDict.pop(pos)
			if( pos in sizeDict):
				sizeDict.pop(pos)

	return True
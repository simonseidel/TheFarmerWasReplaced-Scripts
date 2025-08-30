import mover
import planter
import misc

isInitialized = False
timeDict = {} #stores the time when planted
sizeDict = {} #stores the size of the sunflower
	
def init():
	quick_print("sunflower.init() was called")
	
	global isInitialized
	global timeDict #stores the time when planted
	global sizeDict #stores the size of the sunflower
	
	isInitialized = True
	timeDict = {}
	sizeDict = {}

def initEntity(pos):
	if( pos in timeDict):
		timeDict.pop(pos)
	if( pos in sizeDict):
		sizeDict.pop(pos)

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
	if( isInitialized == False):
		init() #sunflower initialize default values

	mover.moveToPos( mover.getZigZagStartPos() )
	
	fertilizeAll = planter.canAffordFertilize( num_items(Items.Fertilizer) )

	unfertilizeAll = False
	if( fertilizeAll == True and planter.canAffordUnfertilize( num_items(Items.Weird_Substance) ) ):
		unfertilizeAll = True

	irrigateLevel = planter.getIrrigateLevel( num_items(Items.Water) )
	
	runState = 0
	runCount = 0
	moveList = []

	while( runState < 2 ):
		if( misc.isEven(runCount) ):
			moveList = mover.zigZagList
		else:
			moveList = mover.zigZagReverseList
		runCount = runCount+1 #next movements will be in opposite direction

		for dir in moveList:
			if(runState == 0):
				if( planter.plantHere(Entities.Sunflower) == False ):
					return False

				pos = ( get_pos_x(),get_pos_y() )
				timeDict[pos] = get_time()
				sizeDict[pos] = measure()

				if(fertilizeAll == True):
					planter.fertilizeHere()

				if(irrigateLevel > 0):
					planter.irrigateHere(irrigateLevel, False)
			elif(runState == 1):
				planter.unFertilizeHere()
				
			if(dir != None):
				move(dir)

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
			planter.irrigateHere(irrigateLevel, False)

		if( planter.harvestHere() == True ):
			initEntity(pos)

	return True

if(isInitialized == False):
	init()
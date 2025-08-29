import mover
import planter
import worldsize

timeDict = {} #gettime when planted
sizeDict = {} #location and size

def init():
	timeDict = {} #gettime when planted
	sizeDict = {} #location and size

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
	init() 
	
	mover.moveToPos( mover.getZigZagStartPos() )
	
	directionList = mover.getZigZagDirectionList()
	
	fertilizeAll = planter.canAffordFertilize( num_items(Items.Fertilizer) )

	irrigateLevel = planter.getIrrigateLevel( num_items(Items.Water) )
	
	for dir in directionList:
		if( planter.plantHere(Entities.Sunflower) == True ):
			pos = ( get_pos_x(),get_pos_y() )
			timeDict[pos] = get_time()
			sizeDict[pos] = measure()
		else:
			return False

		if(fertilizeAll == True):
			planter.fertilizeHere()

		if(irrigateLevel > 0):
			planter.irrigateHere(irrigateLevel)

		if(dir != None):
			move(dir)

	unfertilizeAll = False
	if( fertilizeAll == True and planter.canAffordUnfertilize( num_items(Items.Weird_Substance) ) ):
		unfertilizeAll = True

	if( unfertilizeAll == True ):
		directionList = mover.reverseZigZag(directionList)

		for dir in directionList:
			planter.unFertilizeHere()
			
			if(dir != None):
				move(dir)

	harvestSet = getHarvestSet()
	for pos in harvestSet:
		mover.moveToPos(pos)

		while(True):
			if ( can_harvest() ):
				if(planter.harvestHere() == True):
					if( pos in timeDict):
						timeDict.pop(pos)
					if( pos in sizeDict):
						sizeDict.pop(pos)
				break
			else:
				planter.irrigateHere(irrigateLevel)
	return True

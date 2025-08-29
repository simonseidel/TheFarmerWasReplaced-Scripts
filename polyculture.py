import mover
import planter
import misc

def autoFarmEntity(entity):
	mainSet = set() #only planted main entities
	companionSet = set() #only planted companions
	companionDict = {} #unplanted companions
	
	mover.moveToPos( mover.getZigZagStartPos() )

	directionList = mover.getZigZagDirectionList()
	
	useFertilizer = planter.canAffordFertilize( num_items(Items.Fertilizer) )
	useUnFertilizer = useFertilizer == True and planter.canAffordUnfertilize( num_items(Items.Weird_Substance) )
	irrigateLevel = planter.getIrrigateLevel( num_items(Items.Water) )
	
	for dir in directionList:
		if(entity == Entities.Tree):
			if( misc.isEven(get_pos_x()) and misc.isEven(get_pos_y()) ):
				planter.plantHere(entity)
			else:
				planter.plantHere(Entities.Bush)
		else:
			planter.plantHere(entity)

		mainSet.add( (get_pos_x(),get_pos_y()) )

		myCompanion = get_companion()
		if( myCompanion != None):
			(myCompanionEntity, (myCompanionX,myCompanionY)) = myCompanion
			companionDict[(myCompanionX,myCompanionY)] = myCompanionEntity
		
		if(irrigateLevel > 0):
			planter.irrigateHere(irrigateLevel)
	
		if(useFertilizer == True):
			planter.fertilizeHere()

		if(dir != None):
			move(dir)

	if(useUnFertilizer == True): #un-fertilize
		directionList = mover.reverseZigZag(directionList)
		
		for dir in directionList:
			planter.unFertilizeHere()
	
			if(dir != None):
				move(dir)

	while len(companionDict) > 0: #plant companions
		directionList = mover.reverseZigZag(directionList)

		for dir in directionList:		
			pos = ( get_pos_x(),get_pos_y() ) 
			if( pos in companionDict ):	
				companionEntity = companionDict[pos]
				if not( planter.canAffordToPlant(companionEntity, 1) ):
					companionDict.pop(pos)
				else:
					if( can_harvest() ):
						planter.harvestHere()
						mainSet.remove(pos)
	
						planter.plantHere(companionEntity)
						companionDict.pop(pos)
						companionSet.add(pos)

			if(dir != None):
				move(dir)

	while len(mainSet) > 0: #harvest main
		directionList = mover.reverseZigZag(directionList)
		
		for dir in directionList:
			pos = (get_pos_x(),get_pos_y())
			if( pos in mainSet ):
				if( can_harvest() ):
					planter.harvestHere()
					mainSet.remove(pos)

			if(dir != None):
				move(dir)
				
	while len(companionSet) > 0: #harvest companions
		directionList = mover.reverseZigZag(directionList)
		
		for dir in directionList:
			pos = (get_pos_x(),get_pos_y())
			if( pos in companionSet ):
				if( can_harvest() ):
					planter.harvestHere()
					companionSet.remove(pos)
				
			if(dir != None):
				move(dir)
	return True
import mover
import misc

def canAffordGame():
	costItem = None
	costAmount = None
	
	costDict = get_cost(Entities.Apple)
	for item in costDict:
		costItem = item
		costAmount = costDict[item]

	costAmount = costAmount * misc.getEntityMaxCount()
	
	if( costAmount > num_items(costItem) ):
		return False
	return True

def runGame( tillFirst ):
	applePos = None

	mover.moveToPos( mover.getCircuitStartPos() )
	
	if( tillFirst == True ):
		for dir in mover.circuitList:
			if(get_ground_type() != Grounds.Soil):
				till()
	
			if(dir != None):
				move(dir)
	
	change_hat(Hats.Dinosaur_Hat) #apply "snake hat"
	applePos = measure()

	while( applePos != None ):
		for dir in mover.circuitList:			
			if( (get_pos_x(),get_pos_y()) == applePos ):
				applePos = measure()
		
			if( move(dir) == False ):
				applePos = None

	change_hat(Hats.Straw_Hat) #remove "snake hat"
	return True
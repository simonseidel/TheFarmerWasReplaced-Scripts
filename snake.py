import worldsize
import mover

def getCostItem():
	costDict = get_cost(Entities.Apple)
	for item in costDict:
		return item
	return None		

def getCostAmount():
	costDict = get_cost(Entities.Apple)
	for item in costDict:
		return costDict[item]
	return None

def canAffordGame():
	costItem = getCostItem()
	costAmount = getCostAmount() * worldsize.getEntityMaxCount()
	if( costAmount > num_items(costItem) ):
		return False
	return True

def runGame():
	applePos = None

	mover.moveToPos( mover.getCircuitStartPos() )
	
	directionList = mover.getCircuitDirectionList()
	
	for dir in directionList:
		if(get_ground_type() != Grounds.Soil):
			till()
		move(dir)
	
	change_hat(Hats.Dinosaur_Hat) #apply "snake hat"
	applePos = measure()

	while(True):
		for dir in directionList:
			if(applePos == None):
				change_hat(Hats.Straw_Hat) #remove "snake hat"
				return False
				
			if( (get_pos_x(),get_pos_y()) == applePos):
				applePos = measure()
		
			if( move(dir) == False ):
				change_hat(Hats.Straw_Hat) #remove "snake hat"
				return True

	return False
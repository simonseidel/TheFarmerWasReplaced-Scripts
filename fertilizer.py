import worldsize
import entitydata

def getAffectedSet(x,y):
	affectedSet = set()
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()
	
	pos = (x,y) #here
	if( pos in entitydata.typeDict ):
		affectedSet.add(pos)

	if(x < maxX):
		pos = (x+1,y) #east
		if( pos in entitydata.typeDict ):
			affectedSet.add(pos) 
	if(x > minX):
		pos = (x-1,y) #west
		if( pos in entitydata.typeDict ):
			affectedSet.add(pos) 
	if(y < maxY):
		pos = (x,y+1) #north
		if( pos in entitydata.typeDict ):
			affectedSet.add(pos) 
	if(y > minY):
		pos = (x,y-1) #south
		if( pos in entitydata.typeDict ):
			affectedSet.add(pos) 
	return affectedSet

def getInfectedInSet(inputSet):
	returnSet = set()
	for pos in inputSet:
		if( pos in entitydata.infectedSet):
			returnSet.add(pos)
	return returnSet

def putHere():
	if( get_entity_type() == Entities.Bush):
		return False #bushes can't be un-fertilized

	if(not can_harvest() and num_items(Items.Fertilizer) > 0):
		use_item(Items.Fertilizer)
		entitydata.infectedSet.add( (get_pos_x(),get_pos_y()) )
	return True

def undoHere():
	if(get_entity_type() == Entities.Bush):
		return False #this would create a maze

	affectedSet = getAffectedSet(get_pos_x(),get_pos_y())
	infectedInSet = getInfectedInSet(affectedSet)
	
	if(len(affectedSet) == 0):
		return False
	
	if not(len(affectedSet) == len(infectedInSet)):
		return False #use if it only affects infected plants
	
	if(num_items(Items.Weird_Substance) == 0):
		return False
	
	use_item(Items.Weird_Substance)
	for pos in affectedSet:
		if( pos in infectedInSet ):
			entitydata.infectedSet.remove(pos)
		else:
			entitydata.infectedSet.add(pos)	
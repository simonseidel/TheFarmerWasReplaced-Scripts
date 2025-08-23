import helper

def getEntityMaxCount():
	return (get_world_size() * get_world_size())

def setEven():
	if( helper.isEven(get_world_size()) ):
		return False

	set_world_size(get_world_size()-1)
	return True

def getMinMaxXXYY():
	#return tuple (minx,maxx,miny,maxy)
	minX = 0
	maxX = get_world_size()-1
	minY = 0
	maxY = get_world_size()-1
	return minX,maxX,minY,maxY
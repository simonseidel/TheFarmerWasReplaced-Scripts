import misc

def getEntityMaxCount():
	return (get_world_size() * get_world_size())

def setEven():
	if( misc.isOdd(get_world_size()) ):
		set_world_size(get_world_size()-1)
		return True
	return False

def getMinMaxXXYY():
	#return tuple (minx,maxx,miny,maxy)
	minX = 0
	maxX = get_world_size()-1
	minY = 0
	maxY = get_world_size()-1
	return minX,maxX,minY,maxY
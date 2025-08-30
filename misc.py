def isOdd(n):
	return n % 2 != 0

def isEven(n):
	return n % 2 == 0

def waitForSeconds(seconds):
	startTime = get_time()
	finishTime = startTime + seconds
	while( get_time() < finishTime ):
		pass

def getEntityMaxCount():
	return (get_world_size() * get_world_size())

def getWorldMinMaxXXYY():
	#return tuple (minx,maxx,miny,maxy)
	minX = 0
	maxX = get_world_size()-1
	minY = 0
	maxY = get_world_size()-1
	return minX,maxX,minY,maxY
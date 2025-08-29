def isOdd(n):
	return n % 2

def isEven(n):
	return not isOdd(n)

def waitForSeconds(seconds):
	startTime = get_time()
	finishTime = startTime + seconds
	while( get_time() < finishTime ):
		pass
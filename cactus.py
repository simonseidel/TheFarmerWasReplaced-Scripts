import worldsize
import mover

def autoSwap(minX, maxX, minY, maxY):
	x = get_pos_x()
	y = get_pos_y()
	swapCount = 0
	
	if(x > minX and measure(West) > measure() and swap(West)):
		swapCount = swapCount + 1	
	if(x < maxX and measure(East) < measure() and swap(East)):
		swapCount = swapCount + 1
	if(y > minY and measure(South) > measure() and swap(South)):
		swapCount = swapCount + 1
	if(y < maxY and measure(North) < measure() and swap(North)):
		swapCount = swapCount + 1
	return swapCount

def autoFarm():
	runState = 0

	mover.moveToPos( mover.getCircuitStartPos() )
	
	directionList = mover.getCircuitDirectionList()
	
	(minX,maxX,minY,maxY) = worldsize.getMinMaxXXYY()
	
	while True:
		loopSwapCount = 0
		for dir in directionList:
			if(runState == 0):
				if(plant(Entities.Cactus) == False):
					return False
			elif(runState == 1):
				while(True):
					thisCount = autoSwap(minX, maxX, minY, maxY)
					if(thisCount == 0):
						break
					loopSwapCount = loopSwapCount + thisCount	
			
			if( ( get_pos_x(),get_pos_y() ) == mover.getCircuitEndPos() ):
				if(runState == 0):
					runState = runState+1
				elif(runState == 1):
					if( loopSwapCount == 0 and can_harvest() and harvest() == True):
						return True
			move(dir)
	return False
import misc
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
	mover.moveToPos( mover.getZigZagStartPos() )
	
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()
	
	runState = 0
	runCount = 0
	moveList = []
	
	while runState < 2:
		if( misc.isEven(runCount) ):
			moveList = mover.zigZagList
		else:
			moveList = mover.zigZagReverseList
		runCount = runCount+1 #next movements will be in opposite direction

		loopSwapCount = 0
		for dir in moveList:
			if(runState == 0):
				if(plant(Entities.Cactus) == False):
					return False
			elif(runState == 1):
				while( True ):
					thisCount = autoSwap(minX, maxX, minY, maxY)
					if( thisCount == 0 ):
						break

					loopSwapCount = loopSwapCount + thisCount
	
			if(dir != None):
				move(dir)

		#reached end
		if(runState == 0):
			runState = 1
		elif(runState == 1):
			if( loopSwapCount > 0 ):
				continue

			mover.moveToPos( (minX,minY) )

			while( can_harvest() == False ):
				pass
			
			if( harvest() == False ):
				return False

			runState = 2
	return True
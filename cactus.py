import misc
import mover
import planter

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
	if( num_unlocked(Unlocks.Cactus) == 0 ):
		return False

	if( planter.canAffordEntity(Entities.Cactus, misc.getEntityMaxCount()) == False ):
		return False

	if( mover.usedWorldSize != get_world_size() ):
		mover.init()

	mover.moveToPos( mover.getZigZagStartPos() )
	
	(minX,maxX,minY,maxY) = misc.getWorldMinMaxXXYY()

	runState = 0
	isForward = True

	while runState < 2:
		loopSwapCount = 0
		moveToggled = True

		while( moveToggled == True ):
			if(runState == 0):
				harvest()
				
				if( get_ground_type() != Grounds.Soil):
					till()

				if( planter.canAffordEntity(Entities.Cactus, 1) == False):
					return False

				plant(Entities.Cactus)
			elif(runState == 1):
				while( True ):
					thisCount = autoSwap(minX, maxX, minY, maxY)
					if( thisCount == 0 ):
						break

					loopSwapCount = loopSwapCount + thisCount
	
			moveDirection = mover.zigZagDict[(get_pos_x(),get_pos_y(),isForward)]
			if( moveDirection == None):
				isForward = not isForward
				moveToggled = False
			
			if(moveToggled == True):
				move(moveDirection)	

		#reached end
		if(runState == 0):
			runState = 1
		
		elif(runState == 1):
			if( loopSwapCount > 0 ):
				continue

			mover.moveToPos( (minX,minY) )

			if(can_harvest() == False):
				return False
			
			harvest()
			runState = 2
	return True
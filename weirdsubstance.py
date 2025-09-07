import mover

def autoFarm():
	if( num_unlocked(Unlocks.Fertilizer) == 0 ):
		return False

	if( num_items(Items.Fertilizer) == 0 ):
		return False

	if( mover.usedWorldSize != get_world_size() ):
		mover.init()

	moveForward = True

	mover.moveToPos( mover.getZigZagStartPos() )

	while( True ):
		if( moveForward ):
			if( num_items(Items.Fertilizer) == 0 ):
				moveForward = not moveForward
			else:
				harvest()

				plantEntity = None
				groundTarget = Grounds.Grassland
				if( num_items(Items.Hay) > 0 ):
					plantEntity = Entities.Grass
					groundTarget = Grounds.Soil

				if( get_ground_type() != groundTarget ):
					till()

				if( plantEntity != None ):
					plant(plantEntity)

				use_item(Items.Fertilizer)
		else:
			harvest()

		pos = (get_pos_x(), get_pos_y(), moveForward)
		moveDirection = mover.zigZagDict[pos]

		if( moveDirection == None ):
			if( moveForward == False):
				break #back at starting point
			moveForward = not moveForward

		if( moveDirection != None ):
			move(moveDirection)

	return True
	
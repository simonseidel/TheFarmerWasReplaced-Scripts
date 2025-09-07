import mover
import misc
import planter

def autoFarm():
	if( num_unlocked(Unlocks.Pumpkins) == 0):
		return False

	if( planter.canAffordEntity(Entities.Pumpkin, misc.getEntityMaxCount()) == False):
		return False
	
	if( mover.usedWorldSize != get_world_size() ):
		mover.init()

	runState = 0
	moveForward = True

	irrigateLevel = 0
	if( num_unlocked(Unlocks.Watering) > 0 ):
		irrigateLevel = planter.getIrrigateLevel( misc.getEntityMaxCount() )

	mover.moveToPos( mover.getZigZagStartPos() )
	
	while( runState < 4 ):
		moveToggled = True
		
		while( moveToggled == True ):
			if(runState == 0): #plant pumpkins
				entityType = get_entity_type()
				if( entityType != Entities.Pumpkin and entityType != None ):
					harvest()

				if( get_ground_type() != Grounds.Soil):
					till()

				if( entityType != Entities.Pumpkin):
					if( planter.canAffordEntity(Entities.Pumpkin, 1) == False ):
						return False

					plant(Entities.Pumpkin)

				while( irrigateLevel > 0 and get_water() < irrigateLevel and num_items(Items.Water) > 0 ):
					use_item(Items.Water)

			elif(runState == 1 or runState == 2): 
				if( get_entity_type() != Entities.Pumpkin ):				
					plant(Entities.Pumpkin)
					runState = 0 #plant pumpkins		

			elif(runState == 3):
				if( can_harvest()):
					harvest()

			pos = (get_pos_x(), get_pos_y(), moveForward)
			moveDirection = mover.zigZagDict[pos]

			if( moveDirection == None ):
				moveToggled = False
				moveForward = not moveForward

			if( moveToggled == True ):
				move(moveDirection)

		#reached end
		if(runState == 0): #plant pumpkins
			runState = runState+1

		elif( runState == 1 or runState == 2 ): #count pumpkins
			runState = runState + 1

		elif(runState == 3):
			runState = 4

	return True
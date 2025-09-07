import mover
import misc
import planter

def runGame( tillFirst ):
	if( num_unlocked(Unlocks.Dinosaurs) == 0 ):
		return False

	if( planter.canAffordEntity(Entities.Apple, misc.getEntityMaxCount()) == False ):
		return False

	starterBone = num_items(Items.Bone)

	worldStartSize = get_world_size()
	if( misc.isOdd(worldStartSize) ):
		set_world_size(worldStartSize-1)

	if( mover.usedWorldSize != get_world_size() ):
		mover.init()

	mover.moveToPos( mover.getCircuitStartPos() )
	
	if( tillFirst == True ):
		change_hat( Hats.Straw_Hat ) #apply default hat

	tillToggled = tillFirst
	while( tillToggled == True ):
		harvest()

		if( get_ground_type() != Grounds.Soil ):
			till()

		move( mover.circuitDict[ (get_pos_x(),get_pos_y()) ] )

		if( (get_pos_x(),get_pos_y()) == mover.getCircuitStartPos() ):
			tillToggled = False

	change_hat(Hats.Dinosaur_Hat) #apply "snake hat"
	applePos = measure()

	mover.moveToPos(applePos)
	
	while( applePos != None ):
		pos = ( get_pos_x(),get_pos_y() )
		if( pos == applePos ):
			applePos = measure()

		moveDirection = mover.circuitDict[pos]
		if( move(moveDirection) == False ):
			applePos = None

	change_hat(Hats.Straw_Hat) #remove "snake hat"

	if( get_world_size() < worldStartSize ):
		set_world_size(worldStartSize)

	return num_items(Items.Bone) > starterBone
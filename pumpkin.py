import mover
import misc

def autoFarm():
	mover.moveToPos( mover.getCircuitStartPos() )
	
	runState = 0
	while( runState < 3 ):
		pumpkinCount = 0 #contains how many pumpkins there are
		
		for dir in mover.circuitList: #plant all pumpkins
			if(runState == 0): #plant pumpkins
				if( get_entity_type() != Entities.Pumpkin):
					plant(Entities.Pumpkin)
					
					if( num_items(Items.Water) > 0 and get_water() < 0.5):
						use_item(Items.Water)					
			elif(runState == 1 or runState == 2): #count pumpkins, twice 
				if( get_entity_type() != Entities.Pumpkin):				
					plant(Entities.Pumpkin)
					runState = 0 #plant pumpkins
				else:
					pumpkinCount = pumpkinCount+1 #add one pumpkin to the count					
			
			if( dir != None ):
				move(dir)

		#reached end
		if(runState == 0): #plant pumpkins
			runState = runState+1
		elif(runState == 1): #count pumpkins
			if( pumpkinCount < misc.getEntityMaxCount() ):
				runState = 0
			else:
				runState = runState + 1
		elif(runState == 2):
			if( pumpkinCount < misc.getEntityMaxCount() ):
				runState = 0
			else:
				while( can_harvest() == False ):
					pass
		
				if( harvest() == True ):
					runState = runState + 1
				else:
					return False #error

	return True
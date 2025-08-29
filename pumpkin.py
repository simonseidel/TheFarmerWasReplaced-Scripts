import worldsize
import mover

def autoFarm():
	runState = 0
	
	mover.moveToPos( mover.getCircuitStartPos() )
	
	directionList = mover.getCircuitDirectionList()

	while(True):
		pumpkinCount = 0
		
		for dir in directionList: #plant all pumpkins
			if(runState == 0):	
				if( get_entity_type() != Entities.Pumpkin):
					plant(Entities.Pumpkin)
					
					if( num_items(Items.Water) > 0 and get_water() < 0.25):
						use_item(Items.Water)					
			elif(runState == 1):
				if( get_entity_type() != Entities.Pumpkin):				
					plant(Entities.Pumpkin)
					if( num_items(Items.Water) > 0 and get_water() < 0.25):
						use_item(Items.Water)

					runState = runState-1
				else:
					pumpkinCount = pumpkinCount+1
			if( (get_pos_x(),get_pos_y()) == mover.getCircuitEndPos()):
				if(runState == 0):
					runState = runState+1
				elif(runState == 1):
					if(pumpkinCount == worldsize.getEntityMaxCount()):
						if( can_harvest() and harvest() == True):
							return True
					else:
						runState = runState-1
			move(dir)


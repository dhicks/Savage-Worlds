from random import randint

def roll_die (faces, wild=False):
	# Roll a single die, possibly with a wild die. 
	# faces : number of faces on the die
	# wild : whether to also roll a wild die
	if faces < 1:
		# if the caller tries to roll a 'zero-sided die', just return 0
		return 0, (0, 0)
	roll = randint(1,faces)
	if roll == faces:
		# explosion!  recursion FTW
		roll += roll_die(faces, False)[0]
	if wild:
		wild_roll = roll_die(6, False)[0]
	else:
		wild_roll = 0
	result = max(roll, wild_roll)
	# since some tests need to know both results, return a tuple
	return result, (roll, wild_roll)

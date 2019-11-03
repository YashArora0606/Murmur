def exact(grid): # takes in 3 sound objects, computes angle relative to s1 and volume of sound source (CCW angle is negative, CW is positive)
	temp = [a.dir for a in grid]
	index = temp.index(min(temp))
	if index == 0:
		s1 = grid[1]
		s2 = grid[2]
		angle = 600
	elif index == 1:
		s1 = grid[0]
		s2 = grid[2]
		angle = 360
	elif index == 2:
		s1 = grid[0]
		s2 = grid[1]
		angle = 120
	angle = ((angle + s1.dir + s2.dir) / 2) % 360
	vol = (s1.vol + s2.vol) / 2
	return Sound(vol, angle, s1.time)

# Generates random sound data for presentation
def gen_random(time):
	angle = random() * 360
	volume = random() * 5 + 95
	s1 = Sound(volume + randint(-5, 8), angle + randint(-3, 3), time)
	s2 = Sound(volume + randint(-10, 16), angle + randint(-7, 13), time)
	s3 = Sound(volume + randint(-2, 10), angle + randint(-1, 32), time)
	return [s1, s2, s3]
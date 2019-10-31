import random
from random import random, randint
from app import Sound

def exact(grid): # takes in 3 sound objects, computes angle relative to s1 and volume of sound source (CCW angle is negative, CW is positive)
	s1 = grid[0]
	s2 = grid[1]
	s3 = grid[2]
	angle = ((s1.dir + s2.dir + s3.dir + 360) % 360) / 3
	vol = (s1.vol + s2.vol + s3.vol) / 3
	return Sound(angle, vol, s1.time)

def gen_random(time):
	angle = random() * 360
	volume = random() * randint(10, 37)
	s1 = Sound(volume + randint(-5, 8), angle + randint(-3, 3), time)
	s2 = Sound(volume + randint(-17, 25), angle + randint(-7, 13), time)
	s3 = Sound(volume + randint(-2, 10), angle + randint(-1, 32), time)
	return [s1, s2, s3]

def triangulate():
	return 0;
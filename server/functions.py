import io, base64, random, matplotlib.pyplot as plt, pandas as pd, os, datetime, threading, numpy as np
from random import random, randint
from app import Sound
from math import pi
from threading import Timer
from datetime import datetime
from matplotlib import figure

# Calculates exact location of sound
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
	volume = random() * randint(10, 37)
	s1 = Sound(volume + randint(-5, 8), angle + randint(-3, 3), time)
	s2 = Sound(volume + randint(-17, 25), angle + randint(-7, 13), time)
	s3 = Sound(volume + randint(-2, 10), angle + randint(-1, 32), time)
	return [s1, s2, s3]

# Generates and saves radar image
def gen_radar(sound):	
	img = io.BytesIO()

	r1 = sound.vol
	theta1 = -(sound.dir * pi / 180) + pi/2

	plt.figure(figsize=(4, 4))
	theta = [0, theta1]
	r = [0, r1]
	ax = plt.subplot(111, projection='polar')
	ax.set_xticklabels([])
	ax.set_yticklabels([])
	ax.plot(theta, r, color='#f4623a')
	ax.xaxis.grid(True, color='#ffffff', linestyle='-')
	ax.yaxis.grid(True, color='#ffffff')
	ax.spines['polar'].set_visible(False)
	ax.set_rmin(0)

	plt.savefig(img, format='png', transparent=True)
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()
	plt.close()
	
	return 'data:image/png;base64,{}'.format(graph_url)

def triangulate():
	return 0;
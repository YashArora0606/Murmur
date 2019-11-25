import io, base64, random, matplotlib.pyplot as plt, pandas as pd, os, datetime, threading, numpy as np
from random import random, randint
from app import Sound
from math import pi, atan2, sqrt, degrees, log10
from threading import Timer
from datetime import datetime
from matplotlib import figure

# Converts amplitude to dB
def convert(sounds):
	for i in range(len(sounds)):
		for j in range(len(sounds[i])):
			sounds[i][j] = 10 * log10(sounds[i][j])

# Calculates exact location of sound (relative to 1 module)
def relative_location(v): # takes in a list v of 3 volumes (from 0 = top, CW); treat right = +ve x, up = +ve y
	v1 = v[1]
	v2 = v[2]
	v3 = v[0]
	vec = [v1 * sqrt(3)/2 - v2 * sqrt(3)/2, -v1/2 - v2/2 + v3]
	angle = 450 - degrees(atan2(vec[1], vec[0]))
	angle %= 360
	vol = 20 * sqrt(vec[0] ** 2 + vec[1] ** 2)
	return Sound(vol, angle, datetime.now().strftime('%I:%M:%S%p'))

# Calculates exact coordinates of sound source (absolute coordinates)
def absolute_location(sound1, sound2, mod1, mod2): # inputs: relative locations of sound to 2 modules, absolute locations of 2 modules
	angle1 = radians((450 - sound1.dir) % 360)
	angle2 = radians((450 - sound2.dir) % 360)
	t = ((mod2.y - mod1.y) * sin(angle1) - (mod2.x - mod1.x) * cos(angle1)) / (sin(angle2) * cos(angle1) - cos(angle2) * sin(angle2))
	new_coords = [mod2.x + t * sin(angle2), mod2.y + t * cos(angle2)]
	new_volume = (sound1.vol + sound2.vol) / 2
	return Source(new_volume, new_coords[0], new_coords[1], sound1.time)

# Generates and saves RADAR image
def generate_radar(sounds):
	img = io.BytesIO()

	r1 = [sound.vol for sound in sounds]
	theta1 = [-(sound.dir * pi / 180) + pi/2 for sound in sounds]

	plt.figure(figsize=(4, 4))
	theta = theta1
	r = r1
	ax = plt.subplot(111, projection='polar')
	ax.set_xticklabels([])
	ax.set_yticklabels([])
	ax.plot(theta, r, 'o', color='#E6ADFF', markersize=12, markerfacecolor='#E6ADFF', markeredgecolor='#E6ADFF')
	ax.xaxis.grid(True, color='#ffffff', linestyle='-')
	ax.yaxis.grid(True, color='#ffffff')
	ax.spines['polar'].set_visible(False)
	ax.set_rmin(0)
	ax.set_rmax(120)

	plt.savefig(img, format='png', transparent=True, bbox_inches='tight')
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()
	plt.close()

	return 'data:image/png;base64,{}'.format(graph_url)

# Generates and saves MAP graph
def generate_map(sounds):
	img = io.BytesIO()

	x = [sound.x for sound in sounds]
	y = [sound.y for sound in sounds]
	s = [sound.vol for sound in sounds]

	plt.scatter(x, y, s)
	plt.savefig(imt, format='png', transparent = True, bbox_inches='tight')
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()
	plt.close()

	return 'data:image/png;base64,{}'.format(graph_url)
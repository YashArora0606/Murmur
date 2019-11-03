import io, base64, random, matplotlib.pyplot as plt, pandas as pd, os, datetime, threading, numpy as np
from random import random, randint
from app import Sound
from math import pi, atan2, sqrt, degrees, log10
from threading import Timer
from datetime import datetime
from matplotlib import figure

# Converts amplitude to dB
def convert(a):
	return 10 * log10(a)

# Calculates exact location of sound
def exact(v): # takes in a list v of 3 volumes (from 0 = top, CW); treat right = +ve x, up = +ve y
	index = v.index(min(v))
	if index == 0:
		v1 = v[1]
		v2 = v[2]
		vec = [v1 * sqrt(3)/2 - v2 * sqrt(3)/2, -v1/2 - v2/2]
		angle = 450 - degrees(atan2(vec[1], vec[0]))
	elif index == 1:
		v1 = v[0]
		v2 = v[2]
		vec = [-v2 * sqrt(3)/2, v1 - v2/2]
		angle = 450 - degrees(atan2(vec[1], vec[0]))
	elif index == 2:
		v1 = v[0]
		v2 = v[1]
		vec = [v2 * sqrt(3)/2, v1 - v2/2]
		angle = 90 - degrees(atan2(vec[1], vec[0]))
	angle %= 360
	vol = sqrt(v1 ** 2 + v2 ** 2)
	return Sound(vol, angle, datetime.now().strftime('%I:%M:%S%p'))

# Generates random sound volumes for presentation
def gen_random():
	# volume = random() * 5 + 60
	# s1 = volume + randint(-5, 8)
	# s2 = volume + randint(-10, 16)
	# s3 = volume + randint(-2, 10)
	s1 = randint(40, 75)
	s2 = randint(40, 75)
	s3 = randint(40, 75)
	return [s1, s2, s3]

# Generates and saves radar image
def gen_radar(sounds):
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

def triangulate():
	return 0;

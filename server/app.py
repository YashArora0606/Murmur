import Flask
import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class sound:
	def __init__(vol, direc, time):
		self.vol = vol
		self.dir = direc
		self.time = time
import os
import requests
import module
import re
from flask import *
from functions import *
import matplotlib.pyplot as plt

###############################################################################
# OBJECTS
###############################################################################
# Sound sample (for relative position to one module)
class Sound:
	def __init__(self, vol = 0, direc = 0, time = 0):
		self.vol = vol
		self.dir = direc
		self.time = time

# Sound sources
class Source:
	def __init__(self, vol = 0, x = 0, y = 0, time = 0):
		self.vol = vol
		self.x = x
		self.y = y
		self.time = time

# Data transfer to website
class Data:
	def __init__(self, n = 0, avgvol = 0, time = 0):
		self.n = n
		self.avgvol = avgvol
		self.time = time

# Module Location (coordinates)
class Module_Location:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

###############################################################################
# CONSTANTS
###############################################################################
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
x = 3 # size of grid: width
y = 3 # size of grid: height
grid = []
module_locations = [] # list of Module_Location objects (contains locations of modules)
times = [] # list of times of files in folder
tdelta = 3.0 # refresh delay
FILE_NAME = ''
nSamples = 5
zoom = 20
modules = {}

# App initialization
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

###############################################################################
# HELPERS
###############################################################################
# Run a function periodically
def refresh(f, delay):
	t = Timer(delay, f)
	t.start()

# Update sample data datetime.now().strftime('%I:%M:%S%p')
def update():
	global grid, nSamples, zoom, times, UPLOAD_FOLDER
	# Initialize times
	for file in os.listdir(UPLOAD_FOLDER):
		if re.match(r".*\.wav", file):
			currTime = file.split('-')[2]
			if currTime not in times:
				times.append(currTime)

	for time in times:
		modules[time] = module.get_modules(time) # list of Modules

	grid = []
	try:
		mostRecent = modules[max(modules.keys())]
	except:
		mostRecent = []
	for mod in mostRecent:
		grid.append(mod.convertToVolumeList())

	# grid = Module.convertToVolumeList(Module.find_module_events(smooth1, smooth2, smooth3), smooth1, smooth2, smooth3)
	convert(grid)

	if len(grid) and grid[0]:
		nSamples = len(grid[0])
	else:
		nSamples = 1



	# module.read_files(times)
	# module.process_files()

	# nSamples = round(random() * 8 + 1)

# Print info to console
def print_grid():
	global tdelta, x, y, grid
	points = list(map(relative_location, grid))
	for data in points:
		print('-------------------------------')
		print('Volume: ' + str(data.vol) + ', Direction: ' + str(data.dir) + ', Time: ' + str(data.time))
		print('-------------------------------')

# Put relevant data in Data object to send to front-end
def generate_data(points):
	global nSamples
	average = round(sum([point.vol for point in points]) / nSamples, 2)
	return Data(nSamples, average, points[0].time)

###############################################################################
# ROUTES
###############################################################################
# Upload
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(UPLOAD_FOLDER, f.filename))
	return redirect(url_for(index))

# Home
@app.route('/', methods = ['GET', 'POST'])
def index():
	global grid, tdelta, nSamples
	update()
	print("Past update")
	# print_grid()
	############################################################################
	# TODO: Only take the most recent recordings and put them in a Sound object, ignore all others
	for elem in grid:
		points = list(map(relative_location, elem))
	for display in points:
		display.vol = round(display.vol, 2)
		display.dir = round(display.dir, 2)
	address = generate_radar(points)
	# address2 = generate_map(points)
	data = generate_data(points)
	return render_template('index.html', data=data, address=address, tdelta=tdelta)

# Test POST Requests
@app.route('/listen', methods = ['POST'])
def listen():
	global FILE_NAME
	if request.method == 'POST':
		print('RECEIVED')
		f = request.files['file']
		f.save(os.path.join('uploads', f.filename))
		FILE_NAME = f.filename
		print('File name: ' + FILE_NAME)
		# print('IP Address:' + request.text)
	return redirect('/')

@app.route('/test', methods = ['POST'])
def test():
	if request.method == 'POST':
		print('RECEIVED TEST')
		print(request.data)
	return redirect('/')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

import os, datetime, threading
from flask import *
from threading import Timer
from triangulate import triangulate

# Constants
UPLOAD_FOLDER = 'uploads'
x = 3 # size of grid: width
y = 3 # size of grid: height
grid = [[1, 2, 3], [3, 2, 3], [2, 3, 1]]
tdelta = 5.0 # refresh delay
# for i in range(y):
# 	grid.append([])

# App initialization
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Sound sample
class Sound:
	def __init__(vol = 0, direc = 0, time = 0):
		self.vol = vol
		self.dir = direc
		self.time = time

# Info at one coordinate
# class Square:
# 	def __init__(level = 0):
# 		self.level = level

# Run a function periodically
def refresh(f, delay):
	t = Timer(delay, f)
	t.start()

# Upload
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(UPLOAD_FOLDER, f.filename))
	return redirect(url_for(index))

# Print info to console
def printGrid():
	global tdelta, x, y, grid
	for i in range(x):
		for j in range(y):
			print(grid[i][j], end=' ')
		print()
	refresh(printGrid, tdelta)

# Home
@app.route('/', methods = ['GET', 'POST'])
def index():
	printGrid()
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
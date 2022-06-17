from random import randint
from enum import Enum
from matplotlib import pyplot as plt
from matplotlib import patches

class MAP_ENTRY_TYPE(Enum):
	MAP_EMPTY = 0,
	MAP_BLOCK = 1,

class WALL_DIRECTION(Enum):
	WALL_LEFT = 0,
	WALL_UP = 1,
	WALL_RIGHT = 2,
	WALL_DOWN = 3,

class Map():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.maze = [[0 for x in range(self.width)] for y in range(self.height)]
	
	def setMap(self, x, y, value):
		if value == MAP_ENTRY_TYPE.MAP_EMPTY:
			self.maze[y][x] = 0
		elif value == MAP_ENTRY_TYPE.MAP_BLOCK:
			self.maze[y][x] = 1
	
	def isMovable(self, x, y):
		return self.maze[y][x] != 1
	
	def isValid(self, x, y):
		if x < 0 or x >= self.width or y < 0 or y >= self.height:
			return False
		return True

    
	def showMap(self, scale):
		def drawGrid(x, y):
			ax.add_patch(
				patches.Rectangle(
					(x, y),
					1 / scale,
					1 / scale,
					facecolor ='white'
				)
			)
		for row in range(len(self.maze)):
			for col in range(len(self.maze[row])):
				if self.maze[row][col] == 0:
					drawGrid(row * (1 / scale), col * (1 / scale))

# recursive division algorithm
def recursiveDivision(maze, x, y, width, height, wall_value):
	# start must be a odd number, wall_index must be a even number
	def getWallIndex(start, length):
		assert length >= 3
		wall_index = randint(start + 1, start + length - 2)
		if wall_index % 2 == 1:
			wall_index -= 1
		return wall_index
	
	# must check adjacent entry of four margin entries, 
	# if adjacent entry is movable, must set the margin entry as the hole
	def generateHoles(maze, x, y, width, height, wall_x, wall_y):
		holes = []
		
		hole_entrys = [(randint(x, wall_x -1), wall_y), (randint(wall_x + 1, x + width -1), wall_y),
						(wall_x, randint(y, wall_y -1)), (wall_x, randint(wall_y + 1, y + height - 1))]
		margin_entrys = [(x, wall_y), (x+width-1, wall_y), (wall_x, y), (wall_x, y + height-1)]
		adjacent_entrys = [(x-1, wall_y), (x+width, wall_y), (wall_x, y - 1), (wall_x, y + height)]
		for i in range(4):
			adj_x, adj_y = (adjacent_entrys[i][0], adjacent_entrys[i][1])
			if maze.isValid(adj_x, adj_y) and maze.isMovable(adj_x, adj_y):
				maze.setMap(margin_entrys[i][0], margin_entrys[i][1], MAP_ENTRY_TYPE.MAP_EMPTY)
			else:
				holes.append(hole_entrys[i])

		ignore_hole = randint(0, len(holes)-1)
		for i in range(0, len(holes)):
			if i != ignore_hole:
				maze.setMap(holes[i][0], holes[i][1], MAP_ENTRY_TYPE.MAP_EMPTY)

	if width <= 1 or height <= 1:
		return
	
	#generate a row and a column wall index, they must be even number
	wall_x, wall_y = (getWallIndex(x, width), getWallIndex(y, height))
	
	#set horizontal and vertical lines to wall
	for i in range(x, x+width):
		maze.setMap(i, wall_y, wall_value)
	for i in range(y, y+height):
		maze.setMap(wall_x, i, wall_value)
	
	#create three holes
	generateHoles(maze, x, y, width, height, wall_x, wall_y)
	
	recursiveDivision(maze, x, y, wall_x - x, wall_y - y, wall_value)
	recursiveDivision(maze, x, wall_y + 1, wall_x - x, y + height - wall_y -1, wall_value)
	recursiveDivision(maze, wall_x + 1, y, x + width - wall_x -1, wall_y - y, wall_value)
	recursiveDivision(maze, wall_x + 1, wall_y + 1, x + width - wall_x -1, y + height - wall_y -1, wall_value)

def doRecursiveDivision(maze):
	# draw four margin wall lines
	for x in range(0, maze.width):
		maze.setMap(x, 0, MAP_ENTRY_TYPE.MAP_BLOCK)
		maze.setMap(x, maze.height-1, MAP_ENTRY_TYPE.MAP_BLOCK)
	
	for y in range(0, maze.height):
		maze.setMap(0, y, MAP_ENTRY_TYPE.MAP_BLOCK)
		maze.setMap(maze.width-1, y, MAP_ENTRY_TYPE.MAP_BLOCK)
		
	recursiveDivision(maze, 1, 1, maze.width - 2, maze.height - 2, MAP_ENTRY_TYPE.MAP_BLOCK)

	
if __name__ == "__main__":
    scale = 201
    plt.rcParams['axes.facecolor']='black'
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    maze = Map(scale, scale)
    doRecursiveDivision(maze)
    maze.showMap(scale)
    plt.show()

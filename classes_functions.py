from ast import literal_eval as make_tuple
import pygame as pg
import random
import time
from items import *

bullet_vel = 20
player_size = 10
enemy_vel = 5
display_heighth = 600
display_width = 800

class player:
	def __init__(self, char_x, char_y, radius, win_):
		self.top = char_y - radius
		self.left = char_x - radius
		self.width = radius*2
		self.heigth = radius*2
		self.win = win_
		self.heldweapons = [0]
		self.currentweapon = self.heldweapons[0]
		self.ammunition = [14,0] #Len() = No. of weapons
	def draw(self):
		pg.draw.circle(self.win, (0,255,0), (self.left + int((self.width)/2), self.top + int((self.width)/2)), int((self.width)/2))

	def debug_draw(self):
		pg.draw.line(self.win, (255,0,0), (self.left, self.top), (self.left, self.top + self.heigth), 1)
		pg.draw.line(self.win, (255,0,0), (self.left, self.top + self.heigth), (self.left + self.width, self.top + self.heigth), 1)
		pg.draw.line(self.win, (255,0,0), (self.left + self.width, self.top + self.heigth), (self.left + self.width, self.top), 1)
		pg.draw.line(self.win, (255,0,0), (self.left, self.top), (self.left + self.width, self.top), 1)

	def next_weapon(self):
		if self.heldweapons.index(self.currentweapon) != len(self.heldweapons)-1:
			self.currentweapon = self.heldweapons[self.heldweapons.index(self.currentweapon)+1]

	def previous_weapon(self):
		if self.heldweapons.index(self.currentweapon) != 0:
			self.currentweapon = self.heldweapons[self.heldweapons.index(self.currentweapon)-1]
	


class bullet:
	def __init__(self, char_x, char_y, x_step_, y_step_, win_):
		self.left = char_x - 2
		self.top = char_y - 2
		self.x_step = x_step_
		self.y_step = y_step_
		self.width = 4
		self.heigth = 4
		self.win = win_
		pg.draw.circle(win_, (0,0,0), (char_x, char_y), int((self.width)/2))

	def move(self):
		self.top += self.y_step
		self.left += self.x_step
		pg.draw.circle(self.win, (0,0,0), (self.left + 2, self.top + 2), 2)

class wall:

	"""docstring for Wall"""
	def __init__(self, position, win_) :
		self.left = position[0]
		self.top = position[1]
		self.width = position[2]
		self.heigth = position[3]
		self.win = win_
	def draw(self):
		pg.draw.rect(self.win, (0,0,200), (self.left, self.top, self.width, self.heigth))

class enemy(player):
	"""docstring for enemy"""
	def __init__(self, position, win_):
		self.left = position[0] - player_size
		self.top = position[1] - player_size
		self.width = player_size*2
		self.heigth = self.width
		self.horizontal_walk = position[2]
		self.direction = position[3]
		self.colour = random.randrange(82, 255)
		self.win = win_
		self.draw()
	def draw(self):
		pg.draw.circle(self.win, (self.colour,0,0), (self.left + player_size, self.top + player_size), player_size)

	def debug_draw(self):
		super().debug_draw()

	def walk(self):
		if(self.horizontal_walk == 1):
			if(self.direction == 1):
				self.left += enemy_vel
			else:
				self.left -= enemy_vel
		else:
			if(self.direction == 1):
				self.top += enemy_vel
			else:
				self.top -= enemy_vel

	def change_direction(self):
		if(self.direction == 1):
			self.direction = 0
		else:
			self.direction = 1
class mouse:
	left = 0
	top = 0

class zone(wall):
	"""docstring for zone"""
	def __init__(self, position, win_):
		super().__init__(position, win_)

	def draw(self):
		pg.draw.rect(self.win, (255, 0, 255), (self.left, self.top, self.width, self.heigth))
		
		
#object_1 should be a wall
#object_2 should be bullet, enemy or player
def check_colission(object_1, object_2):
	if((object_1.left <= object_2.left + (object_2.width)) and (object_1.left + object_1.width >= object_2.left) and (object_1.top <= object_2.top + object_2.heigth) and (object_1.top + object_1.heigth >= object_2.top)):
		return True
	else:
		return False

def check_wall_colission(object_):
	if(object_.left + object_.width > display_width or object_.left < 0 or object_.top + object_.heigth > display_heighth or object_.top < 0):
		return True
	else:
		return False

def map_objects_init(win):
	map_objects = []
	mode = 0
	file = open("map_01.txt", "r")
	for line in file:
		if(line =="---wall---\n"):
			mode = 1

		if(line == "---enemy---\n"):
			mode = 2

		if(line == "---zone---\n"):
			mode = 3

		if(line == "---shotgun-item---\n"):
			mode = 4

		if(line == "---pistol-item---\n"):
			mode = 5

		if(mode == 1 and line != "---wall---\n"):
			map_objects.append(wall(make_tuple(line), win))

		if(mode == 2 and line != "---enemy---\n"):
			map_objects.append(enemy(make_tuple(line), win))

		if(mode == 3 and line != "---zone---\n"):
			map_objects.append(zone(make_tuple(line),win))

		if(mode == 4 and line != "---shotgun-item---\n"):
			map_objects.append(shotgunItem(make_tuple(line),win))

		if(mode == 5 and line != "---pistol-item---\n"):
			map_objects.append(pistolItem(make_tuple(line),win))
	return map_objects

def coordinates_to_wall(a,b):
	if((a[0]-b[0])==0):
		if((a[1]-b[1])==-1):
			return((a[0]*100,(a[1]+1)*100,100,20))
		else:
			return((a[0]*100,a[1]*100,100,20))
	else:
		if((a[0]-b[0])==-1):
			return(((a[0]+1)*100,a[1]*100,20,100))
		else:
			return((a[0]*100,a[1]*100,20,100))

def create_map_broadsearch(win):
	#file = open("map_01.txt", "rw")
	map_objects = []

	w, h = pg.display.get_surface().get_size()

	square_a = 100

	amount_horizontal_squares = int(w / square_a)
	amount_vertical_squares = int(h / square_a)

	all_squares = amount_vertical_squares * amount_horizontal_squares

	vertex_list = []
	walls = []
	for i in range(0, amount_vertical_squares):
		for j in range(0, amount_horizontal_squares):
			vertex = [[j,i], [], False, None]
			if j != amount_horizontal_squares - 1:
				vertex[1].append([j+1,i])#
				if(((j+1)*100,i*100,20,100) not in walls):
					walls.append(((j+1)*100,i*100,20,100))
			if j != 0:
				vertex[1].append([j-1,i])
				if(((j*100),i*100,20,100) not in walls):
					walls.append((j*100,i*100,20,100))

			if i != 0:
				#[0] is Position [1] is neighbors
				vertex[1].append([j,i-1])
				if((j*100,i*100,100,20) not in walls):
					walls.append((j*100,i*100,100,20))
			if i != amount_vertical_squares-1:
				#[0] is Position [1] is neighbors
				vertex[1].append([j,i+1])
				if((j*100,(i+1)*100,120,20) not in walls):
					walls.append((j*100,(i+1)*100,100,20))

			vertex_list.append(vertex)

	queue = []
	queue.insert(0,vertex_list[0])
	last = None
	while len(queue) != 0:
		c = queue.pop()

		#print(c)
		if(c[2] == False):
			c[2] = True
			random.shuffle(c[1])
			for adjacent in c[1]:
				for x in vertex_list:
					if(x[0] == adjacent and x[2] == False):
						x[3] = c[0]
						queue.append(x)
			if(c[3]!= None):
				if(coordinates_to_wall(c[0],c[3]) in walls):
					walls.remove(coordinates_to_wall(c[0],c[3]))


	items_coords =[[0,0],[0,1],[1,0],[amount_horizontal_squares-1,amount_vertical_squares-1]]

	#enemys and items
	for y in range(0,10):
		placed = False
		while(placed==False):
			x_cor=random.randint(0,amount_horizontal_squares-1)
			y_cor=random.randint(0,amount_vertical_squares-1)
			if([x_cor,y_cor] not in items_coords):
				placed=True
				items_coords.append([x_cor,y_cor])
				if(y<5):
					map_objects.append(enemy(((x_cor*100)+50,(y_cor*100)+50, random.randint(0,1),random.randint(0,1)), win))
				if(5<=y and y<8):
					map_objects.append(pistolItem(((x_cor*100)+50,(y_cor*100)+50, 10),win))
				if(8<=y):
					map_objects.append(shotgunItem(((x_cor*100)+50,(y_cor*100)+50, 10),win))
				

			#else:
				#print([x_cor,y_cor])

	for x in walls:
		map_objects.append(wall(x,win))
	map_objects.append(zone((720,520,80,80),win))
	return map_objects



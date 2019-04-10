from ast import literal_eval as make_tuple
import pygame as pg
import random

bullet_vel = 20
player_size = 10
enemy_vel = 5
display_heighth = 360
display_width = 640

class player:
	def __init__(self, char_x, char_y, radius, win_):
		self.top = char_y - radius
		self.left = char_x - radius
		self.width = radius*2
		self.heigth = radius*2
		self.win = win_
	def draw(self):
		pg.draw.circle(self.win, (0,255,0), (self.left + int((self.width)/2), self.top + int((self.width)/2)), int((self.width)/2))

	def debug_draw(self):
		pg.draw.line(self.win, (255,0,0), (self.left, self.top), (self.left, self.top + self.heigth), 1)
		pg.draw.line(self.win, (255,0,0), (self.left, self.top + self.heigth), (self.left + self.width, self.top + self.heigth), 1)
		pg.draw.line(self.win, (255,0,0), (self.left + self.width, self.top + self.heigth), (self.left + self.width, self.top), 1)
		pg.draw.line(self.win, (255,0,0), (self.left, self.top), (self.left + self.width, self.top), 1)


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
		self.draw()
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

		if(mode == 1 and line != "---wall---\n"):
			map_objects.append(wall(make_tuple(line), win))

		if(mode == 2 and line != "---enemy---\n"):
			print(make_tuple(line))
			map_objects.append(enemy(make_tuple(line), win))
			print(make_tuple(line)[0])
			print(line)
	return map_objects

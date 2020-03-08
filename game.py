import pygame as pg
import math
import random
from classes_functions import *
from weapons import *

pg.init()

game_points = 0
display_heighth = 600
display_width = 800
bullets = []
vel = 5
x = 30
y = 30
bullet_vel = 20

no_d = False 
no_w = False 
no_s = False
no_a = False
walloffset = 7
enemy_vel = 5

win = pg.display.set_mode((display_width, display_heighth))

pg.display.set_caption("Hotline Berlin")





#Map-init
player_radius = 10
player_start_x = 30
player_start_y = 30
player_object = player(player_start_x, player_start_y, player_radius, win)
map_objects = map_objects_init(win)

pg.mouse.set_cursor(*pg.cursors.broken_x)


font = pg.font.SysFont("comicsansms", 24)


running_game = True
running = True

while running:
	keys = pg.key.get_pressed()
	pg.time.delay(20)
	all_events = pg.event.get()
	for event in all_events:
		if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
		  running = False

		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				shootweapon(player_object, bullet_vel, bullets, win)
				game_points -= 50
			if event.button == 4:
				player_object.next_weapon()
			if event.button == 5:
				player_object.previous_weapon()


	
	win.fill((255,255,255))

	for object_ in map_objects:
#		if(((wall.left < player_size + x) and (wall.left + wall.width > x- player_size)) and ((wall.top < y + player_size) and (wall.top + wall.heigth > y - player_size))):
#			print("X,Y Crossover")

#		else:
#			print("No Crossover")
		# if(((object_.top <= y + player_size) and (object_.top + object_.heigth + walloffset >= y - player_size)) and (object_.left >= x + player_size and object_.left - walloffset <= x + player_size)):
		# 	no_d = True
			
		# if((object_.left - walloffset < player_size + x) and (object_.left + object_.width + walloffset > x- player_size) and (object_.top >= y + player_size and object_.top - walloffset <= y + player_size)):
		# 	no_s = True

		# if((object_.left - walloffset < player_size + x) and (object_.left + object_.width + walloffset > x- player_size) and (object_.top + object_. heigth <= y - player_size and object_.top + object_.heigth + walloffset >= y - player_size)):
		# 	no_w = True

		# if(((object_.top <= y + player_size) and (object_.top + object_.heigth+ walloffset >= y - player_size)) and (object_.left + object_.width <= x - player_size and object_.left + object_.width + walloffset >= x - player_size)):
		# 	no_a = True
		if(type(object_) is not zone):
			if((object_.top <= player_object.top + player_object.heigth) and (object_.top + object_.heigth >= player_object.top) and (object_.left == player_object.left + player_object.width)):
				no_d = True
				
			if((object_.top <= player_object.top + player_object.heigth) and (object_.top + object_.heigth >= player_object.top) and (object_.left + object_.width == player_object.left)):
				no_a = True

			if((object_.left <= player_object.left + player_object.width) and (object_.left + object_.width >= player_object.left) and (object_.top + object_.heigth == player_object.top)):
				no_w = True

			if((object_.left <= player_object.left + player_object.width) and (object_.left + object_.width >= player_object.left) and (object_.top == player_object.top + player_object.heigth)):
				no_s = True


		object_.draw()
		if(type(object_) is enemy):
			object_.debug_draw()
			object_.walk()
			for object_to_compare in map_objects:
				if(object_ != object_to_compare and type(object_to_compare) is not zone):
					if(check_colission(object_, object_to_compare) or check_wall_colission(object_)):
						object_.change_direction()
						break

			if(check_colission(object_, player_object)):
				game_points = 0
				player_object.top = player_start_y - player_radius
				player_object.left = player_start_x - player_radius
				map_objects = map_objects_init(win)

		if(type(object_) is zone):
			if(check_colission(object_, player_object)):
				game_points += 500
				player_object.top = player_start_y - player_radius
				player_object.left = player_start_x - player_radius
				map_objects = map_objects_init(win)
					






	if(keys[pg.K_w] and player_object.top - vel >= 0):
		if(no_w == False):
			player_object.top -= vel

	if(keys[pg.K_s] and player_object.top + vel + player_object.heigth<= display_heighth):
		if(no_s == False):
			player_object.top += vel

	if(keys[pg.K_a] and player_object.left - vel >= 0):
		if(no_a == False):
			player_object.left -= vel

	if(keys[pg.K_d] and player_object.left + vel + player_object.width<= display_width):
		if(no_d == False):
			player_object.left += vel

	no_d = False 
	no_w = False 
	no_s = False
	no_a = False
		



	for bullet_ in bullets:
		bullet_.move()
		for object_ in map_objects:
			if(check_colission(object_, bullet_) or check_wall_colission(bullet_)):
				bullets.remove(bullet_)
				#print(type(object_))
				if(type(object_) is enemy):
					map_objects.remove(object_)
					game_points += 100
				break
				
	#TODO create displayPoints()
	game_points_text = font.render(str(game_points), True, (0, 0, 0))
	win.blit(game_points_text, (display_width - game_points_text.get_width(), 0))


	player_object.draw()
	displayCurrentWeapon(player_object, win)
	pg.display.update()


pg.display.quit()
pg.quit()
exit(0)
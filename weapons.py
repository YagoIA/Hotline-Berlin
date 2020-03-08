import math
import pygame as pg
from classes_functions import *
from time import *
lastShot = [0,0]


def displayCurrentWeapon(player_object, win, font):
    w, h = pg.display.get_surface().get_size()

    #Display Ammunition for current weapon
    ammunution_text = font.render(str(player_object.ammunition[player_object.currentweapon]), True, (0, 0, 0))
    win.blit(ammunution_text, (w - ammunution_text.get_width(), 65))


    if(player_object.currentweapon == 0):


        pistolImg = pg.image.load('assets/pistol.png')
        pistolImgScaled = pg.transform.scale(pistolImg, (40, 40))
        win.blit(pistolImgScaled, (w - (w / 20), 25))

    if (player_object.currentweapon == 1):
        shotgunImg = pg.image.load('assets/shotgun.png')
        shotgunImgScaled = pg.transform.scale(shotgunImg, (40, 40))
        win.blit(shotgunImgScaled, (w - (w / 20), 25))


def shootweapon(player_object, bullet_vel, bullets, audio_enabled, weapon_sounds, win):
    if player_object.currentweapon == 0:

        if (player_object.ammunition[0] > 0 and ((time() - lastShot[0]) * 1000) > 200) or lastShot[0] == 0:

            if (audio_enabled == True):
                weapon_sounds[0].play()

            player_object.ammunition[0] = player_object.ammunition[0]-1

            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            hypotenuse = math.sqrt(math.pow(player_object.left + int(player_object.width / 2) - mouse_x, 2) + math.pow(
                player_object.top + int(player_object.width / 2) - mouse_y, 2))
            winkel = -(math.asin((player_object.top + int(player_object.width / 2) - mouse_y) / hypotenuse))

            if (player_object.left - mouse_x > 0):
                bullet_x_step = -int(math.cos(winkel) * bullet_vel)

            else:
                bullet_x_step = int(math.cos(winkel) * bullet_vel)

            bullet_y_step = int(math.sin(winkel) * bullet_vel)

            bullets.append(
                bullet(player_object.left + int(player_object.width / 2), player_object.top + int(player_object.width / 2),
                       bullet_x_step, bullet_y_step, win))
            lastShot[0] = time()
            return True
        else:
            return False
    if player_object.currentweapon == 1:
        if (player_object.ammunition[1] > 0 and ((time() - lastShot[1]) * 1000) > 1180) or lastShot[1] == 0:

            if(audio_enabled== True):
                weapon_sounds[1].play()

            player_object.ammunition[1] = player_object.ammunition[1]-1
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            hypotenuse = math.sqrt(math.pow(player_object.left + int(player_object.width / 2) - mouse_x, 2) + math.pow(
                player_object.top + int(player_object.width / 2) - mouse_y, 2))
            winkel = -(math.asin((player_object.top + int(player_object.width / 2) - mouse_y) / hypotenuse))

            if (player_object.left - mouse_x > 0):
                bullet_x_step1 = -int(math.cos(winkel) * bullet_vel)
                bullet_x_step2 = -int(math.cos(winkel-(10*(math.pi/180))) * bullet_vel)
                bullet_x_step3 = -int(math.cos(winkel+(10*(math.pi/180))) * bullet_vel)

            else:
                bullet_x_step1 = int(math.cos(winkel) * bullet_vel)
                bullet_x_step2 = int(math.cos(winkel-(10*(math.pi/180))) * bullet_vel)
                bullet_x_step3 = int(math.cos(winkel+(10*(math.pi/180))) * bullet_vel)

            bullet_y_step1 = int(math.sin(winkel) * bullet_vel)
            bullet_y_step2 = int(math.sin(winkel-(10*(math.pi/180))) * bullet_vel)
            bullet_y_step3 = int(math.sin(winkel+(10*(math.pi/180))) * bullet_vel)

            bullets.append(
                bullet(player_object.left + int(player_object.width / 2), player_object.top + int(player_object.width / 2),
                       bullet_x_step1, bullet_y_step1, win))
            bullets.append(
                bullet(player_object.left + int(player_object.width / 2), player_object.top + int(player_object.width / 2),
                       bullet_x_step2, bullet_y_step2, win))
            bullets.append(
                bullet(player_object.left + int(player_object.width / 2), player_object.top + int(player_object.width / 2),
                       bullet_x_step3, bullet_y_step3, win))
            lastShot[1] = time()
            return True
        else:
            return False



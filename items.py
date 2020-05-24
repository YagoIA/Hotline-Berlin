import pygame as pg
from math import sqrt, floor


class Item:
    def __init__(self, position, win_):
        self.left = position[0]
        self.top =  position[1] 
        self.width = position[2] *2
        self.heigth = position[2] *2
        self.win = win_

    def draw(self):
        pg.draw.circle(self.win, (255, 153, 102), (self.left + int((self.width ) /2), self.top + int((self.width ) /2)), int((self.width ) /2))

    def debug_draw(self):
        pg.draw.line(self.win, (255 ,0 ,0), (self.left, self.top), (self.left, self.top + self.heigth), 1)
        pg.draw.line(self.win, (255 ,0 ,0), (self.left, self.top + self.heigth), (self.left + self.width, self.top + self.heigth), 1)
        pg.draw.line(self.win, (255 ,0 ,0), (self.left + self.width, self.top + self.heigth), (self.left + self.width, self.top), 1)
        pg.draw.line(self.win, (255 ,0 ,0), (self.left, self.top), (self.left + self.width, self.top), 1)

    def pickup(self, player_object, beepSound, audio_enabled):
        print("Picked up Item: ", end='')
        if audio_enabled == True:
            beepSound.play()


class shotgunItem(Item):
    def __init__(self, position, win_):
        super().__init__(position, win_)

    def draw(self):
        super().draw()

        shotgunImgScaled = pg.transform.scale(pg.image.load('assets/shotgun.png'), (floor(self.width/sqrt(2)), floor(self.width/sqrt(2))))
        self.win.blit(shotgunImgScaled, (self.left+(floor(self.width/sqrt(2)/4)), self.top+(floor(self.width/sqrt(2)/4))))

    def pickup(self, player_object, beepSound, audio_enabled):
        super().pickup(player_object, beepSound, audio_enabled)
        print("shotgun")
        if 1 not in player_object.heldweapons:
            player_object.heldweapons.append(1)
            player_object.heldweapons.sort()
            player_object.currentweapon = 1
        player_object.ammunition[1] += 2



class pistolItem(Item):
    def __init__(self, position, win_):
        super().__init__(position, win_)

    def draw(self):
        super().draw()

        pistolImgScaled = pg.transform.scale(pg.image.load('assets/pistol.png'), (floor(self.width/sqrt(2)), floor(self.width/sqrt(2))))
        self.win.blit(pistolImgScaled, (self.left+(floor(self.width/sqrt(2)/4)), self.top+(floor(self.width/sqrt(2)/4))))

    def pickup(self, player_object, beepSound, audio_enabled):
        super().pickup(player_object,beepSound, audio_enabled)
        print("pistol")
        if 0 not in player_object.heldweapons:
            player_object.heldweapons.append(0)
            player_object.heldweapons.sort()
        player_object.ammunition[0] += 7


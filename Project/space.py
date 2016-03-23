""" 
Sergio Avila

In this program I will implement a versin of the  game space invaders
for Game Development class. In this game there will be a main ship where 
it will be able to shoot bullets to other smaller space ships.

This project will be done in python and 
it will be ran through the terminal/command prompt.

For this program to run you will have to have python installed
in your computer. However, if you use ubuntu python comes 
already installed.
Also you will need to install the pygame library from pygame.org

How to run it:
First go to your folder where search.py is in.
For example: cd /Game-Dev/Project$ 
once you are there you simply type:
python search.py
"""

""" 
(this is just for my notes, and will be deleted later on)
Brainstorm:

Right off the bat I know that we are going to need a few classes
Possible classes
	-main ship or mother ship
	-small ships/enemies
	-maybe a few bigger enemies (possible)
	-bullets might only be a function or maybe a whole class

"""
#import pygame
from pygame import *
import sys
from random import shuffle
from random import randrange, choice

#// globals

SCREEN = display.set_mode((800,600))
PicName = ["motherShip"]
pictures = {name: image.load("images/{}.png".format(name)).convert_alpha() for name in PicName}




class MotherShip(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = pictures["motherShip"]
		self.rect = self.image.get_rect(topleft=(375,540))
		self.speed = 5

	def update(self, keys, *args):
		if keys[K_LEFT] and self.rect.x > 10:
			self.rect.x -= self.speed
		if keys[K_RIGHT] and self.rect.x < 750:
			self.rect.x += self.speed

		game.screen.blit(self.image, self.rect)

# // not done with this class 
class StartGame(object):
	def __init__(self):
		self.screen = display.set_mode(800,600)
		self.background = image.load('images/space.jpg').convert()
#class enemies():

#class biggerEnemies():



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
import pygame
from pygame import *
import sys

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
		if keys[K_RIGHT] and self.rect.x < 740:
			self.rect.x += self.speed

		game.screen.blit(self.image, self.rect)

class Bullet(sprite.Sprite):
	def __init__(self, xpos, ypos, direction, speed, filename, side):
		sprite.Sprite.__init__(self)
		self.image = pictures[filename]
		self.rect = self.image.get_rect(topleft=(xpos, ypos))
		self.speed = speed
		self.direction = direction
		self.side = side
		self.filename = filename


	def update(self, keys, *args):
		game.screen.blit(self.image, self.rect)
		self.rect.y += self.speed * self.direction
		if self.rect.y < 15 or self.rect.y > 600:
			self.kill()

class block(sprite.Sprite):

	def update(self, keys, *args):
		game.screen.blit(self.image, self.rect)

# // not done with this class 
class StartGame(object):
	def __init__(self):
		#init()
		self.screen = SCREEN
		self.background = image.load('images/space.jpg').convert()
		self.startGame = False
		self.mainScreen = True
		self.gameOver = False

	def reset(self, score, lives):
		self.player = MotherShip()

	def main(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
			if self.mainScreen:
				self.reset(0,3)
				self.screen.blit(self.background, (0,0))
			#elif self.startGame:
				#currentTime = time.get_ticks()

			display.update()
		pygame.quit ()


if __name__ == '__main__':
	game = StartGame()
	game.main()

#class enemies():

#class biggerEnemies():


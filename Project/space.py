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
PICNAME = ["motherShip","bullet", "enemy_A", "enemy_B", "enemy_C", "explosion_all", "boss_fight"]
PICTURES = {name: image.load("images/{}.png".format(name)).convert_alpha() for name in PICNAME}




class MotherShip(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = PICTURES["motherShip"]
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
		self.image = PICTURES[filename]
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

#block = blocker
class block(sprite.Sprite):

	def __init__(self,size,color, row, column):
		sprite.Sprite.__init__(self)
		self.height = size
		self.width = size
		self.color = color
		self.image = Surface((self.width, self.height))
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.row = row
		self.column = column

	def update(self, keys, *args):
		game.screen.blit(self.image, self.rect)

#class Mystery(sprite.Sprite): == class boss_fight(sprite.Sprite)
# Collisions is the same as "class Explosion"
class Collision(sprite.Sprite):
	#x = xpos,   y = ypos
	def __init__(self, x, y, row, ship, mystery, score):
		sprite.Sprite.__init__(self)
		self.isMothership = ship
		self.isMystery = mystery
		if mystery:
			self.text = Text(FONT, 20, str(score), WHITE, x+20, y+6)
		elif ship:
			self.image = PICTURES["motherShip"]
			self.rect = self.image.get_rect(topleft=(x,y))
		else:
			self.row = row
			self.load_image()
			self.image = transform.scale(self.image, (40, 35))
			self.rect = self.image.get_rect(topleft=(x,y))
			game.screen.blit(self.image, self.rect)

		self.timer = time.get_ticks()

	def update(self, keys, currentTime):
		if self.isMothership:
			if currentTime - self.timer > 300 and currentTime - self.timer <= 600:
				game.screen.blit(self.image, self.rect)
			if currentTime - self.timer > 900:
				self.kill()

		else:
			if currentTime - self.timer <= 100:
				game.screen.blit(self.image, self.rect)
			if currentTime - self.timer > 100 and currentTime - self.timer <= 200:
				self.image - transform.scale(self.image, (50, 45))
				game.screen.blit(self.image, (self.rect.x-6, self.rect.y-6))
			if currentTime - self.timer > 400:
				self.kill()

	def load_image(self):
		imgColors = ["_all"]
		self.image = PICTURES["explosion{}".format(imgColors[self.row])]

		

class Enemies(sprite.Sprite):

	def __init__(self, row, column):
		sprite.Sprite.__init__(self)
		self.row = row
		self.column = column
		self.images = []
		self.load_images()
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.direction = 1
		self.leftMoves = 30
		self.rightMoves = 15
		self.moveTime = 600
		self.moveNumber = 0
		self.firstTime = True
		self.movedY = False
		self.columns = [False] * 10
		self.aliveColumns = [True] * 10
		self.addRightMoves = False
		self.addLeftMoves = False
		self.numOfRightMoves = 0
		self.numOfLeftMoves = 0
		self.timer = time.get_ticks()

		


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


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

	# need the mistery part in here
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

	def check_column_deletion(self, deadRow, deadColumn, deadArray):
		if deadRow != -1 and deadColumn != -1:
			deadArray[deadRow][deadColumn] = 1
			for column in range(10):
				if all([deadArray[row][column] == 1 for row in range(5)]):
					self.columns[column] = True

		for i in range(5):
			if all([self.columns[x] for x in range(i + 1)]) and self.aliveColumns[i]:
				self.leftMoves += 5
				self.aliveColumns[i] = False
				if self.direction == -1:
					self.rightMoves += 5
				else:
					self.addRightMoves = True
					self.addLeftMoves += 5

		for i in range(5):
			if all([self.columns[x] for x in range(9, 8 - i, -1)]) and self.aliveColumns[9 - i]:
				self.aliveColumns[9 - i] = False
				self.rightMoves += 5
				if self.direction == 1:
					self.leftMoves += 5
				else:
					self.addLeftMoves = True
					self.numOfLeftMoves += 5

	#deadRow, deadColumn, deadArray == killedRow...
	def update(self, keys, currentTime, deadRow, deadColumn, deadArray):
		self.check_column_deletion(deadRow, deadColumn, deadArray)
		if currentTime - self.timer > self.moveTime:
			self.movedY = False
			if self.moveNumber >= self.rightMoves and self.direction == -1:
				self.direction *= -1
				self.moveNumber = 0
				self.rect.y += 35
				self.movedY = True
				if self.addRightMoves:
					self.rightMoves += self.numOfRightMoves
				if self.firstTime:
					self.rightMoves = self.leftMoves
					self.firstTime = False
				self.addRightMovesAfterDrop = False
			if self.moveNumber >= self.leftMoves and self.direction == -1:
				self.direction *= -1
				self.moveNumber = 0
				self.rect.y += 35
				self.movedY = True
				if self.addLeftMoves:
					self.leftMoves += self.numOfLeftMoves
				self.addLeftMovesAfterDrop = False
			if self.moveNumber < self.rightMoves and self.direction == 1 and not self.movedY:
				self.rect.x += 10
				self.moveNumber += 1
			if self.moveNumber < self.leftMoves and self.direction == -1 and not self.movedY:
				self.rect.x -= 10
				self.moveNumber += 1

			self.index += 1
			if self.index >= len(self.images):
				self.index = 0
			self.image = self.images[self.index]

			self.timer += self.moveTime
		game.screen.blit(self.images, self.rect)

	def loadImages(self):
		images = {0: ["_A", "_A"],
				  1: ["_B", "_B"],
				  2: ["_C", "_C"],
				  3: ["_C", "_C"],
				  4: ["_A", "_A"],
				 }
		img1, img2 = (PICTURES["enemy{}".format(img_num)] for img_num in images[self.row])
		self.images.append(transform.scale(img1, (40, 35)))
		self.images.append(transform.scale(img2, (40, 35)))



# // not done with this class 
class StartGame(object):
	def __init__(self):
		#init()
		self.screen = SCREEN
		self.background = image.load('images/space.jpg').convert()
		self.startGame = False
		self.mainScreen = True
		self.gameOver = False
		self.enemyposition = 65

	def reset(self, score, lives):
		self.player = MotherShip()
		self.playerGroup = sprite.Group(self.player)
		self.explosionGroup = sprite.Group()
		self.mysteryShip = Mystery() #have to change this to boss fight or something
		self.mysteryGroup = sprite.Group(self.mysteryShip)
		self.enemyBullets = sprite.Group()
		self.reset_lives()
		self.make_enemies()
		self.allBlockers = sprite.Group(self.make_blockers(0), self.make_blockers(1), self.make_blockers(2), self.make_blockers(3))
		self.keys = key.get_pressed()
		self.clock = time.Clock()
		self.timer = time.get_ticks()
		self.noteTimer = time.get_ticks()
		self.shipTimer = time.get_ticks()
		self.score = score
		self.lives = lives
		self.create_audio()
		self.create_text()
		self.killedRow = -1
		self.killedColumn = -1
		self.makeNewShip = False
		self.shipAlive = True
		self.killedArray = [[0] * 10 for x in range(5)]



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


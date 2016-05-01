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
from pygame.locals import *
import sys
from random import shuffle, randrange, choice

#// globals

SCREEN = display.set_mode((800,600))
PICNAME = ["motherShip","bullet", "enemy_A", "enemy_B", "enemy_C", "explosion_all", "boss_fight"]
PICTURES = {name: image.load("images/{}.png".format(name)).convert_alpha() for name in PICNAME}

WHITE 	= (255, 255, 255)
GREEN 	= (78, 255, 87)
YELLOW 	= (241, 255, 0)
BLUE 	= (80, 255, 239)
PURPLE 	= (203, 0, 255)
RED 	= (237, 28, 36)
FONTS = "game-font-7/game_font_7.ttf"


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
	def __init__(self, x, y, direction, speed, filename, side):
		sprite.Sprite.__init__(self)
		self.image = PICTURES[filename]
		self.rect = self.image.get_rect(topleft=(x, y))
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
class boss_fight(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = PICTURES["boss_fight"]
		self.image = transform.scale(self.image, (75, 35))
		self.rect = self.image.get_rect(topleft=(-80, 45))
		self.row = 5
		self.moveTime = 25000
		self.direction = 1
		self.timer = time.get_ticks()

	def update(self, keys, currentTime, *args):
		resetTimer = False
		if (currentTime - self.timer > self.moveTime) and self.rect.x < 840 and self.direction == 1:
			self.rect.x += 2
			game.screen.blit(self.image, self.rect)
		if (currentTime - self.timer > self.moveTime) and self.rect.x > -100 and self.direction == -1:
			self.rect.x -= 2
			game.screen.blit(self.image, self.rect)
		if (self.rect.x > 830):
			self.direction = -1
		if (self.rect.x < -90):
			self.direction = 1
			resetTimer = True
		if (currentTime - self.timer > self.moveTime) and resetTimer:
			self.timer = currentTime
# Collisions is the same as "class Explosion"
class Collision(sprite.Sprite):
	def __init__(self, x, y, row, ship, boss, score):
		sprite.Sprite.__init__(self)
		self.isMothership = ship
		self.isBoss = boss
		if boss:
			self.text = Text(FONTS, 20, str(score), WHITE, x+20, y+6)
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
		if self.isBoss:
			if currentTime - self.timer <= 200:
				self.text.draw(game.screen)
			if currentTime - self.timer > 400 and currentTime - self.timer <= 600:
				self.text.draw(game.screen)
			if currentTime - self.timer > 600:
				self.kill()

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

	
class Text(object):
	def __init__(self, textFont, size, message, color, xpos, ypos):
		self.font = font.Font(textFont, size)
		self.surface = self.font.render(message, True, color)
		self.rect = self.surface.get_rect(topleft=(xpos, ypos))

	def draw(self, surface):
		surface.blit(self.surface, self.rect)

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


class LIVES(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = PICTURES["motherShip"]
		self.image = transform.scale(self.image, (23, 23))
		self.rect = self.image.get_rect(topleft=(x, y))
		
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
		self.enemyposition = 65

	def reset(self, score, lives):
		self.player = MotherShip()
		self.playerGroup = sprite.Group(self.player)
		self.explosionGroup = sprite.Group()
		self.bullets = sprite.Group()
		self.bossShip = boss_fight() #have to change this to boss fight or something
		self.bossGroup = sprite.Group(self.bossShip)
		self.enemyBullets = sprite.Group()
		self.make_lives()
		#self.make_enemies()
		#self.allBlockers = sprite.Group(self.make_blockers(0), self.make_blockers(1), self.make_blockers(2), self.make_blockers(3))
		self.keys = key.get_pressed()
		self.clock = time.Clock()
		self.timer = time.get_ticks()
		self.noteTimer = time.get_ticks()
		self.shipTimer = time.get_ticks()
		self.score = score
		self.lives = lives
		#self.create_audio()
		self.make_text()
		self.killedRow = -1
		self.killedColumn = -1
		self.makeNewShip = False
		self.shipAlive = True
		self.killedArray = [[0] * 10 for x in range(5)]


	def make_lives(self):
		self.life1 = LIVES(715, 3)
		self.life2 = LIVES(742, 3)
		self.life3 = LIVES(769, 3)
		self.life4 = LIVES(796, 3)
		self.life5 = LIVES(823, 3)
		self.livesGroup = sprite.Group(self.life1, self.life2, self.life3, self.life4, self.life5)

	def make_blockers(self, number):
	   blockerGroup = sprite.Group()
	   for row in range(4):
		   for column in range(9):
			   blocker = Blocker(10, GREEN, row, column)
			   blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
			   blocker.rect.y = 450 + (row * blocker.height)
			   blockerGroup.add(blocker)
	   return blockerGroup


	#create text is next
	def make_text(self):
		self.title = Text(FONTS, 50, "Game Dev Project", WHITE, 164, 155)
		self.gameOver = Text(FONTS, 50, "Game Over", WHITE, 250, 270)
		self.nextRound = Text(FONTS, 50, "Next Round", WHITE, 240, 270)
		self.enemyA = Text(FONTS, 25, "   =   10 pts", GREEN, 368, 270)
		self.enemyB = Text(FONTS, 25, "   =  20 pts", BLUE, 368, 320)
		self.enemyC = Text(FONTS, 25, "   =  30 pts", PURPLE, 368, 370)
		self.enemyBoss = Text(FONTS, 25, "   =  ?????", RED, 368, 420)
		self.score = Text(FONTS, 20, "Score", WHITE, 5, 5)
		self.lives = Text(FONTS, 20, "Lives ", WHITE, 640, 5)

	def userInput(self):
		self.keys = key.get_pressed()
		for i in event.get():
			if i.type == QUIT:
				sys.exit()
			if i.type == KEYDOWN:
				if i.key == K_SPACE:
					if len(self.bullets) == 0 and self.shipAlive:
						if self.score < 1000:
							bullet = Bullet(self.player.rect.x + 23, self.player.rect.y +5, -1, 15, "bullet", "center")
							self.bullets.add(bullet)
							self.allSprites.add(self.bullets)
						else:
							leftbullet = Bullet(self.player.rect.x + 8, self.player.rect.y + 5, -1, 15, "bullet", "left")
							rightbullet = Bullet(self.player.rect.c + 38, self.player.rect.y + 5, -1, 15, "bullet", "right")
							self.bullets.add(leftbullet)
							self.bullets.add(rightbullet)
							self.allSprites.add(self.bullets)




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


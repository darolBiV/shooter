#Создай собственный Шутер!
from pygame  import * 
from random import *
from time import sleep
win_width = 700
win_height = 500 
lost=0
kill=0
pyl=0
window = display.set_mode((win_width,win_height))
display.set_caption('SHOOTER')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
clock = time.Clock()
FPS = 120
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
font.init()
font1=font.SysFont('Arial',24)
font2=font.SysFont('Arial',36)
t1 = font1.render('Счёт:'+str(kill),True,(255,255,255))
t2 = font1.render('Пропущено:'+str(lost),True,(255,255,255))
t3 = font2.render('Ты лох:',True,(255,255,255))
t4 = font2.render('МЕГАХАРОШ',True,(200,222,0))
t5 = font1.render('Пули:'+str(lost),True,(255,255,255))
t6 = font2.render('Косой',True,(200,222,0))
#########################################################
class GameSprite(sprite.Sprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__()
		self.height=height
		self.width=width
		self.speed = speed
		self.image = transform.scale(image.load(img),(self.width,self.height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	def reset(self):
		window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x>0:
			self.rect.x-=self.speed
		elif keys[K_RIGHT] and self.rect.x+self.width<win_width:
			self.rect.x+=self.speed
	def fire(self):
		global pyl,t5
		bullet =Bullet('bullet.png',self.rect.x+35,self.rect.y,3,20,20)
		bullets.add(bullet)
		pyl+=1
		t5 = font1.render('Пули:'+str(pyl),True,(255,255,255))

class UFO(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		global lost,t2
		self.rect.y+=self.speed
		if self.rect.y>=win_height:
			self.rect.y = 0
			self.rect.x = randint(0 , win_width-self.width)
			lost+=1
			t2 = font1.render('Пропущено:'+str(lost),True,(255,255,255))

			

class Bullet(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		self.rect.y-=self.speed
		if self.rect.y<=0:
			self.kill()
#########################################################



rocket = Player('rocket.png',win_width//2,win_height-80,4,80,80)
bullets = sprite.Group()
enemies = sprite.Group()
for i in range(5):
	enemy = UFO('ufo.png',randint(0,win_width-80),0,1,80,80)
	enemies.add(enemy)

while True:
	window.blit(background,(0,0))
	enemies.update()
	enemies.draw(window)
	bullets.update()
	bullets.draw(window)
	rocket.update()
	rocket.reset()
	window.blit(t1,(20,20))
	window.blit(t2,(20,50))
	window.blit(t5,(20,80))
	display.update()
	hits = sprite.groupcollide(bullets,enemies,True,True) 
	for i in hits:

		enemy = UFO('ufo.png',randint(0,win_width-80),0,1,80,80)
		enemies.add(enemy)
		t1 = font1.render('Счёт:'+str(kill),True,(255,255,255))
		kill+=1

	for i in event.get():
		if i.type==QUIT:
			quit()
		if lost>=5:
			sleep(1)
			window.blit(t3,(250,200))
			display.update()
			sleep(2)
			quit()
		if kill >= 100 :
			window.blit(t4,(300,200))
			display.update()
			sleep(2)
			quit()
		if pyl >= 400 :
			window.blit(t6,(300,200))
			display.update()
			sleep(2)
			quit()

		if i.type==MOUSEBUTTONDOWN:
			if i.button==5 or i.button==4:

				rocket.fire( )
				#у объекта rocket вызываем функцию fire()
	clock.tick(FPS)


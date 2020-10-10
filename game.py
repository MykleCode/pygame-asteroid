from engine.main import *
from game_classes import *
import random



class Game(Scene):
	def __init__(self,e):
		Scene.__init__(self,e)
		
		self.engine.change_physics(Physics(self,gravity=Vector2(0,0)))
		self.asteroid_img = pygame.image.load('asteroid.png')
		
		for i in range(200):
			color = (200,200,random.randint(150,255))
			StaticStar(e,color)
		
		self.asteroids = []
		for i in range(10):
			self.spawnAsteroid()
		
		self.player = Ship(e,e.XWIN/2,e.YWIN-40,35,30,RED)
		self.player.weapon = Weapon(self.player,(e,20,5,SKY),0.1,500)
	
	def spawnAsteroid(self):
		radius = random.randint(30,70)
		if not self.ready:
			self.asteroids+=[Asteroid(self.engine,0,0,radius,self.asteroid_img)]
		else:self.instanciate(Asteroid,self.engine,0,0,radius,self.asteroid_img)
		self.asteroids[-1].mass=int(radius/2)
	
	def onUpdateEnter(self):
		self.asteroids = [a for a in self.asteroids if a!=None]
		if len(self.asteroids)<10:self.spawn(Asteroid)
	
	def onEventStay(self,event):
		if event.type==KEYDOWN:
			if event.key == K_ESCAPE:self.engine.load_scene(Menu)

	
	
class Menu(Scene):
	def __init__(self,e):
		Scene.__init__(self,e)
		
		space = self.engine.applyY(100)
		title_size = self.engine.XWIN/15+self.engine.YWIN/15
		button_text_size = int(self.engine.XWIN/50+self.engine.YWIN/50)
		
		for i in range(300):
			color = (200,200,random.randint(150,255))
			MovingStar(e,color)
		
		self.title=TextSprite(self.engine,self.engine.XWIN/2.7,# X coords
			self.engine.applyY(100),					# Y coords
			title_size,									# Size
			WHITE,										# Color
			txt=self.engine.TITLE)						# String
		
		self.button_play = Button(self.engine,self.engine.XWIN/2,self.engine.YWIN/2,# X,Y coords
			self.engine.applyX(250),self.engine.applyY(70),				# Width, Height
			ALPHA,LIGHT_GRAY,													# Colors
			TextSprite(self.engine,self.engine.applyX(100),							# Text
				self.engine.applyY(80)/2,
				button_text_size,
				WHITE,txt="PLAY",auto=False))
		
		self.button_quit = Button(self.engine,self.engine.XWIN/2,self.engine.YWIN/2+space,# X,Y coords
			self.engine.applyX(250),self.engine.applyY(70),				# Width, Height
			ALPHA,LIGHT_GRAY,													# Colors
			TextSprite(self.engine,self.engine.applyX(100),							# Text
				self.engine.applyY(80)/2,
				button_text_size,
				WHITE,txt="QUIT",auto=False))
				
	
	def onUpdateEnter(self):
		if self.button_play.pressed:
			self.engine.load_scene(Game)
		if self.button_quit.pressed:
			self.engine.stop()
		


engine = Engine((1280,720),Menu,title="Asteroid")
engine.start()

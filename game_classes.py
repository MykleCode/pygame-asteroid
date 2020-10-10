from engine.engine_lib import *

from engine.sprite import Sprite
from engine.colors import *
from engine.physics import *
from engine.controller import *
from engine.colliders import *
from engine.object import *

import math,random


pygame.init()


class Block(Sprite,RectCollider):
	def __init__(self,engine,x,y,w,h,color,material=PhysicMaterial(),groups=[]):
		Sprite.__init__(self,engine,x,y,w,h,color,groups=groups,auto=False)
		RectCollider.__init__(self,engine,x,y,w,h,material=material)



class Asteroid(Sprite,RigidBody):
	def __init__(self,engine,x,y,r,color,material=PhysicMaterial(),groups=[]):
		Sprite.__init__(self,engine,x,y,r,r,color,groups=groups,auto=False)
		RigidBody.__init__(self,engine,x,y,r,r,1e5,material=material)
		
		self.velocity.x = random.randint(-200,200)
		self.velocity.y = random.randint(-200,200)
		
		self.rot_speed = random.random()*5
	
	def update(self):
		self.angle = (self.angle+self.rot_speed)%360
		
		self.pos.x = self.pos.x%self.engine.XWIN
		self.pos.y = self.pos.y%self.engine.YWIN
	



class Projectile(Sprite,KinematicBody):
	def __init__(self,engine,w,h,color,shooter,speed,groups=[]):
		self.shooter = shooter
		self.speed = speed
		
		x = math.cos(math.radians(shooter.angle))*(shooter.rect.width/2)+shooter.pos.x
		y = math.sin(math.radians(shooter.angle))*(shooter.rect.height/2)+shooter.pos.y
		Sprite.__init__(self,engine,x,y,w,h,color,groups=groups,auto=False)
		KinematicBody.__init__(self,engine,x,y,w,h)
		self.mass=1
		self.trigger = True
		self.angle = shooter.angle
		self.rotate()
		
		self.velocity = Vector2(
			math.cos(math.radians(shooter.angle))*speed,
			math.sin(math.radians(shooter.angle))*speed
		)
	
	def onTriggerEnter(self,hit):
		if(isinstance(hit,Asteroid)):
			self.engine.scene.removeObject(hit)
			self.engine.scene.removeObject(self)
	
	def update(self):
		if self.rect.left > self.engine.XWIN or self.rect.right < 0 or self.rect.top > self.engine.YWIN or self.rect.bottom < 0:
			self.engine.scene.removeObject(self)
		
		


class Weapon:
	def __init__(self,holder,projectile,firerate,power):
		self.holder = holder
		self.firerate = firerate
		self.power = power
		self.projectile = projectile
		
		self.shooting = False
		self.cpt = firerate
		
	def handle_event(self,event):
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				self.shooting = True
		elif event.type == KEYUP:
			if event.key == K_SPACE:
				self.shooting = False
	
	def shoot(self):
		self.holder.engine.scene.instanciate(
			Projectile,*self.projectile,self.holder,self.power
		)
	
	def update(self):
		if self.shooting:
			self.cpt += self.holder.engine.physics.delta
			if self.cpt > self.firerate:
				self.cpt = 0
				self.shoot()
		

	
	

class Ship(RigidBodyController,Sprite):
	def __init__(self,engine,x,y,w,h,color,groups=[],r=-90,accel=25,mspeed=100,rotatespeed=300,weapon=None,
			keys={"LEFT":K_LEFT,"RIGHT":K_RIGHT,"UP":K_UP,"DOWN":K_DOWN}):
		
		Sprite.__init__(self,engine,x,y,w,h,ALPHA,groups=groups,auto=False)
		RigidBodyController.__init__(self,engine,x,y,w,h,keys,speed=mspeed,accel=accel)
		
		self.angle = r
		self.velocity.y = -100
		self.slowdown = 0
		
		self.shooting = False
		self.weapon = None
		self.rotatespeed = rotatespeed
		self.shipcolor = color
		
		self.points = [(0,0),(0,h),(w,h/2)]
		pygame.draw.polygon(self.origin_image,color,self.points)
	
	def handle_event(self,event):
		RigidBodyController.handle_event(self,event)
		if self.weapon != None: self.weapon.handle_event(event)
		if event.type==KEYDOWN and event.key==K_r:
			self.slowdown=1
		elif event.type==KEYUP and event.key==K_r:
			self.slowdown=0
	
	def update(self):
		self.angle = (self.angle + self.horizontal*self.rotatespeed*self.engine.physics.delta)%360
		
		self.addForce(Vector2(
			math.cos(math.radians(self.angle))*self.accel*-self.vertical,
			math.sin(math.radians(self.angle))*self.accel*-self.vertical
		))
		self.addForce(-self.velocity*0.1*self.slowdown)
		
		self.pos.x = self.pos.x%self.engine.XWIN
		self.pos.y = self.pos.y%self.engine.YWIN
	
		if self.weapon != None:
			self.weapon.update()
	
	# ~ def onCollisionStay(self,hit):
		# ~ if isinstance(hit,Asteroid):
			# ~ self.engine.stop()
		










class StaticStar(Sprite):
	def __init__(self,engine,surface):
		
		Sprite.__init__(self,engine,0,0,1,1,surface,rotate=False)
		self.freeze = False
		self.randomize()
		self.make_velocity()
	
	def randomize(self):
		self.speed = random.randint(10,120)
		self.min_lenght = random.randint(1,5)
		self.lenght = random.randint(100,400)
		self.width = random.randint(1,2)
		self.radius = random.randint(1,5)
		
		centerx = (self.engine.XWIN/2+random.randint(-70,70))
		centery = (self.engine.YWIN/2+random.randint(-70,70))
		a = random.randint(0,360)
		self.pos.x = math.cos(math.radians(a))*250+centerx
		self.pos.y = math.sin(math.radians(a))*150+centery+30
	
	def make_velocity(self):
		dx = self.pos.x - self.engine.XWIN/2
		dy = self.pos.y - self.engine.YWIN/2
		r = math.atan2(dy,dx)
		self.angle = math.degrees(r)
		self.velocity = Vector2(
			math.cos(r)*self.speed,
			math.sin(r)*self.speed
		)
	
	def update(self):
		if self.freeze:return
		
		self.velocity.x *= 0.97
		self.velocity.y *= 0.97
		
		if self.lenght > self.min_lenght:
			self.lenght -= self.speed/1.5
		if self.lenght <= self.min_lenght:
			self.angle = 0
			self.freeze = True
			self.lenght = self.min_lenght
		if not self.freeze:
			self.pos += self.velocity
		if self.rect.left > self.engine.XWIN or self.rect.right < 0 or self.rect.top > self.engine.YWIN or self.rect.bottom < 0:
			self.randomize()
			self.make_velocity()

	def draw(self,surface):
		if self.freeze:
			pygame.draw.circle(surface,self.color,self.rect.center,self.radius)
		else:
			pos2 = (
				math.cos(math.radians(self.angle))*self.lenght+self.pos.x,
				math.sin(math.radians(self.angle))*self.lenght+self.pos.y
			)
			pygame.draw.line(surface,self.color,self.pos,pos2,self.width)



class MovingStar(Sprite):
	def __init__(self,engine,surface):
		Sprite.__init__(self,engine,0,0,1,1,surface,rotate=False)
		self.randomize()
		self.make_velocity()
	
	
	def randomize(self):
		self.max_lenght = random.randint(50,100)
		self.lenght = random.randint(1,5)
		self.width = random.randint(1,3)
		
		centerx = (self.engine.XWIN/2+random.randint(-70,70))
		centery = (self.engine.YWIN/2+random.randint(-70,70))
		self.angle = math.radians(random.randint(0,360))
		self.pos.x = math.cos(self.angle)*250+centerx
		self.pos.y = math.sin(self.angle)*150+centery+30
		self.speed = random.randint(1,5)*(self.width/2)
		
		self.new_surface(self.color)
	
	def make_velocity(self):
		dx = self.pos.x - self.engine.XWIN/2
		dy = self.pos.y - self.engine.YWIN/2
		self.angle = math.atan2(dy,dx)
		self.velocity = Vector2(
			math.cos(self.angle)*self.speed,math.sin(self.angle)*self.speed)
	
	def update(self):
		self.velocity *= 1.2
		
		if self.lenght < self.max_lenght: self.lenght += self.speed
		elif self.lenght > self.max_lenght:
			self.lenght = self.max_lenght
			
		self.pos += self.velocity
		
		if self.rect.left > self.engine.XWIN or self.rect.right < 0 or self.rect.top > self.engine.YWIN or self.rect.bottom < 0:
			self.randomize()
			self.make_velocity()
			
	
	def draw(self,surface):
		pos2 = (
			math.cos(self.angle)*self.lenght+self.pos.x,
			math.sin(self.angle)*self.lenght+self.pos.y
		)
		pygame.draw.line(surface,self.color,self.pos,pos2,self.width)
		

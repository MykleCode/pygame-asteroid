#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.object import Object
from engine.sprite import Sprite
from engine.colliders import *	




class RigidBody(RectCollider):
	def __init__(self,engine,x,y,w,h,maxforce,material=PhysicMaterial(),
			mass=2,kinematic=False,freezeX=False,freezeY=False,auto=True):
		
		super().__init__(engine,x,y,w,h,material=material,auto=auto)
		
		self.mass = mass
		self.kinematic = kinematic
		self.freezeX = freezeX
		self.freezeY = freezeY
		self.maxforce = maxforce
		
		self.velocity = Vector2(0,0)
		self.colliding=False
	
	
	def addForce(self,direction=Vector2(0,0)):
		self.velocity += direction/self.mass
		
			
	def onCollisionLeft(self,hit):
		super().onCollisionLeft(hit)
		if(isinstance(hit,RigidBody)):
			self.physics.elastic_collision(self,hit)
		else:self.physics.bounce(self,hit,d=(1,0))
	def onCollisionRight(self,hit):
		super().onCollisionRight(hit)
		if(isinstance(hit,RigidBody)):
			self.physics.elastic_collision(self,hit)
		else:self.physics.bounce(self,hit,d=(1,0))
	def onCollisionTop(self,hit):
		super().onCollisionTop(hit)
		if(isinstance(hit,RigidBody)):
			self.physics.elastic_collision(self,hit)
		else:self.physics.bounce(self,hit,d=(0,1))
	def onCollisionBottom(self,hit):
		super().onCollisionBottom(hit)
		if(isinstance(hit,RigidBody)):
			self.physics.elastic_collision(self,hit)
		else:self.physics.bounce(self,hit,d=(0,1))
	
	# ~ def friction(self):
		# ~ self.velocity *= hit.physics_material.friction
	
	def physics_update(self,delta=0):
		self.physics.apply_gravity(self)
		self.physics.velocity_fix(self)
		self.physics.move(self)
	
	def collide(self,*objects):
		for l in objects:
			## Collisions on X axis
			self.update_hit_rect(Vector2(1,0))
			hits = self.pygame_rect_collision_detection(l)
			self.collision(hits,direction=Vector2(1,0))
			## Collisions on Y axis
			self.update_rect()
			hits = self.pygame_rect_collision_detection(l)
			self.collision(hits,direction=Vector2(0,1))
		




class KinematicBody(RectCollider):
	def __init__(self,engine,x,y,w,h,
			material=PhysicMaterial(),mass=2,freezeX=None,freezeY=None,auto=True):
		
		super().__init__(engine,x,y,w,h,material=material,auto=auto)
		
		self.freezeX = freezeX
		self.freezeY = freezeY
		self.mass = mass
		
		self.velocity = Vector2(0,0)
		
	
	def onCollisionBottom(self,hit):
		super().onCollisionBottom(hit)
		self.velocity.y = 0
	def onCollisionLeft(self,hit):
		super().onCollisionLeft(hit)
		self.velocity.x = 0
	def onCollisionRight(self,hit):
		super().onCollisionRight(hit)
		self.velocity.x = 0
	def onCollisionTop(self,hit):
		super().onCollisionTop(hit)
		self.velocity.y = 0
	
	def physics_update(self,delta=0):
		self.physics.move(self)
	
	def collide(self,*objects):
		for l in objects:
			## Collisions on X axis
			self.update_hit_rect(Vector2(1,0))
			hits = self.pygame_rect_collision_detection(l)
			self.collision(hits,direction=Vector2(1,0))
			## COllisions on Y axis
			self.update_rect()
			hits = self.pygame_rect_collision_detection(l)
			self.collision(hits,direction=Vector2(0,1))
	




class Physics(threading.Thread):
	def __init__(self,engine,cps=60,gravity=Vector2(0,98),timefactor=1):
		threading.Thread.__init__(self)
		self.alive = threading.Event()
		self.alive.set()
		
		self.engine = engine
		self.gravity = gravity
		self.cps = cps
		self.timefactor = timefactor
		
		self.bodies = []
		self.sprite_colliders = pygame.sprite.Group()
		self.static_colliders = []
		self.colliders = []
		
		self.clock = None
		self.delta = 0
		self.current_cps = 0
		
	def handle_event(self,event):pass	
	
	
	#==== Objects Management ====
	
	def add(self,obj):
		self.addCollider(obj)
		self.addBody(obj)
	
	def adds(self,objects):
		for obj in objects:self.add(obj)
	
	def addBodies(self,objs):
		for obj in objs: self.addBody(obj)
	
	def addColliders(self,objs):
		for obj in objs: self.addCollider(obj)
	
	def addBody(self,obj):
		isBody = isinstance(obj,RigidBody)or isinstance(obj,KinematicBody)
		if isBody and obj not in self.bodies:self.bodies.append(obj);return True
		return False
	
	def addCollider(self,obj):
		if not isinstance(obj,RectCollider):return
		isSprite,isBody = isinstance(obj,Sprite),not self.addBody(obj)
		if obj not in self.colliders:
			self.colliders.append(obj)
		if isBody and not obj in self.static_colliders:
			self.static_colliders.append(obj)
		if isSprite and not obj in self.sprite_colliders:
			self.sprite_colliders.add(obj)
	
	
	def removeBody(self,obj):
		if obj in self.bodies:self.bodies.remove(obj)
	
	def removeCollider(self,obj):
		if obj in self.colliders:self.colliders.remove(obj)
		if obj in self.static_colliders:self.static_colliders.remove(obj)
		if obj in self.sprite_colliders:self.sprite_colliders.remove(obj)
		
	def removeBodies(self,objects):
		for obj in objects:self.removeBody(obj)
	
	def removeColliders(self,objects):
		for obj in objects:self.removeCollider(obj)
	
	def remove(self,obj):
		self.removeBody(obj)
		self.removeCollider(obj)
	
	def removes(self,objs):
		for obj in objs: self.remove(obj)
	
	def clear(self):
		self.static_colliders,self.colliders,self.bodies = [],[],[]
		self.sprite_colliders = pygame.sprite.Group()
		
	
	#==== Physics Function/Tools ====
	
	def elastic_collision(self,obj1,obj2):
		b1,b2 = isinstance(obj1,RigidBody),isinstance(obj2,RigidBody)
		if not b1 and not b2:return
		v1,v2,m1,m2 = obj1.velocity,obj2.velocity,obj1.mass,obj2.mass
		obj1.velocity=(m1-m2)/(m1+m2)*v1+2*m2/(m1+m2)*v2
		obj2.velocity=(m2-m1)/(m1+m2)*v2+2*m1/(m1+m2)*v1
	
	
	def no_rect_overlap(self,obj,hit,left=0,right=0,top=0,bottom=0):
		if left:obj.pos.x = hit.rect.right + obj.hit_rect.width / 2
		if right:obj.pos.x = hit.rect.left - obj.hit_rect.width / 2
		if top:obj.pos.y = hit.rect.bottom + obj.hit_rect.height / 2
		if bottom:obj.pos.y = hit.rect.top - obj.hit_rect.height / 2
	
	
	def bounce(self,obj,hit,d=(0,0)):
		if d[0]:
			obj.velocity.x = (-hit.physics_material.bounce-obj.physics_material.bounce)*obj.velocity.x
		if d[1]:
			obj.velocity.y = (-hit.physics_material.bounce-obj.physics_material.bounce)*obj.velocity.y
	
	def apply_gravity(self,obj):
		if self.gravity==Vector2(0,0):return
		if not obj.kinematic:
			obj.velocity.x += self.gravity.x*self.delta
			obj.velocity.y += self.gravity.y*self.delta
	
	def move(self,obj):
		if not obj.freezeX:
			obj.pos.x += obj.velocity.x * self.delta
		if not obj.freezeY:
			obj.pos.y += obj.velocity.y * self.delta
	
	def velocity_fix(self,obj):
		if obj.velocity.x>obj.maxforce:    obj.velocity.x=obj.maxforce
		elif obj.velocity.x<-obj.maxforce: obj.velocity.x=-objf.maxforce
		if obj.velocity.y>obj.maxforce:    obj.velocity.y=obj.maxforce
		elif obj.velocity.y<-obj.maxforce: obj.velocity.y=-obj.maxforce
	
	
	#==== MAIN THREAD LOOP =====
	
	def run(self):
		self.alive.wait()
		self.clock = pygame.time.Clock()
		lastdelta = time.time()
		
		while self.alive.isSet():
			if self.delta != 0:
				for body in self.bodies:
					body.physics_update()
					body.collide(self.colliders)
					body.update_rect()
			
			self.clock.tick(self.cps)
			self.current_cps = self.clock.get_fps()
			self.delta = (time.time() - lastdelta)*self.timefactor
			lastdelta = time.time()
		
		
	def stop(self, timeout=None):
		self.alive.clear()
		#~ threading.Thread.join(self, timeout)

#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *
from engine.object import Object


class PhysicMaterial:
	def __init__(self,friction=0.2,bounce=0,
			left=True,right=True,up=True,down=True):
		self.friction = friction
		self.bounce = bounce
		
		self.left = left
		self.right = right
		self.up = up
		self.down = down	




class RectCollider(Object):
	def __init__(self,engine,x,y,w,h,
			material=PhysicMaterial(),offset=(0,0),auto=True):
				
		Object.__init__(self,engine,x,y,w,h,auto=auto)
		
		self.offset = offset
		self.hit_rect = Rect(0,0,w+offset[0],h+offset[1])
		self.hit_rect.center = self.pos
		self.physics = self.engine.physics
		self.physics_material = material
		
		self.trigger = False
		self._lock = False
	
	def group_collision_detection(self,group):
		hits = pygame.sprite.spritecollide(self, group, False,self.collide_hit_rect)
		if self in hits: hits.remove(self)
		return hits

	def mask_collision_detection(self,objs):
		return[obj for obj in objs if pygame.sprite.collide_mask(self,obj)and obj!=self]
	
	def pygame_rect_collision_detection(self,objs):
		return[obj for obj in objs if self.hit_rect.colliderect(obj.hit_rect)and obj!=self]
	
	def rect_collision_detection(self,objs):
		hits = []
		for obj in objs:
			if obj != self:
				if obj.hit_rect.x<self.hit_rect.x+self.hit_rect.width:
					if obj.hit_rect.x+obj.hit_rect.width>self.hit_rect.x:
						if obj.hit_rect.y<self.hit_rect.y+self.hit_rect.height:
							if obj.hit_rect.y+obj.hit_rect.height>self.hit_rect.y:
								hits.append(obj)
		return hits
		
	def update_rect(self):
		self.update_hit_rect()
		self.rect.center = self.hit_rect.center
	
	def update_hit_rect(self,direction=Vector2(1,1)):
		if direction.x: self.hit_rect.centerx = self.pos.x
		if direction.y: self.hit_rect.centery = self.pos.y
	
	def collide_hit_rect(self,one, two):
		return one.hit_rect.colliderect(two.hit_rect)


	def onCollisionBottom(self,hit):
		self.engine.physics.no_rect_overlap(self,hit,bottom=1)
	def onCollisionLeft(self,hit):
		self.engine.physics.no_rect_overlap(self,hit,left=1)
	def onCollisionRight(self,hit):
		self.engine.physics.no_rect_overlap(self,hit,right=1)
	def onCollisionTop(self,hit):
		self.engine.physics.no_rect_overlap(self,hit,top=1)
	
	def onCollisionEnter(self,hit):pass
	def onCollisionStay(self,hit):pass
	def onCollisionExit(self):pass
	
	def onTriggerEnter(self,hit):pass
	def onTriggerStay(self,hit):pass
	def onTriggerExit(self):pass
	

	def collision(self,hits,direction=Vector2(1,1)):
		if not hits and self._lock:
			self._lock = False
			if self.trigger:self.onTriggerExit()
			else:self.onCollisionExit()
		elif hits and not self._lock:
			self._lock = True
			if self.trigger:self.onTriggerEnter(hits[0])
			else:self.onCollisionEnter(hits[0])
			
		for hit in hits:
			if self._lock:
				if self.trigger:self.onTriggerStay(hit)
				else:self.onCollisionStay(hit)
			if direction.x and not self.trigger and not hit.trigger:
				if hit.rect.centerx >= self.hit_rect.centerx and hit.physics_material.left and self.velocity.x>0:
					self.onCollisionRight(hit)
				if hit.rect.centerx <= self.hit_rect.centerx and hit.physics_material.right and self.velocity.x<0:
					self.onCollisionLeft(hit)
			if direction.y and not self.trigger and not hit.trigger:
				if hit.rect.centery >= self.hit_rect.centery and hit.physics_material.up and self.velocity.y>0:
					self.onCollisionBottom(hit)
				if hit.rect.centery <= self.hit_rect.centery and hit.physics_material.down and self.velocity.y<0:
					self.onCollisionTop(hit)





#~ class SphereCollider(Object):
	#~ def __init__(self,engine,x,y,radius,
			#~ material=PhysicMaterial(),offset=(0,0),auto=True):
		
		#~ Object.__init__(self,engine,x,y,radius*2,radius*2,auto=auto)
		
		#~ self.offset = offset
		#~ self.hit_rect = Rect(0,0,w+offset[0],h+offset[1])
		#~ self.hit_rect.center = self.pos
		#~ self.physics = self.engine.physics
		#~ self.physics_material = material
		
		#~ self.trigger = False
		#~ self.hits = []
		
		#~ self.lock = False

#~ def sphere_collision(self,obj):
	#~ if isinstance(obj,SphereCollider):
		#~ dx = self.pos.x - obj.pos.x
		#~ dy = self.pos.y - obj.pos.y
		#~ d = math.sqrt(dx*dx + dy*dy)
		#~ if self.radius + obj.radius >= d:
			#~ return True
	#~ elif isinstance(obj,RectCollider):
		#~ self_left = self.pos.x-self.radius
		#~ self_right = self.pos.x+self.radius
		#~ self_up = self.pos.y-self.radius
		#~ self_down = self.pos.y+self.radius
		#~ if (self_right>obj.hit_rect.x and self_right<obj.hit_rect.right)or(self_left<obj.hit_rect.right and self_left>obj.hit_rect.x):
			#~ if (self_down>obj.hit_rect.y and self_down<obj.hit_rect.bottom)or(self_up<obj.hit_rect.bottom and self_up>obj.hit_rect.y):
				#~ return True

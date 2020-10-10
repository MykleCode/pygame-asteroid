#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.colors import *
from engine.object import Object



class Sprite(Object,pygame.sprite.Sprite):
	def __init__(self,engine,x,y,w,h,surface,groups=[],rotate=True,auto=True,r=0):
		pygame.sprite.Sprite.__init__(self,groups)
		Object.__init__(self,engine,x,y,w,h,auto=auto,r=r)
		
		self.new_surface(surface)
		self.auto_rotate = rotate
			
	def onDraw(self):pass
	def onUpdateSurface(self):pass

	def new_surface(self,surface):
		isSurface = (isinstance(surface,pygame.Surface))
		isColor=isinstance(surface,pygame.Color) or (
			isinstance(surface,tuple)and len(surface)>=3)
		
		if not isSurface and not isColor:
			self.image=None;self.mask=None;self.origin_image=None;return
		elif isSurface:
			self.color = None
			self.image = pygame.transform.scale(surface,self.rect.size)
		else:
			self.color = surface
			self.image = pygame.Surface(self.rect.size,pygame.SRCALPHA)
			self.image.fill(self.color)
		
		self.image = self.image.convert_alpha()
		self.mask = pygame.mask.from_surface(self.image)
		self.origin_image = self.image
		self.onUpdateSurface()
			
	
	def rotate(self):
		self.image = pygame.transform.rotate(self.origin_image,-self.angle).convert_alpha()
		self.rect = self.image.get_rect(center=self.pos)
		self.mask = pygame.mask.from_surface(self.image)
	
	def _update(self):
		Object._update(self)
		self.rotate()
	
	def draw(self,surface):
		if self.image != None:
			self.image.unlock()
			surface.blit(self.image,self.rect)
			self.onDraw()
		


class TextSprite(Object,pygame.sprite.Sprite):
	def __init__(self,engine,x,y,size,color,bgcolor=None,font=None,txt="",groups=[],auto=True):
		pygame.sprite.Sprite.__init__(self,groups)
		Object.__init__(self,engine,x,y,size,size,auto=auto)
		
		self.txt = txt
		self.path_font = font
		self.color = color
		self.bgcolor = bgcolor
		
		self.font = None
		self.image = None
		
		self.update()
	
	def load_font(self,path):
		return pygame.font.Font(path,self.rect.width)
	
	def update(self):
		self.font = self.load_font(self.path_font)
		self.image = self.font.render(self.txt,True,self.color).convert_alpha()

	
	def draw(self,surface,offset=(0,0)):
		if self.image != None:
			if self.bgcolor!=None:
				surface.fill(self.bgcolor)
			surface.blit(self.image,(self.rect.x+offset[0],self.rect.y+offset[1]))
		
		
		


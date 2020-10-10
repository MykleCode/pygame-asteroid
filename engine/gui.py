#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.sprite import *
from engine.colors import *


class Button(Sprite):
	def __init__(self,engine,x,y,w,h,surface,active_color,txt,auto=True):
		super().__init__(engine,x,y,w,h,surface,auto=auto)
		
		self.txt = txt
		self.active = False
		self.pressed = False
		self.active_color = active_color
		self.nactive_color = self.color
	
	def handle_event(self,event):
		if event.type == MOUSEMOTION:
			if self.rect.collidepoint(event.pos):
				self.active = True
			else:
				self.active = False
		elif event.type == MOUSEBUTTONDOWN:
			if self.active:
				self.onClick()
	
	def onClick(self):
		self.pressed = True
	
	def update(self):
		self.pressed = False
		self.new_surface(self.active_color) if self.active else self.new_surface(self.nactive_color)
		self.txt.update()
		
	
	def draw(self,surface):
		self.image.unlock()
		surface.blit(self.image,self.rect)
		self.txt.draw(surface,self.rect.topleft)

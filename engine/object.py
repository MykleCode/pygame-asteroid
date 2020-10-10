#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

class Object:
	def __init__(self,engine,x,y,w,h,r=0,mass=1,auto=True):
		self.rect = Rect(0,0,w,h)
		self.pos = Vector2(x,y)
		self.rect.center = self.pos
		self.angle = r
		self.mass = mass
		
		self.engine = engine
		self.scene = self.engine.scene
		
		if not self.engine.scene and auto:
			self.engine.add_ready(self)
		
		
	def update_rect(self):
		self.rect.center = self.pos
	
	def _handle_event(self,event=None):self.handle_event(event)
	def _update(self):
		self.update()
	def handle_event(self,event):pass
	def update(self):pass
	def ready(self):pass
	def destroy(self):self=None

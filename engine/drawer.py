#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.sprite import Sprite,TextSprite
from engine.colors import *
from engine.colliders import *

class Drawer(threading.Thread):
	def __init__(self,engine,fps=60,flags=0,depth=32,
			bgcolor=BLACK,window=None):
		threading.Thread.__init__(self)
		
		self.engine = engine
		self.window=window
		self.fps = fps
		self.depth = depth
		self.flags = flags
		self.bgcolor = bgcolor
		
		self.sprites = []
		self.current_fps = 0
		self.clock = pygame.time.Clock()
		self.alive = threading.Event()
		self.alive.set()

	
	def add(self,sprite):
		if not sprite in self.sprites:
			if isinstance(sprite,pygame.sprite.Sprite):
				self.sprites.append(sprite)
	
	def remove(self,sprite):
		if sprite in self.sprites:
			self.sprites.remove(sprite)
	
	def clear(self):
		self.sprites = []
		
	
	def create_window(self):
		self.window = pygame.display.set_mode((self.engine.XWIN,self.engine.YWIN),self.flags,self.depth)
	
	
	# ==== Main ====

	def run(self):
		while self.alive.isSet():
			if self.window != None:
				if self.bgcolor!=None:
					self.window.fill(self.bgcolor)
				for sprite in self.sprites:
					sprite.draw(self.window)
				
				pygame.display.update()
				self.clock.tick(self.fps)
				self.current_fps = self.clock.get_fps()
				

	def stop(self, timeout=None):
		self.alive.clear()

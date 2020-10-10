#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.__init__ import *


pygame.init()




class Engine(threading.Thread):
	def __init__(self,display,mainscene,
			fps=60,flags=0,depth=32,title="Window"):
		
		threading.Thread.__init__(self)
		
		self.DISPLAY = display
		self.XWIN,self.YWIN = display
		self.FPS = fps
		self.FLAGS = flags
		self.TITLE = title
		self.DEPTH = depth
		
		self.drawer = Drawer(self,fps=fps,flags=flags,depth=depth)
		self.physics = Physics(self,cps=30)
		self.main_scene = mainscene
		
		self.scene = None
		self.alive = threading.Event()
		self.objs_ready = []
		
		
	#---EVENTS---
	def removedObject(self,obj):
		self.drawer.remove(obj)
		self.physics.remove(obj)
	def addedObject(self,obj):
		self.drawer.add(obj)
		self.physics.add(obj)
	
	#---TOOLS---
	def applyX(self,x,res=1280):
		return int(self.XWIN/(res/x))
	def applyY(self,y,res=720):
		return int(self.YWIN/(res/y))
	def applyXY(self,x,xres=1280,yres=720):
		return int(self.XWIN*self.YWIN/(xres*yres/x))
	
	def change_physics(self,new):
		self.physics.clear()
		self.physics.stop()
		self.physics = new
		self.physics.start()


	#======== START ========

	def _print_start(self):
		print("-------------------------")
		print(" Welcome on {0}".format(self.TITLE))
		print("-------------------------")

	def _set_display(self):
		self.clock = pygame.time.Clock()
		self.drawer.create_window()
		pygame.display.set_caption(self.TITLE)

	#----- START MAIN -----
	def start(self):
		threading.Thread.start(self)
		self.ready()
	
	def add_ready(self,obj):
		if obj not in self.objs_ready:
			self.objs_ready.append(obj)
	
	def ready(self):
		#~ try:
		self._print_start()
		self._set_display()
		self.drawer.start()
		self.physics.start()
		self.load_scene(self.main_scene)
		self.alive.set()
		#~ except Exception as e:
			#~ print("Something went wrong while initialising Engine: \n",e)
		
		
	#======== RUN ========
	
	def load_scene(self,scene):
		self.objs_ready = []
		self.physics.clear()
		self.drawer.clear()
		self.scene = None
		self.scene = scene(self)
		self.scene.addObjects(self.objs_ready)
		self.scene.onStart()
	
	#----- RUN MAIN -----
	def run(self):
		self.alive.wait()
		
		while self.alive.isSet():
			#~ print(int(self.drawer.current_fps),int(self.physics.current_cps))
			if self.scene:
				self.scene.run()
			self.clock.tick(self.FPS)
	
	def stop(self,timeout=None):
		self.drawer.stop(timeout)
		self.physics.stop(timeout)
		self.alive.clear()
	
	

#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *
from engine.object import *
from engine.sprite import *
from engine.physics import *



class Scene:
	def __init__(self,engine):
		self.objects = []
		self.ready = False
		self.engine = engine
	
	
	
	# ==== Objects Management ====
	
	def instanciate(self,classObject,*args,**kwargs):
		newObject = classObject(*args,**kwargs)
		self.addObject(newObject)
		return newObject
	
	def addObject(self,obj):
		if not isinstance(obj,Object) or obj in self.objects:return
		self.objects.append(obj)
		self.onObjectAdded(obj)
		obj.ready()
	
	def addObjects(self,objects):
		for obj in objects:self.addObject(obj)
	
	def removeObject(self,obj):
		if obj in self.objects:
			i = self.objects.index(obj)
			self.objects[i]=None
			del self.objects[i]
			self.onObjectRemoved(obj)
	
	def removeObjects(self,objects):
		for obj in objects:
			self.remove(obj)
			
	# ==== MAIN ====		
	
	def _handle_event(self,event):
		if event.type == QUIT:
			self.engine.stop()
		for obj in self.objects:
			obj._handle_event(event)
	
	
	def run(self):
		#------ EVENT ------
		self.onEventEnter()
		for event in pygame.event.get():
			self.onEventStay(event)
			self._handle_event(event)
		#------ UPDATE ------
		self.onUpdateEnter()
		for obj in self.objects:
			self.onUpdateStay(obj)
			obj._update()
		self.onRun()
	
	
	# ==== EVENTS ====
	
	def onStart(self):self.ready=True
	def onRun(self):pass
	
	def onObjectAdded(self,obj):
		self.engine.addedObject(obj)
	def onObjectRemoved(self,obj):
		self.engine.removedObject(obj)
	
	def onEventEnter(self):pass
	def onEventStay(self,event):pass
	def onUpdateEnter(self):pass
	def onUpdateStay(self,obj):pass

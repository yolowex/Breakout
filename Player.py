import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
from typing import Optional
from pygame.surface import Surface

from Window import Window
from EventHolder import EventHolder
from Assets import Assets
from Colors import Colors


import random as r



from CommonResources import CommonResources

class Player:
    def __init__(self,rect:Rect,color:Color,common_resources:CommonResources):
        self.common_resources = common_resources
        self.events = self.common_resources.event_holder
        self.colors = self.common_resources.colors
        self.assets = self.common_resources.assets
        self.window = self.common_resources.window

        self.pos = Pos(rect.x,rect.y)
        self.size = Pos(rect.width,rect.height)

        self.color = color

    @property
    def rect( self ):
        return Rect(self.pos.x,self.pos.y,self.size.x,self.size.y)


    def move( self,hkeys ):

        right = K_RIGHT in hkeys or K_d in hkeys
        left = K_LEFT in hkeys or K_a in hkeys
        if right and left: right = left = False


        if right :
            self.pos.x += self.speed

        if left :
            self.pos.x -= self.speed

        stick = not self.window.rect.contains(self.rect)

        if stick :
            if right :
                self.pos.x = self.window.size.x - self.rect.width

            if left :
                self.pos.x = 0



    def check_events( self ):
        hkeys = self.events.held_keys

        self.move(hkeys)




    @property
    def speed( self ):
        return self.rect.width * 0.04


    def render( self,surface:Surface ):
        pg.draw.rect(surface,self.color,self.rect)



import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from pygame.surface import Surface

from CommonResources import CommonResources
import math

def rotate(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


class Ball:
    def __init__(self,rect:Rect,color:Color,common_resources:CommonResources):
        self.common_resources = common_resources
        self.events = self.common_resources.event_holder
        self.colors = self.common_resources.colors
        self.assets = self.common_resources.assets
        self.window = self.common_resources.window

        self.pos = Pos(rect.x,rect.y)
        self.size = Pos(rect.width,rect.height)
        self.color = color

        self.angle = 10


    @property
    def top( self ):
        return Pos(self.center.x,self.center.y-100)

    @property
    def target_point( self ):
        return rotate(self.center,self.top,self.angle)

    @property
    def center( self ):
        return Pos(self.pos.x+self.size.x/2,self.pos.y+self.size.y/2)

    @center.setter
    def center( self, pos:Pos):
        self.pos.x = pos.x - self.size.x / 2
        self.pos.y = pos.y - self.size.y / 2

    @property
    def rect( self ):
        return Rect(self.pos.x,self.pos.y,self.size.x,self.size.y)


    def move( self ):
        center = self.center
        target = self.target_point

        new_center = self.center.lerp(target,0.04)
        self.center = new_center

        c = self.center
        a = self.angle

        if c.x < 0 + self.size.x / 2:
            c.x = self.size.x / 2

            if 180<a<270:
                self.angle = 180 - abs(180 - a)

            if 270<a<360:
                self.angle = abs(360 - a)

        if c.x > self.window.size.x  - self.size.x / 2:
            c.x = self.window.size.x - self.size.x / 2

            if 0<a<90:
                self.angle = 360 - a

            if 90<a<180:
                self.angle = 180 + abs(180 - a)

        if c.y < 0 + self.size.y / 2:
            c.y = self.size.y / 2
            if 270 < a < 360 :
                self.angle = 270 - abs(270 - a)

            if 0 < a < 90 :
                self.angle = 90 + abs(90 - a)

        if c.y > self.window.size.y - self.size.y / 2:
            c.y = self.window.size.y - self.size.y / 2
            if 90 < a < 180 :
                self.angle = 90 - abs(90 - a)

            if 180 < a < 270 :
                self.angle = 270 + abs(270 - a)


        self.center = c


    def check_events( self ):
        self.angle = self.angle % 360
        self.move()

    def render_debug( self,surface:Surface ):
        pg.draw.line(surface,self.colors.WHITE,self.center,self.target_point)


    def render( self,surface:Surface ):
        pg.draw.rect(surface,self.color,self.rect)

        if self.events.should_render_debug:
            self.render_debug(surface)




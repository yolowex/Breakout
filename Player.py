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


class Player :

    def __init__( self, rect: Rect, color: Color) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.pos = Pos(rect.x, rect.y)
        self.size = Pos(rect.width, rect.height)

        self.color = color


    @property
    def rect( self ) :
        return Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)


    @property
    def speed( self ) :
        return (self.window.size.y * 0.07 - self.rect.height) * 0.1

    @property
    def speed_change_speed( self ):
        return self.rect.height * 0.1

    @property
    def size_change_speed( self ) :
        return self.rect.width * 0.1


    def move( self, hkeys ) :
        right = K_RIGHT in hkeys or K_d in hkeys
        left = K_LEFT in hkeys or K_a in hkeys
        if right and left : right = left = False

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


    def speed_up( self ):
        last_rect = self.rect
        center = self.rect.center
        speed_change = self.speed_change_speed
        self.size.y -= speed_change
        revert = self.size.y <= self.window.size.y * 0.01
        rect = self.rect
        rect.center = center

        if revert:
            self.pos.x,self.pos.y,self.size.x,self.size.y = last_rect
        else:
            self.pos.x,self.pos.y = rect.x,rect.y



    def speed_down( self ):
        last_rect = self.rect
        center = self.rect.center
        speed_change = self.speed_change_speed
        self.size.y += speed_change
        revert = self.size.y > self.window.size.y * 0.065
        rect = self.rect
        rect.center = center

        if revert :
            self.pos.x, self.pos.y, self.size.x, self.size.y = last_rect
        else :
            self.pos.x, self.pos.y = rect.x, rect.y





    def grow( self ) :
        last_rect = self.rect
        center = self.rect.center
        self.size.x += self.size_change_speed
        rect = self.rect
        rect.center = center
        self.pos.x, self.pos.y = rect.x, rect.y

        revert = not self.window.rect.contains(self.rect) or self.size.x >= self.window.size.x * 0.3

        if revert :
            self.pos.x, self.pos.y = last_rect.x, last_rect.y
            self.size.x, self.size.y = last_rect.width, last_rect.height


    def shrink( self ) :
        last_rect = self.rect
        center = self.rect.center
        self.size.x -= self.size_change_speed
        rect = self.rect
        rect.center = center
        self.pos.x, self.pos.y = rect.x, rect.y

        revert = not self.window.rect.contains(self.rect) or self.size.x < self.window.size.x * 0.05

        if revert :
            self.pos.x, self.pos.y = last_rect.x, last_rect.y
            self.size.x, self.size.y = last_rect.width, last_rect.height


    def check_events( self ) :
        hkeys = self.events.held_keys

        pkeys = self.events.pressed_keys

        if K_UP in pkeys :
            self.grow()
        if K_DOWN in pkeys :
            self.shrink()

        if K_w in pkeys:
            self.speed_up()
        if K_s in pkeys:
            self.speed_down()


        self.move(hkeys)


    def render( self, surface: Surface ) :
        pg.draw.rect(surface, self.color, self.rect)

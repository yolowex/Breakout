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
    """
        Upgradeable abilities:
            paddle size,
            paddle speed,

    """

    def __init__( self, rect: Rect, color: Color) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.pos = Pos(rect.x, rect.y)
        self.size = Pos(rect.width, rect.height)

        self.color = color

        self.size_list  = []
        self.speed_list = []


        min_size = self.size.x * 0.1
        size_wing = 6
        self.size_index = 0
        self.min_size_index = -size_wing
        self.max_size_index = size_wing

        size_step = abs(self.size.x-min_size) / abs(self.min_size_index)


        for i in range(self.min_size_index,self.max_size_index+1):
            mult = i
            if i > 0:
                mult = i * 2

            new_size = self.size.x + (size_step * mult)
            self.size_list.append(new_size)


        self.size_index += abs(self.min_size_index)
        self.max_size_index += abs(self.min_size_index)
        self.min_size_index += abs(self.min_size_index)

        min_speed = self.size.y * 0.1

        self.speed_index = 0
        speed_wing = 6
        self.min_speed_index = -speed_wing
        self.max_speed_index = speed_wing

        speed_step = abs(self.size.y - min_speed) / abs(self.min_speed_index)

        for i in range(self.min_speed_index, self.max_speed_index+ 1) :
            new_speed = self.size.y + (speed_step * i)
            self.speed_list.append(new_speed)

        self.speed_list = self.speed_list[::-1]


        self.speed_index += abs(self.min_speed_index)
        self.max_speed_index += abs(self.min_speed_index)
        self.min_speed_index += abs(self.min_speed_index)




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


    def respeed( self ):
        center = self.rect.center
        self.size.y = self.speed_list[self.speed_index]
        rect = self.rect
        rect.center = center
        self.pos.x, self.pos.y = rect.x, rect.y


    def speed_up( self ):
        if self.speed_index == self.max_speed_index :
            return
        self.speed_index += 1

        self.respeed()


    def speed_down( self ):
        if self.speed_index == self.min_speed_index :
            return
        self.speed_index -= 1

        self.respeed()

    def resize( self ):
        last_rect = self.rect
        center = self.rect.center
        self.size.x = self.size_list[self.size_index]
        rect = self.rect
        rect.center = center
        self.pos.x, self.pos.y = rect.x, rect.y

        revert = not self.window.rect.contains(self.rect)

        if revert :
            self.pos.x, self.pos.y = last_rect.x, last_rect.y
            self.size.x, self.size.y = last_rect.width, last_rect.height


    def grow( self ) :
        if self.size_index == self.max_size_index:
            return
        self.size_index += 1

        self.resize()

    def shrink( self ) :
        if self.size_index == self.min_size_index:
            return
        self.size_index -= 1

        self.resize()


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

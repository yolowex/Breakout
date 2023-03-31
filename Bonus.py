import random

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
from functions import *

import random as r

from Ball import Ball

from CommonResources import CommonResources

class Bonus:

    names_list = [
        "grow",
        "shrink",
        "speed_up",
        "speed_down",
        "arm_up",
        "hype_arm_up",
        "fireball",
        "multiball",
    ]

    grow_color = Colors.GREEN
    shrink_color = Colors.RED
    speed_up_color = Colors.WHITE
    speed_down_color = Colors.BLACK
    arm_up_color = Colors.RED.lerp(Colors.BLACK,0.5)
    hype_arm_up_color = Colors.RED.lerp(Colors.BLUE,0.5)
    fireball_color = Colors.RED.lerp(Colors.WHITE,0.7)
    multiball_color = Colors.GREEN.lerp(Colors.RED,0.5)


    all_ = {
        "grow":grow_color,
        "shrink":shrink_color,
        "speed_up":speed_up_color,
        "speed_down":speed_down_color,
        "arm_up":arm_up_color,
        "hype_arm_up" : hype_arm_up_color,
        "fireball": fireball_color,
        "multiball": multiball_color
    }


    def __init__(self,name:str,center:Pos,radius,color:Color):
        if type(center) == tuple: center = Pos(center)

        self.consumed = False

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window
        self.player = CommonResources.player

        self.name = name
        self.center = center
        self.radius = radius
        self.color = color
        self.fall_speed = 1 / self.events.determined_fps * 2 * r.uniform(0.7,2)

    @property
    def rect( self ):
        return Rect(
            self.center.x - self.radius,
            self.center.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    @property
    def ball( self ):
        return CommonResources.game.ball

    def update( self ):
        self.player = CommonResources.player

    def check_events( self ):
        self.center.y += self.fall_speed * (self.radius * 2)

        p: Player = self.player
        b: Ball = self.ball

        cool_dict ={
            "grow":p.grow,
            "shrink":p.shrink,
            "speed_up":p.speed_up,
            "speed_down":p.speed_down,
            "arm_up":p.arm_up,
            "hype_arm_up":p.hype_arm_up,
            "fireball": b.ignite,
            "multiball": b.divide
        }

        pr = self.player.rect

        if self.rect.colliderect(pr):
            self.consumed = True
            cool_dict[self.name]()


    def render_debug( self,surface:Surface ):
        ...

    def render( self,surface:Surface ):
        pg.draw.circle(surface,self.color,self.center,self.radius)
        pg.draw.circle(surface,self.color.lerp(Colors.BLACK,0.5),self.center,self.radius,width=3)




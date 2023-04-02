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
from random import randint as rr

from Ball import Ball

from CommonResources import CommonResources


# RESPECT PEP 8 & PEP 20

class Bonus :
    GROW = 'grow'
    SHRINK = 'shrink'
    SPEED_UP = 'speed_up'
    SPEED_DOWN = 'speed_down'
    ARM_UP = 'arm_up'
    HYPE_ARM_UP = 'hype_arm_up'
    FIREBALL = 'fireball'
    MULTIBALL = 'multiball'

    names_list = [GROW, SHRINK, SPEED_UP, SPEED_DOWN, ARM_UP, HYPE_ARM_UP, FIREBALL, MULTIBALL, ]

    by_number = {0 : "none", 1 : "empty", 2 : "bad", 3 : "good", 4 : "best"}

    section_dict = {"bad" : [SHRINK, SPEED_DOWN], "good" : [ARM_UP, MULTIBALL, GROW, SPEED_UP],
        "best" : [FIREBALL, HYPE_ARM_UP]}

    grow_color = Colors.GREEN
    shrink_color = Colors.RED
    speed_up_color = Colors.BLACK.lerp(Colors.WHITE,0.8)
    speed_down_color = Colors.BLACK
    arm_up_color = Colors.RED.lerp(Colors.BLACK, 0.5)
    hype_arm_up_color = Colors.RED.lerp(Colors.BLUE, 0.5)
    fireball_color = Color("#780000")
    multiball_color = Colors.GREEN.lerp(Colors.RED, 0.5)

    all_ = {GROW : grow_color, SHRINK : shrink_color, SPEED_UP : speed_up_color,
        SPEED_DOWN : speed_down_color, ARM_UP : arm_up_color, HYPE_ARM_UP : hype_arm_up_color,
        FIREBALL : fireball_color, MULTIBALL : multiball_color}


    def __init__( self, name: str, center: Pos, radius, color: Color ) :
        if type(center) == tuple : center = Pos(center)


        self.consumed = False
        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window
        self.player = CommonResources.player

        self.angle = 0

        self.name = name
        self.center = center
        self.radius = radius
        if self.name == Bonus.MULTIBALL : self.radius *= 1.5
        if self.name == Bonus.SHRINK: self.radius *= r.uniform(0.5,1)
        if self.name == Bonus.SPEED_DOWN: self.radius *= r.uniform(0.5,1)
        self.tail = []
        self.color = color

        if self.name == Bonus.FIREBALL:
            self.fall_speed = 1 / self.events.determined_fps * 2 * r.uniform(2, 4)
        else:
            self.fall_speed = 1 / self.events.determined_fps * 2 * r.uniform(0.5, 2)

        if self.name == Bonus.SHRINK: self.fall_speed *= 2

    @property
    def sound( self ):
        if self.name in Bonus.section_dict['bad']:
            return self.assets.bad_sound
        if self.name in Bonus.section_dict['good']:
            return self.assets.good_sound
        if self.name in Bonus.section_dict['best']:
            return self.assets.best_sound

    @property
    def multiball_top( self ) :
        pos = self.center.copy()
        pos.y -= self.radius * 0.5
        return pos


    @property
    def fire_color( self ) :
        red = rr(225, 255)
        green = rr(0, 150)
        blue = green
        return Color(red, green, blue)

    @property
    def multiball_size( self ) :
        return self.radius * 0.46


    @property
    def rect( self ) :
        return Rect(self.center.x - self.radius, self.center.y - self.radius, self.radius * 2,
            self.radius * 2)


    @property
    def this_color( self ) :
        if self.name == Bonus.HYPE_ARM_UP :
            return Colors.random_color()

        if self.name == Bonus.MULTIBALL :
            return self.ball.color

        if self.name == Bonus.ARM_UP:
            return self.player.bullets_color

        if self.name == Bonus.SPEED_UP:
            noise = [rr(-50,50) for _ in range(3)]
            new_color = [self.color.r + noise[0],self.color.g + noise[1],self.color.b+noise[2]]
            new_color = [cap(i,0,255) for i in new_color]
            return Color(new_color)

        return self.color


    @property
    def ball( self ) :
        return CommonResources.game.ball


    def update( self ) :
        self.player = CommonResources.player


    def check_fire_tail_events( self ):

        c = 0
        for _, radius, _ in self.tail :
            radius *= 0.98
            self.tail[c][1] = radius
            if radius <= 0.7 :
                self.tail.pop(c)
            c += 1

        center = self.center.copy()
        radius = self.radius
        color = self.fire_color
        x = int(self.radius / 2.5)
        noise = Pos(r.randint(-x,x),r.randint(-x,x))
        center.x += noise.x
        center.y += noise.y
        self.tail.append([center,radius,color])

    def check_events( self ) :
        if self.name == Bonus.MULTIBALL :
            self.angle += 0.5
        elif self.name == Bonus.HYPE_ARM_UP :
            self.angle += 0.7
        elif self.name == Bonus.ARM_UP :
            self.angle -= 0.35
        elif self.name == Bonus.SPEED_UP:
            self.center.x += rr(-1,1)
            self.center.y += rr(-1,1)
        elif self.name == Bonus.SPEED_DOWN:
            diff = self.player.rect.center[0] - self.center.x
            if diff!=0:
                self.center.x += (diff/abs(diff)) * self.fall_speed * (self.radius * 2) * 0.2

        if self.name == Bonus.FIREBALL:
            self.check_fire_tail_events()

        self.center.y += self.fall_speed * (self.radius * 2)

        p = self.player
        b: Ball = self.ball

        cool_dict = {"grow" : p.grow, "shrink" : p.shrink, "speed_up" : p.speed_up,
            "speed_down" : p.speed_down, "arm_up" : p.arm_up, "hype_arm_up" : p.hype_arm_up,
            "fireball" : b.ignite, "multiball" : b.divide}

        pr = self.player.rect

        if self.rect.colliderect(pr) :
            self.consumed = True
            CommonResources.bonuses_channel.play(self.sound)
            cool_dict[self.name]()


    def render_debug( self, surface: Surface ) :
        ...


    def render_multiball( self, surface: Surface ) :
        p1 = rotate(self.center, self.multiball_top, self.angle + 0)
        p2 = rotate(self.center, self.multiball_top, self.angle + 120)
        p3 = rotate(self.center, self.multiball_top, self.angle + 240)

        pg.draw.circle(surface, self.this_color, p1, self.multiball_size)
        pg.draw.circle(surface, self.this_color, p2, self.multiball_size)
        pg.draw.circle(surface, self.this_color, p3, self.multiball_size)

        pg.draw.circle(surface, self.this_color.lerp(Colors.BLACK, 0.8), p1, self.multiball_size,
            width=2)
        pg.draw.circle(surface, self.this_color.lerp(Colors.BLACK, 0.8), p2, self.multiball_size,
            width=2)
        pg.draw.circle(surface, self.this_color.lerp(Colors.BLACK, 0.8), p3, self.multiball_size,
            width=2)

    def render_hype_gun( self, surface: Surface  ):
        polygon(surface,self.this_color,self.center,self.radius,3,self.angle)

        polygon(surface,
            self.this_color.lerp(Colors.BLACK,0.7),
            self.center,
            self.radius,3,self.angle,width=2
        )

    def render_gun( self,surface:Surface ):
        polygon(surface,self.this_color,self.center,self.radius,3,self.angle)

        t = self.this_color
        n = [t.r + 125,t.g + 125,t.b +125]
        border_color = [i%255 for i in n]


        polygon(surface,
            border_color,
            self.center,
            self.radius,3,self.angle,width=2
        )


    def render_fireball( self, surface: Surface ):
        for center, radius, color in self.tail :
            pg.draw.circle(surface, color, center, radius)

        pg.draw.circle(surface, self.color, self.center,self.radius)

    def render_speed_up( self,surface:Surface ):
        pg.draw.circle(surface,self.this_color,self.center,self.radius)
        pg.draw.circle(surface, self.this_color.lerp(Colors.BLACK, 0.5), self.center, self.radius,
            width=3)

    def render( self, surface: Surface ) :
        if self.name == Bonus.MULTIBALL :
            self.render_multiball(surface)
            return

        if self.name == Bonus.HYPE_ARM_UP:
            self.render_hype_gun(surface)
            return

        if self.name == Bonus.ARM_UP:
            self.render_gun(surface)
            return

        if self.name == Bonus.FIREBALL:
            self.render_fireball(surface)
            return

        if self.name == Bonus.SPEED_UP:
            self.render_speed_up(surface)
            return

        pg.draw.circle(surface, self.this_color, self.center, self.radius)
        pg.draw.circle(surface, self.this_color.lerp(Colors.BLACK, 0.5), self.center, self.radius,
            width=3)


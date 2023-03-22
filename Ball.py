import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from pygame.surface import Surface
from functions import *

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
        self.player = self.common_resources.player
        self.map_ = self.common_resources.map_

        self.pos = Pos(rect.x,rect.y)
        self.size = Pos(rect.width,rect.height)
        self.color = color

        self.top_pos_distance = 100
        self.speed = 0.05

        self.angle = 180


    def reset( self ):
        p_rect = self.player.rect
        rect = self.rect
        rect.center = p_rect.center
        rect.y = p_rect.y - rect.height
        self.pos.x,self.pos.y = rect.x,rect.y
        self.angle = 0

    @property
    def top( self ):
        return Pos(self.center.x,self.center.y-self.top_pos_distance)

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

    def check_walls_collision( self ):
        c = self.center
        a = self.angle

        ran_factor = 5
        ran = lambda: r.randint(-ran_factor,ran_factor)

        if c.x < 0 + self.size.x / 2 : # LEFT
            c.x = self.size.x / 2

            if a == 180:
                self.angle = 179

            if a == 270:
                self.angle = 90 + ran()

            if a == 360 or a == 0:
                self.angle = 1

            if 180 < a < 270 :
                self.angle = 180 - abs(180 - a) + ran()

            if 270 < a < 360 :
                self.angle = abs(360 - a) + ran()


        if c.x > self.window.size.x - self.size.x / 2 : # RIGHT
            c.x = self.window.size.x - self.size.x / 2

            if a == 180 :
                self.angle = 181

            if a == 90 :
                self.angle = 270 + ran()

            if a == 360 or a == 0 :
                self.angle = 359

            if 0 < a < 90 :
                self.angle = 360 - a + ran()

            if 90 < a < 180 :
                self.angle = 180 + abs(180 - a) + ran()

        if c.y < 0 + self.size.y / 2 : # UP
            c.y = self.size.y / 2

            if a == 90 :
                self.angle = 91

            if a == 0 or a == 360 :
                self.angle = 180 + ran()

            if a == 270 :
                self.angle = 269

            if 270 < a < 360 :
                self.angle = 270 - abs(270 - a) + ran()

            if 0 < a < 90 :
                self.angle = 90 + abs(90 - a) + ran()

        if c.y > self.window.size.y - self.size.y / 2 : # DOWN
            self.angle = 180
            c.y = self.window.size.y - self.size.y / 2


            # c.y = self.window.size.y - self.size.y / 2
            #
            # if a == 90 :
            #     self.angle = 89
            #
            # if a == 180 :
            #     self.angle = 0  + ran()
            #
            # if a == 270 :
            #     self.angle = 271
            #
            # if 90 < a < 180 :
            #     self.angle = 90 - abs(90 - a) + ran()
            #
            # if 180 < a < 270 :
            #     self.angle = 270 + abs(270 - a) + ran()



        self.center = c

    def check_player_collision( self ):


        if self.player.rect.colliderect(self.rect):
            self.pos.y = self.player.rect.y - self.size.y

            p_center = Pos(self.player.rect.center)
            diff = self.rect.center[0] - p_center.x
            reflection_percent = percent(self.player.rect.width/2,diff)
            if reflection_percent<-100: reflection_percent = -100
            if reflection_percent>100: reflection_percent = 100

            reflection_percent += 100

            reflection_degree = (120 / 200) * reflection_percent - 120 / 2

            self.angle = reflection_degree

    def check_map_collisions( self ):

        for i in self.map_.bricks:

            if i.rect.colliderect(self.rect) :


                p_center = Pos(i.rect.center)
                diff = self.rect.center[0] - p_center.x
                reflection_percent = percent(i.rect.width / 2, diff)
                if reflection_percent < -100 : reflection_percent = -100
                if reflection_percent > 100 : reflection_percent = 100

                reflection_percent += 100

                reflection_degree = (120 / 200) * reflection_percent - 120 / 2

                self.angle = reflection_degree

                break



    def move( self ):

        target = self.target_point

        new_center = self.center.lerp(target,self.speed)
        self.center = new_center

        self.check_walls_collision()
        self.check_player_collision()
        self.check_map_collisions()


    def check_events( self ):
        if K_SPACE in self.events.pressed_keys:
            self.reset()

        self.angle = self.angle % 360
        self.move()


    def render_debug( self,surface:Surface ):
        pg.draw.line(surface,self.colors.WHITE,self.center,self.target_point)


    def render( self,surface:Surface ):
        pg.draw.rect(surface,self.color,self.rect)

        if self.events.should_render_debug:
            self.render_debug(surface)




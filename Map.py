import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
import json

from typing import Optional
from random import randint as rr
from pygame.surface import Surface
from Colors import Colors

from Brick import Brick
from CommonResources import CommonResources


class Map :

    def __init__( self,path:str ) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.path = "none"
        self.name = "none"
        self.rect: Optional[Rect]= None
        self.total_gap_x = 0
        self.total_gap_y = 0

        self.colors = {}
        self.health_rows = []
        self.bricks = []
        self.bonus_list = []


        self.load(path)
        self.create_tiles()


    def load( self,path:str ):
        self.path = path
        f = open(path).read()
        j = json.loads(f)

        self.name = j['name']
        self.health_rows = j["health_rows"]
        self.rect = Rect(
                        j['rect_x'] * self.window.size.x,
                        j['rect_y'] * self.window.size.y,
                        j['rect_w'] * self.window.size.x,
                        j['rect_h'] * self.window.size.y
        )

        self.total_gap_x = j['total_gap_x']
        self.total_gap_y = j['total_gap_y']
        self.colors:dict = j['colors']



    def update( self ):
        for brick in self.bricks:
            if brick.bonus is not None:
                brick.bonus.update()

    def create_tiles( self ) :

        Y = self.rect.height / len(self.health_rows)


        for y,row in zip(range(len(self.health_rows)),self.health_rows):
            for x,health in zip(range(len(row)),row):
                X = self.rect.width / len(row)
                if str(health) in self.colors:
                    color = self.colors[
                        str(health)
                    ]
                else:
                    color = Colors.random_color()

                rect = Rect(
                    self.rect.x+x*X+self.total_gap_x*X/2,
                    self.rect.y+y*Y+self.total_gap_y*Y/2,
                    X-self.total_gap_x*X,
                    Y-self.total_gap_y*Y
                )
                brick = Brick(rect,color,health)
                self.bricks.append(brick)


    def check_events( self ) :

        brick_destroy_list = []
        bonus_destroy_list = []

        for bonus,c in zip(self.bonus_list,range(len(self.bonus_list))):
            if (bonus.center.y - bonus.radius) > self.window.size.y or bonus.consumed:
                bonus_destroy_list.append(c)
            else:
                bonus.check_events()

        for c in bonus_destroy_list[::-1]:
            self.bonus_list.pop(c)



        for brick,c in zip(self.bricks,range(len(self.bricks))):
            if brick.health == 0:
                brick_destroy_list.append(c)
                if brick.bonus is not None:
                    self.bonus_list.append(brick.bonus)


        for c in brick_destroy_list[::-1]:
            self.bricks.pop(c)


    def render_debug( self, surface: Surface ) :
        pg.draw.rect(surface, [0, 0, 0], self.rect, width=3)


    def render( self, surface: Surface ) :
        for brick in self.bricks :
            brick.render(surface)

        for bonus in self.bonus_list:
            bonus.render(surface)

        if self.events.should_render_debug:
            self.render_debug(surface)




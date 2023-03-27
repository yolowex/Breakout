import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from random import randint as rr
from pygame.surface import Surface

from Colors import Colors

from Brick import Brick
from CommonResources import CommonResources


class Map :

    def __init__( self, rect: Rect, x_tiles, y_tiles ) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.rect = rect
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles
        self.bricks = []
        self.bonus_list = []
        self.create_tiles()

    def update( self ):
        for brick in self.bricks:
            if brick.bonus is not None:
                brick.bonus.update()

    def create_tiles( self ) :
        X = self.rect.width / self.x_tiles
        Y = self.rect.height / self.y_tiles
        gap_x = self.rect.width * 0.01 / self.x_tiles
        gap_y = self.rect.height * 0.01 / self.y_tiles

        for y in range(self.y_tiles) :
            color = Colors.random_color().lerp([255, 0, 0], 0.4)
            for x in range(self.x_tiles) :
                rect = Rect(self.rect.x + x * X + gap_x / 2, self.rect.y + y * Y + gap_y / 2,
                    X - gap_x, Y - gap_y)

                brick = Brick(rect, color,rr(1,1))
                brick.set_bonus(30)

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




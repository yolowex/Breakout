import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from pygame.surface import Surface

from Colors import Colors

from Brick import Brick


class Map :

    def __init__( self, rect: Rect, x_tiles, y_tiles ) :
        self.rect = rect
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles
        self.bricks = []
        self.create_tiles()


    def create_tiles( self ) :
        X = self.rect.width / self.x_tiles
        Y = self.rect.height / self.y_tiles
        gap_x = self.rect.width * 0.3 / ( self.x_tiles )
        gap_y = self.rect.height * 0.3 / ( self.y_tiles )


        for y in range(self.y_tiles) :
            color = Colors.random_color().lerp([255,0,0],0.4)
            for x in range(self.x_tiles) :
                rect = Rect(
                        self.rect.x+x*X+gap_x/2,
                        self.rect.y + y * Y+gap_y/2,
                        X-gap_x,
                        Y-gap_y
                )

                self.bricks.append(
                    Brick(rect
                        ,
                    color))



    def check_events( self ) :
        ...


    def render( self, surface: Surface ) :
        pg.draw.rect(surface,[0,0,0],self.rect,width=3)
        for brick in self.bricks :
            brick.render(surface)

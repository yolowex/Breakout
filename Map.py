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
from Bonus import Bonus
from Brick import Brick
from CommonResources import CommonResources

now = lambda: pg.time.get_ticks() / 1000

class Map :

    def __init__( self,path:str ) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window
        self.player = CommonResources.player

        self.path = "none"
        self.name = "none"
        self.rect: Optional[Rect]= None
        self.total_gap_x = 0
        self.total_gap_y = 0

        self.colors = {}
        self.health_rows = []
        self.bonus_rows = []
        self.bricks = []
        self.bonus_list = []
        self.edge_size = 0
        self.bg = Colors.BLACK

        # self.bricks_break_sound = pg.mixer.Sound("./sounds/Block Break 2.wav")


    @property
    def ball( self ):
        return CommonResources.game.ball

    def reset( self ):
        self.path = "none"
        self.name = "none"
        self.rect: Optional[Rect] = None
        self.total_gap_x = 0
        self.total_gap_y = 0

        self.colors = {}
        self.health_rows = []
        self.bricks = []
        self.bonus_list = []
        self.edge_size = 0

    def reload( self,path:str = None ):
        if path is None: path = self.path

        self.reset()
        self.load(path)
        self.create_tiles()


    def load( self,path:str ):

        self.path = path
        f = open(path).read()
        j = json.loads(f)

        if 'edge_size' in j:
            self.edge_size = j['edge_size']

        self.ball.color = pg.color.Color(j['ball_color'])
        self.bg = pg.color.Color(j['background_color'])
        self.player.color = pg.color.Color(j['paddle_color'])
        self.player.edge = int(j['paddle_edge_size'])
        self.name = j['name']
        self.health_rows = j["health_rows"]
        self.bonus_rows = j['bonus_rows']
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
        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window
        self.player = CommonResources.player

        for brick in self.bricks:
            if brick.bonus is not None:
                brick.bonus.update()

    def create_tiles( self ) :

        Y = self.rect.height / len(self.health_rows)


        for y,row,bonus_row in zip(range(len(self.health_rows)),self.health_rows,self.bonus_rows):
            for x,health,section_id in zip(range(len(row)),row,bonus_row):
                # print(bonus,Bonus.by_number[int(bonus)])

                if health <= 0: continue

                X = self.rect.width / len(row)
                if str(health) in self.colors:
                    color = Color(self.colors[str(health)])
                else:
                    color = Colors.random_color()

                rect = Rect(
                    self.rect.x+x*X+self.total_gap_x*X/2,
                    self.rect.y+y*Y+self.total_gap_y*Y/2,
                    X-self.total_gap_x*X,
                    Y-self.total_gap_y*Y
                )
                brick = Brick(rect,color,health)

                section = Bonus.by_number[section_id]
                if section not in ['empty','none']:
                    bonus_name = r.choice(Bonus.section_dict[section])
                    brick.set_bonus(80,bonus_name=bonus_name)


                brick.edge_size = self.edge_size
                brick.font_time = now()
                self.bricks.append(brick)

    def check_events( self ) :

        brick_destroy_list = []
        bonus_destroy_list = []

        if self.bricks.__len__() == 0:
            self.events.win = True
            CommonResources.game.get_screen_shot()

        for bonus,c in zip(self.bonus_list,range(len(self.bonus_list))):
            if bonus.name == Bonus.SHRINK and (bonus.center.y - bonus.radius) > self.window.size.y:
                bonus.center.y = -bonus.radius

            elif (bonus.center.y - bonus.radius) > self.window.size.y or bonus.consumed:
                bonus_destroy_list.append(c)
            else:
                bonus.check_events()

        for c in bonus_destroy_list[::-1]:
            self.bonus_list.pop(c)

        for brick,c in zip(self.bricks,range(len(self.bricks))):
            if brick.health <= 0:
                brick_destroy_list.append(c)
                if brick.bonus is not None:
                    self.bonus_list.append(brick.bonus)


        for c in brick_destroy_list[::-1]:

            v = self.ball.volumes
            CommonResources.ball_channel.stop()
            CommonResources.ball_channel.set_volume(v[0]*0.5,v[1]*0.5)
            CommonResources.ball_channel.play(r.choice(self.assets.break_sounds))
            self.bricks.pop(c)


    def render_debug( self, surface: Surface ) :
        pg.draw.rect(surface, [0, 0, 0], self.rect, width=3)


    def render( self, surface: Surface ) :
        surface.fill(self.bg)

        for brick in self.bricks :
            brick.render(surface)

        for bonus in self.bonus_list:
            bonus.render(surface)

        if self.events.should_render_debug:
            self.render_debug(surface)




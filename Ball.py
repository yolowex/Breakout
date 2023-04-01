import Colors
import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from pygame.surface import Surface
from functions import *
from random import randint as rr

from CommonResources import CommonResources
from Colors import Colors
import math

def rotate(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

now = lambda: pg.time.get_ticks() / 1000

class Ball:
    def __init__(self,rect:Rect,color:Color,is_sub_ball:bool = False ):
        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window


        self.player = CommonResources.player
        self.map_ = CommonResources.map_
        self.game = CommonResources.game

        self.pos = Pos(rect.x,rect.y)
        self.size = Pos(rect.width,rect.height)
        self.color = color
        self.tail: list[list[Pos, float, Color]] = []  # list of tuple(center,radius,color)

        self.is_sub_ball = is_sub_ball
        self.destroyed = False
        if self.is_sub_ball:
            self.sub_balls = None
        else:
            self.sub_balls = []

        self.top_pos_distance = 50
        self.speed = 0.05

        self.angle = 180

        self.on_fire_timer = -100
        self.on_fire_duration = 7.5


    def reset( self ):
        p_rect = self.player.rect
        if self.sub_balls is not None:
            self.sub_balls.clear()

        self.tail.clear()
        self.on_fire_timer = -100

        rect = self.rect
        rect.center = p_rect.center
        rect.y = p_rect.y - rect.height
        self.pos.x,self.pos.y = rect.x,rect.y
        self.angle = r.randint(-3,3)

    @property
    def border_color( self ):
        return self.color.lerp(Colors.BLACK,0.8)

    @property
    def on_fire( self ):
        return now() <= self.on_fire_timer + self.on_fire_duration

    @property
    def fire_color( self ) :
        red = rr(225, 255)
        green = rr(0, 150)
        blue = green
        return Color(red, green, blue)

    @property
    def radius( self ):
        return self.rect.w / 2

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

        ran_factor = 1
        ran = lambda: r.randint(-ran_factor,ran_factor)
        was_swapped = False
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

        if c.y > self.window.size.y: # DOWN
            self.angle = 180

            if self.is_sub_ball:
                self.destroyed = True
            else:
                if len(self.sub_balls):
                    ball = self.sub_balls[0]
                    self.sub_balls.pop(0)
                    self.swap(ball)
                    was_swapped = True
                else:
                    if not self.events.is_dev: self.events.game_over = True
                    self.game.get_screen_shot()


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


        if not was_swapped:
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
        ran_factor = 5
        ran = lambda : r.randint(-ran_factor, ran_factor)
        c = self.center
        a = self.angle
        for brick in self.map_.bricks:

            if brick.rect.colliderect(self.rect) :
                # self.angle += 180
                if self.on_fire:
                    brick.health = 0
                    break

                vertical_bias = 'between'
                horizontal_bias = 'between'
                vertical_diff = 0
                horizontal_diff = 0

                if self.center.x >= brick.rect.x + brick.rect.width:
                    horizontal_bias = 'right'
                    horizontal_diff = abs(self.center.x - (brick.rect.x + brick.rect.width))
                if self.center.x <= brick.rect.x:
                    horizontal_bias = 'left'
                    horizontal_diff = abs(self.center.x - brick.rect.x)


                if self.center.y >= brick.rect.y + brick.rect.height:
                    vertical_bias = 'bottom'
                    vertical_diff = abs(self.center.y - (brick.rect.y + brick.rect.height))
                if self.center.y <= brick.rect.y:
                    vertical_bias = 'top'
                    vertical_diff = abs(self.center.y - brick.rect.y)

                final_bias = 'none'

                if vertical_diff > horizontal_diff:
                    final_bias = vertical_bias
                elif vertical_diff < horizontal_diff:
                    final_bias = horizontal_bias




                if final_bias == 'none':
                    if vertical_bias == 'between' and horizontal_bias =='between':
                        self.angle += 180 + r.randint(-30,30)
                        return


                if final_bias == 'top': # Ball is going down
                    if 90 <= self.angle <= 270: # if ball is going down
                        c.y = brick.rect.y - self.size.y / 2

                        if a == 90 :
                            self.angle = 89

                        if a == 180 :
                            self.angle = 0 + ran()

                        if a == 270 :
                            self.angle = 271

                        if 90 < a < 180 :
                            self.angle = 90 - abs(90 - a) + ran()

                        if 180 < a < 270 :
                            self.angle = 270 + abs(270 - a) + ran()



                if final_bias == 'bottom': # Ball is going up
                    if 270 <= self.angle <= 360 or 0<=self.angle<=90 :  # if ball is going up

                        c.y = brick.rect.y + brick.rect.height + self.size.y / 2

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

                if final_bias == 'right': # Ball is going left
                    if 180 <= self.angle <= 360 :  # if ball is going left
                        c.x = brick.rect.x+brick.rect.width+self.size.x / 2

                        if a == 180 :
                            self.angle = 179

                        if a == 270 :
                            self.angle = 90 + ran()

                        if a == 360 or a == 0 :
                            self.angle = 1

                        if 180 < a < 270 :
                            self.angle = 180 - abs(180 - a) + ran()

                        if 270 < a < 360 :
                            self.angle = abs(360 - a) + ran()


                if final_bias == 'left': # Ball is going right
                    if 0 <= self.angle <= 180 :  # if ball is going right
                        c.x = brick.rect.x - self.size.x / 2

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

                brick.hit()
                break

        self.center = c

    def ignite( self ):
        self.on_fire_timer = now()
        if not self.is_sub_ball:
            for ball in self.sub_balls:
                ball.ignite()


    def swap( self,ball ):
        self.pos = ball.pos
        self.size = ball.size
        self.color = ball.color
        self.on_fire_timer = -100
        self.angle = ball.angle

    def move( self ):

        target = self.target_point

        new_center = self.center.lerp(target,self.speed)
        self.center = new_center

        self.check_walls_collision()
        self.check_player_collision()
        self.check_map_collisions()


    def check_fire_tail_events( self ):

        c = 0
        for _, radius, _ in self.tail :
            radius *= 0.95
            self.tail[c][1] = radius
            if radius <= 0.7 :
                self.tail.pop(c)
            c += 1

        if not self.on_fire:
            return

        center = self.center
        radius = self.radius
        color = self.fire_color
        x = self.radius // 2
        noise = Pos(r.randint(-x,x),r.randint(-x,x))
        center.x += noise.x
        center.y += noise.y
        self.tail.append([center,radius,color])




    def divide( self ):
        if self.is_sub_ball:
            return

        ball_1 = Ball(self.rect,self.color,True)
        ball_1.angle = self.angle + rr(20,40)
        ball_2 = Ball(self.rect,self.color,True)
        ball_2.angle = self.angle - rr(20,40)

        self.sub_balls.extend([ball_1,ball_2])



    def check_events( self ):

        if self.events.is_dev and not self.is_sub_ball:
            if K_r in self.events.pressed_keys:
                self.ignite()

            if K_t in self.events.pressed_keys:
                self.divide()

            if K_y in self.events.held_keys:
                print(self.sub_balls.__len__())
                self.divide()


        if self.sub_balls is not None:
            for ball,c in zip(self.sub_balls,range(len(self.sub_balls))):
                if ball.destroyed:
                    self.sub_balls.pop(c)
                    break
                else:
                    ball.check_events()

        self.check_fire_tail_events()

        self.angle = self.angle % 360
        self.move()


    def render_debug( self,surface:Surface ):
        pg.draw.line(surface,self.colors.WHITE,self.center,self.target_point)
        pg.draw.rect(surface,self.color,self.rect)


    def render( self,surface:Surface ):
        if self.sub_balls is not None :
            for ball in self.sub_balls:
                ball.render(surface)

        for center,radius,color in self.tail:
            pg.draw.circle(surface,color,center,radius)

        pg.draw.circle(surface,self.color,self.center,self.radius)
        pg.draw.circle(surface,self.border_color,self.center,self.radius,width=2)

        if self.events.should_render_debug:
            self.render_debug(surface)




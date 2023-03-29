import pygame as pg
from pygame.locals import *
from functions import *

from CommonResources import CommonResources

now = lambda: pg.time.get_ticks() / 1000

class Mouse:
    def __init__(self):
        self.event_holder = CommonResources.event_holder
        pg.mouse.set_visible(False)
        self.mouse_color = pg.color.Color(0, 0, 0)
        self.mouse_radius = 10
        self.mouse_width = 1
        self.mouse_angle = 0

        self.radius_range = [self.mouse_radius*0.8,self.mouse_radius*1.2]
        self.radius_direction = 1
        self.radius_speed = 0.03

        self.mouse_timer = 0
        self.mouse_timer_interval = 1

        self.angle_direction = 1

        self.rd = 1
        self.gd = 1
        self.bd = 1
        self.rs = 1
        self.gs = 0.5
        self.bs = 1.5


    def top( self,angle=0 ) :
        pos = self.event_holder.mouse_pos.copy()
        pos.y -= (self.mouse_radius - 1)

        pos = Pos(rotate(self.event_holder.mouse_pos, pos, angle))

        return pos


    def lines( self,angle ) :
        p1 = self.top(90 + angle)
        p2 = self.top(180 + angle)
        p3 = self.top(270 + angle)
        p4 = self.top(360 + angle)

        return (p1, p3), (p2, p4)

    def check_events( self ):
        if self.event_holder.mouse_moved:
            self.mouse_timer = now()

        if now() > self.mouse_timer + self.mouse_timer_interval:
           return




        self.mouse_radius += self.radius_speed * self.radius_direction
        if self.mouse_radius > self.radius_range[1]:
            self.mouse_radius = self.radius_range[1]
            self.radius_direction *=-1
        if self.mouse_radius < self.radius_range[0]:
            self.mouse_radius = self.radius_range[0]
            self.radius_direction *=-1

        c = list(self.mouse_color)

        c[0] += self.rd * self.rs
        c[1] += self.gd * self.gs
        c[2] += self.bd * self.bs

        if c[0]>=255 or c[0]<=0:
            if c[0]>=255:
                c[0] = 255
            else:
                c[0] = 0

            self.rd *=-1


        if c[1] >= 255 or c[1] <= 0:
            if c[1] >= 255 :
                c[1] = 255
            else :
                c[1] = 0
            self.gd *=-1

        if c[2] >= 255 or c[2] <= 0 :
            if c[2] >= 255 :
                c[2] = 255
            else :
                c[2] = 0
            self.bd *=-1


        self.mouse_color = Color(c)

        if True in self.event_holder.mouse_pressed_keys:
            self.angle_direction *= -1

        self.mouse_angle += 1 * self.angle_direction


    def render( self,surface:pg.surface.Surface ):
        if now() > self.mouse_timer + self.mouse_timer_interval:
           return

        pg.draw.circle(surface, self.mouse_color, self.event_holder.mouse_pos, self.mouse_radius,
            width=self.mouse_width)

        line_a, line_b = self.lines(self.mouse_angle)
        pg.draw.line(surface, self.mouse_color, line_a[0], line_a[1])
        pg.draw.line(surface, self.mouse_color, line_b[0], line_b[1])


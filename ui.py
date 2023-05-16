import pygame as pg
from pygame.locals import *
from pygame import Vector2,Surface,Rect
from CommonResources import CommonResources as cr
from random import randint as rr
from random import uniform as ru

from Mouse import Mouse


class UI:
    def __init__(self):
        self.screen = cr.window.surface
        self.back_rect = Rect(0,0,self.screen.get_width(),15)
        self.back_color = [0,0,0,150]
        self.back_surface = Surface(self.back_rect.size).convert_alpha()
        self.trigger = False

    def check_events( self ):
        self.trigger = False

        speed = cr.event_holder.dt * 100
        noise = 5 * speed

        self.back_color[0] = ( ru(self.back_color[0]-noise,self.back_color[0]+noise))
        self.back_color[1] = ( ru(self.back_color[1]-noise,self.back_color[1]+noise))
        self.back_color[2] = ( ru(self.back_color[2]-noise,self.back_color[2]+noise))

        for c,bit in enumerate(self.back_color[:3]):
            if bit < 0:
                self.back_color[c] = 0
            elif bit > 255:
                self.back_color[c] = 255

        click = cr.event_holder.mouse_pressed_keys[0]
        m: Mouse = cr.mouse

        if m.rect.colliderect(self.back_rect) and click:
            self.trigger = True

    def render( self ):

        self.back_surface.fill(self.back_color)
        self.screen.blit(self.back_surface,self.back_rect)

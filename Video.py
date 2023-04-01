import pygame as pg
from pygame.math import Vector2 as Pos
from functions import *

from CommonResources import CommonResources as cr

class Video:
    def __init__(self,path:str,size_scale:Pos):
        self.frames = get_video_frames(path)
        self.frames.pop(0)
        self.frames.pop(-1)

        self.hopper = 0
        self.hopper_interval = 5

        self.frame_index = 0
        self.pos = Pos(0,0)
        self.size_scale = size_scale
        s = cr.window.size
        self.size = Pos(s.x * self.size_scale.x, s.y * self.size_scale.y)
        self.fix()
        self.transform()


    def fix( self ):
        for surface,c in zip(self.frames,range(len(self.frames))):
            rect = surface.get_rect()
            a = 0.04
            chop_rect = Rect(0,rect.h*(1-a),0,rect.h*a)

            new_surface = pg.transform.chop(surface,chop_rect)
            self.frames[c] = new_surface

    def transform( self ):
        for surface,c in zip(self.frames,range(len(self.frames))):

            new_surface = pg.transform.scale(surface,self.size)
            self.frames[c] = new_surface


    def check_events( self ):
        self.hopper += 1
        if self.hopper_interval == self.hopper:
            self.hopper = 0
            self.frame_index += 1
            if self.frame_index == len(self.frames):
                self.frame_index = 0

    def render( self,surface:pg.surface.Surface,rel_pos:Pos=None ):
        if rel_pos is None: rel_pos = Pos(0,0)

        pos = (self.pos.x+rel_pos.x,self.pos.y+rel_pos.y)
        surface.blit(self.frames[self.frame_index],pos)
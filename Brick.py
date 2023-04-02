import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from pygame.surface import Surface
from Bonus import Bonus

from Colors import Colors
from CommonResources import CommonResources

now = lambda : pg.time.get_ticks() / 1000


class Brick :


    def __init__( self, rect: Rect, color: Color, health ) :
        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window



        self.rect = rect
        self.color = color
        self.bonus = None
        self.health = health
        self.edge_size = 0
        self.font_time_interval = 5
        self.font_time = 0

    @property
    def sound( self ) -> pg.mixer.Sound:
        return r.choice(self.assets.hit_sounds)

    @property
    def ball( self ):
        return CommonResources.game.ball

    @property
    def mfont( self ) :
        target_color = Colors.WHITE

        if sum(self.color) > 255 * 3 * 0.5 :
            target_color = Colors.BLACK

        return self.assets.font.render(f"{self.health}", False, self.color.lerp(target_color, 0.7))


    def hit( self,gun=False ) :
        self.health -= 1
        self.font_time = now()
        v = self.ball.volumes

        if gun:
            CommonResources.gun_brick_channel.stop()
            CommonResources.gun_brick_channel.set_volume(v[0]*0.5, v[1]*0.5)
            CommonResources.gun_brick_channel.play(r.choice(self.assets.shoot_hit_sounds))


            return





        CommonResources.bricks_channel.stop()
        CommonResources.bricks_channel.set_volume(v[0],v[1])
        CommonResources.bricks_channel.play(self.sound)


    def set_bonus( self, chance_percent: int = None, bonus_name: str = None ) :
        l = []
        if chance_percent is not None :
            l = [0] * (100 - chance_percent)
            l += [1] * chance_percent

        if chance_percent is None or r.choice(l) :
            if bonus_name is None :
                bonus_name = r.choice(Bonus.names_list)

            self.bonus = Bonus(bonus_name, self.rect.center,
                min([self.rect.width, self.rect.height]) / 4, Bonus.all_[bonus_name])


    def render_font( self, surface: Surface ) :
        if not now() > self.font_time + self.font_time_interval :
            m_rect = self.rect.copy()
            m_rect.width, m_rect.height = self.mfont.get_size()
            m_rect.center = self.rect.center
            surface.blit(self.mfont, m_rect)


    def render_debug( self, surface: Surface ) :
        m_rect = self.rect.copy()
        m_rect.width, m_rect.height = self.mfont.get_size()
        m_rect.center = self.rect.center
        surface.blit(self.mfont, m_rect)


    def render( self, surface: Surface ) :
        rect = self.rect.copy()

        rect.x -= 1
        rect.y -= 1
        rect.w += 1
        rect.h += 1

        edge = self.edge_size
        pg.draw.rect(surface, self.color, rect, border_top_left_radius=edge,
            border_top_right_radius=edge, border_bottom_left_radius=edge,
            border_bottom_right_radius=edge)

        pg.draw.rect(surface, self.color.lerp(Colors.WHITE, 0.5), rect, width=2,
            border_top_left_radius=edge, border_top_right_radius=edge,
            border_bottom_left_radius=edge, border_bottom_right_radius=edge

        )

        rect.x += 2
        rect.y += 2
        rect.w -= 4
        rect.h -= 4

        pg.draw.rect(surface, self.color.lerp(Colors.BLACK, 0.3), rect, width=2,
            border_top_left_radius=edge, border_top_right_radius=edge,
            border_bottom_left_radius=edge, border_bottom_right_radius=edge

        )

        if self.events.should_render_debug :
            self.render_debug(surface)
        else :
            self.render_font(surface)

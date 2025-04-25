import pygame as pg
from settings import *

class Scope:
    def __init__(self):
        pg.mouse.set_visible(False)

        self.radius = SCOPE_RADIUS
        self.color = COLORS['scope']
        self.pos = pg.Vector2(0, 0)

    def update(self, mouse_pos):
        self.pos.update(mouse_pos)

    def draw(self, surface):
        pg.draw.line(surface, self.color, 
                     (self.pos.x - self.radius//2, self.pos.y), 
                     (self.pos.x + self.radius//2, self.pos.y),
                     2)
        pg.draw.line(surface, self.color, 
                     (self.pos.x, self.pos.y - self.radius//2), 
                     (self.pos.x, self.pos.y + self.radius//2),
                     2)
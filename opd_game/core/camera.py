import pygame as pg


class Camera():
    def __init__(self, screen_size: tuple, world_size: tuple):
        self.camera_rect = pg.Rect(0, 0, *screen_size)
        self.world_width, self.world_height = world_size

    def move_object(self, obj_rect):
        return obj_rect.move(-self.camera_rect.topleft[0], -self.camera_rect.topleft[1])
    
    def update(self, obj_rect):
        x = obj_rect.centerx - self.camera_rect.width // 2
        y = obj_rect.centery - self.camera_rect.height // 2

        x = max(0, min(x, self.world_width - self.camera_rect.width))
        y = max(0, min(y, self.world_height - self.camera_rect.height))

        self.camera_rect.topleft = (x, y)
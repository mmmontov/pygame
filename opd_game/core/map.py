import pygame as pg

class GameMap():
    def __init__(self, path):
        self.image = pg.image.load(path).convert()
        self.rect = self.image.get_rect()

    def draw(self, screen, camera_rect):
        screen.blit(self.image, (-camera_rect.x, -camera_rect.y))
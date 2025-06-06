import pygame

from pygame.sprite import Sprite

class Gun(Sprite):
    def __init__(self, screen: pygame.display):
        super(Gun, self).__init__()

        self.screen = screen
        self.image = pygame.image.load('images/gun.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom

        self.mright = False
        self.mleft = False

    def output(self):
        """"отрисовка пушки"""
        self.screen.blit(self.image, self.rect)

    def update_gun(self):
        """обновление позиции пушки"""
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += 0.7

        if self.mleft and self.rect.right > self.image.get_width():
            self.center -= 0.7

        self.rect.centerx = self.center

    def create_gun(self):
        """ращмещает пушку по центру внизу"""

        self.center = self.screen_rect.centerx
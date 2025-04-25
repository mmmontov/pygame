import pygame

from gun import Gun

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, gun: Gun):
        """создаём пулю в позиции пушки"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = (255, 222, 33)
        self.speed = 1
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """перемещение пули вверх"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """рисуем пулю"""
        pygame.draw.rect(self.screen, self.color, self.rect)


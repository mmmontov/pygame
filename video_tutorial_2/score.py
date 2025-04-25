import pygame.font

from gun import Gun
from pygame.sprite import Group

class Score():
    """вывод игровой информации"""
    def __init__(self, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        self.text_color = (139, 195, 74)
        self.font = pygame.font.SysFont(None, 36)
        self.image_score()
        self.image_best_score()
        self.image_guns()


    def image_score(self):
        """преобразование текст счёта в картинку"""
        self.score_image = self.font.render(str(self.stats.score), True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.top = 20



    def image_best_score(self):
        """преобразование лучшего счёта в картинку"""
        self.best_score_image = self.font.render(str(self.stats.best_score), True, self.text_color, (0, 0, 0))
        self.best_score_rect = self.best_score_image.get_rect()
        self.best_score_rect.centerx = self.screen_rect.centerx
        self.best_score_rect.top = 20

    def image_guns(self):
        """количество жизней"""
        self.guns = Group()
        for gun_num in range(self.stats.guns_left):
            gun = Gun(self.screen)
            gun.rect.x = 15 + gun_num*gun.rect.width
            gun.rect.y = 20
            self.guns.add(gun)

    def show_score(self):
        """вывод счёта на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.best_score_image, self.best_score_rect)
        self.guns.draw(self.screen)

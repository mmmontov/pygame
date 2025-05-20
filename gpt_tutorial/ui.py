import pygame as pg
from game_state import game_state
from settings import *

class GameUi:
    def draw_ui(self, screen):
        font = pg.font.SysFont(None, 30)
        health_text = font.render(f'HP: {game_state.player_health}', True, COLORS['text'])
        score_text = font.render(f'SCORE: {game_state.score}', True, COLORS['text'])
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (100, 10))
        
class GameOverUi:

    def __init__(self):
        self.restart_button = pg.Rect(0, 0, 200, 70)
        self.restart_button.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+70)
        


    def draw_ui(self, screen):
        screen.fill(COLORS['bg'])
        pg.mouse.set_visible(True)
        font = pg.font.SysFont(None, 100)
        game_over_text = font.render('GAME OVER', True, COLORS['text'])
        
        font = pg.font.SysFont(None, 50)
        game_score_text = font.render(f'your score: {game_state.last_game_score}', True, COLORS['text'])

        restart_button_text = font.render('restart', True, 'black')
        restart_button_text_rect = restart_button_text.get_rect(center=self.restart_button.center)

        pg.draw.rect(screen, COLORS['text'], self.restart_button, border_radius=10)
        screen.blit(restart_button_text, restart_button_text_rect)
        screen.blit(game_over_text, (SCREEN_WIDTH//3, SCREEN_HEIGHT//3))
        screen.blit(game_score_text, (SCREEN_WIDTH//3+100, SCREEN_HEIGHT//3+100))

        buttons: dict[str, pg.Rect] = {
            'restart_button': self.restart_button
        }
        return buttons
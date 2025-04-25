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
    def draw_ui(self, screen):
        font = pg.font.SysFont(None, 100)
        game_over_text = font.render('GAME OVER', True, COLORS['text'])
        
        font = pg.font.SysFont(None, 50)
        game_score_text = font.render(f'your score: {game_state.last_game_score}', True, COLORS['text'])


        screen.blit(game_over_text, (SCREEN_WIDTH//3, SCREEN_HEIGHT//3))
        screen.blit(game_score_text, (SCREEN_WIDTH//3+100, SCREEN_HEIGHT//3+100))
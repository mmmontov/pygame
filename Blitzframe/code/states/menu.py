from settings import *
from ui import *
from support import *

import pygame

class Background:
    def __init__(self, image_path, scale, screen_size, speed=20):
        bg = pygame.image.load(image_path).convert()
        size = (bg.get_width() * scale, bg.get_height() * scale)
        self.image = pygame.transform.scale(bg, size)

        self.offset = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(1, 1).normalize()
        self.speed = speed

        self.screen_rect = pygame.Rect(0, 0, *screen_size)
        self.bg_rect = self.image.get_rect()

    def draw(self, surface):
        source = pygame.Rect(self.offset.x, self.offset.y, self.screen_rect.width, self.screen_rect.height)
        surface.blit(self.image, (0, 0), source)

    def update(self, dt):
        self.offset += self.direction * self.speed * dt

        if self.offset.x <= 0:
            self.offset.x = 0
            self.direction.x *= -1
        elif self.offset.x >= self.bg_rect.width - self.screen_rect.width:
            self.offset.x = self.bg_rect.width - self.screen_rect.width
            self.direction.x *= -1

        if self.offset.y <= 0:
            self.offset.y = 0
            self.direction.y *= -1
        elif self.offset.y >= self.bg_rect.height - self.screen_rect.height:
            self.offset.y = self.bg_rect.height - self.screen_rect.height
            self.direction.y *= -1

class MainMenu:
    music_state = 'main_menu'

    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)

    def on_enter(self):
        self.create_buttons()

    def draw(self):
        self.game.background.draw(self.display_surface)
        self.game.buttons_sprites.draw(self.display_surface)

    def update(self, dt):
        self.game.background.update(dt)
        self.game.buttons_sprites.update(dt)


class Menu(MainMenu):
    
    state_name = 'main_menu'
    
    def create_buttons(self):
        # new game
        self.start_game_button = Button(
            groups=(self.game.buttons_sprites),
            pos=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3),
            text='New game',
            font=self.font,
            size=(300, 100),
            bg_color='#CA7842',
            text_color='#4B352A'
        )

        # settings
        self.settings_button = Button(
            groups=(self.game.buttons_sprites),
            pos=(self.start_game_button.rect.centerx, self.start_game_button.rect.centery + self.start_game_button.rect.height + 50),
            text='Settings',
            font=self.font,
            size=(300, 100),
            bg_color='#CA7842',
            text_color='#4B352A'
        )

        # exit game
        self.exit_button = Button(
            groups=(self.game.buttons_sprites),
            pos=(self.settings_button.rect.centerx, self.settings_button.rect.centery + self.settings_button.rect.height + 50),
            text='Exit game',
            font=self.font,
            size=(300, 100),
            bg_color='#CA7842',
            text_color='#4B352A'
        )


    def input(self):
        # keys = pygame.key.get_just_pressed()

        if self.start_game_button.is_clicked():
            self.game.change_state('gameplay')
     
        if self.settings_button.is_clicked():
            self.game.change_state('settings')

        if self.exit_button.is_clicked():
            self.game.running = False
            


    def update(self, dt):
        super().update(dt)
        self.input()
            
      
        
class Settings(MainMenu):
    state_name = 'settings'
    
    def create_buttons(self):
        
        # sounds volume
        self.sounds_volume_slider = Slider(
            groups=self.game.buttons_sprites,
            pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT//3),
            size=(300, 20),
            initial_value=self.game.sounds_volume,
            label_text='Effects volume:',
            label_font=self.font
        )
        
        # music volume 
        self.music_volume_slider = Slider(
            groups=self.game.buttons_sprites,
            pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT//3 + 100),
            size=(300, 20),
            initial_value=self.game.music_volume,
            label_text='Music volume:',
            label_font=self.font
        )
        
        # back to menu
        self.back_to_menu_button = Button(
            groups=(self.game.buttons_sprites),
            pos=(100, 70),
            text='<--',
            font=self.font,
            size=(75, 40),
            bg_color='#CA7842',
            text_color='#4B352A'
        )


    def input(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_ESCAPE] or self.back_to_menu_button.is_clicked():
            self.game.change_state('main_menu')
            self.text = 'mian_menu'
            
        
        
        self.game.sounds_volume = self.sounds_volume_slider.get_value()
        self.game.music_volume = self.music_volume_slider.get_value()

    def update(self, dt):
        super().update(dt)
        self.input()
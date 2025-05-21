from settings import *
from ui import *

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)

        

    def on_enter(self):
        self.create_buttons()

    def draw(self):
        self.display_surface.fill('#B2CD9C')
        
        self.game.buttons_sprites.draw(self.display_surface)

    def update(self, dt):
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
            self.text = 'game started'
     
        if self.settings_button.is_clicked():
            self.text = 'settings'
            self.game.change_state('settings')

        if self.exit_button.is_clicked():
            self.game.running = False
            


    def update(self, dt):
        super().update(dt)
        self.input()
            
      
        
class Settings(MainMenu):
    state_name = 'settings'
    
    def create_buttons(self):
        
        # volume
        self.volume_slider = Slider(
            groups=self.game.buttons_sprites,
            pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT//3),
            size=(300, 10),
            initial_value=self.game.volume
        )


    def input(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game.change_state('main_menu')
            self.text = 'mian_menu'
        
        self.game.volume = self.volume_slider.get_value()

    def update(self, dt):
        super().update(dt)
        self.input()
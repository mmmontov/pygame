from settings import *
from ui import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)
        self.text = 'main_menu'
        
        self.buttons = []
        self.create_buttons()
    
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
        self.buttons.append(self.start_game_button)

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
        self.buttons.append(self.settings_button)

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
        self.buttons.append(self.exit_button)
        # доделать отображение кнопок
    
    def draw(self):
        self.display_surface.fill('#B2CD9C')

        text = self.font.render(self.text, True, '#4B352A')
        self.display_surface.blit(text, (WINDOW_WIDTH/2, 0))
    
    def update(self, dt):
        # keys = pygame.key.get_just_pressed()

        if self.start_game_button.is_clicked():
            self.text = 'game started'
            print('start game click')
        
        if self.settings_button.is_clicked():
            self.text = 'settings'
            self.game.current_state = self.game.states['settings']
            # self.game.buttons_sprites.empty()
            for button in self.buttons:
                button.visible = False
            print('settings button click')

        if self.exit_button.is_clicked():
            self.game.running = False
            
        
class Settings:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)
        self.text = 'settings'

        self.create_buttons()

    def create_buttons(self):
        pass


    def draw(self):
        self.display_surface.fill('#B2CD9C')

        text = self.font.render(self.text, True, '#4B352A')
        self.display_surface.blit(text, (WINDOW_WIDTH/2, 0))
    
    def update(self, dt):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game.current_state = self.game.states['main_menu']
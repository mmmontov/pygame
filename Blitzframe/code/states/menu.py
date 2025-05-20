from settings import *
from ui import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)
        self.text = 'main_menu'
        
        self.create_buttons()
    
    def create_buttons(self):
        # new game
        self.start_game_button = Button(
            groups=(self.game.all_sprites, self.game.buttons_sprites),
            pos=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3),
            text='New game',
            font=self.font,
            size=(300, 100),
            bg_color='#CA7842',
            text_color='#4B352A'
        )
    
    
    def draw(self):
        self.display_surface.fill('#B2CD9C')

        text = self.font.render(self.text, True, '#4B352A')
        self.display_surface.blit(text, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    
    def update(self, dt):
        # keys = pygame.key.get_just_pressed()

        if self.start_game_button.is_clicked():
            self.text = 'game started'
            print('start game click')
        
        
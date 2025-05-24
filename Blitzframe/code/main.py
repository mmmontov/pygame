from settings import *

import states
import states.menu
from ui import *

class Game:
    def __init__(self):
        # game init
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Blitzframe')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # sprite groups5
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.buttons_sprites = pygame.sprite.Group()
        
        # game states
        self.states = {
            'main_menu': states.menu.Menu(self),
            'settings': states.menu.Settings(self),
        }
        self.current_state = self.states['main_menu']
        self.current_state.on_enter() 
        
        # sounds
        self.volume = 0.5
        
    def change_state(self, new_state: str):
        self.buttons_sprites.empty()
        
        self.current_state = self.states[new_state]
        self.current_state.on_enter()    


    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # update
            self.all_sprites.update(dt)
            self.current_state.update(dt)
            
            # draw
            self.display_surface.fill('black')
            self.current_state.draw()
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
            
        pygame.quit()
        

if __name__ == '__main__':
    game = Game()
    game.run()

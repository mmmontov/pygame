from settings import *

import states.gameplay
import states.menu
from tilemap import Tilemap
from ui import *
from groups import AllSprites
from support import *

class Game:
    def __init__(self):
        # game init
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Blitzframe')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_paused = False
        
        # sprite groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.buttons_sprites = pygame.sprite.Group()
        
        # game states
        self.states = {
            'main_menu': states.menu.Menu(self),
            'settings': states.menu.Settings(self),
            'gameplay': states.gameplay.Gameplay(self),
            'pause': states.gameplay.Pause(self, 'Pause'),
        }
        self.current_state = self.states['main_menu']
        self.current_state.on_enter() 
        
        # tilemap
        self.tilemap = Tilemap(self.all_sprites, self.collision_sprites)
        self.tilemap.setup()
        
        # load assets
        self.load_assets()
        
        # sounds
        self.volume = 0.5
        
    def change_state(self, new_state: str, animation=True):
        def state_func():
            self.buttons_sprites.empty()
            self.current_state = self.states[new_state]
            self.current_state.on_enter()    
        if animation:
            transition_effect(
                    surface=self.display_surface,
                    callback=state_func,
                    draw_callback=lambda: self.current_state.draw())
        else:
            state_func()
        

    def load_assets(self):
        # graphics 
        self.player_frames = folder_importer('images', 'player', 'down')

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # update
            if not self.game_paused:
                self.all_sprites.update(dt)
            self.current_state.update(dt)
            
            # draw
            self.display_surface.fill('black')
            self.current_state.draw()
            
            pygame.display.update()
            
        pygame.quit()
        

if __name__ == '__main__':
    game = Game()
    game.run()

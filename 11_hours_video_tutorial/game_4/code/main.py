from settings import *

from groups import *
from tilemap import Tilemap
from support import *
from sprites import *
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True
        
        
        # groups
        self.all_sprites = AllSprites()
        self.collisions_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        # load game 
        self.load_assets()
        
        # tilemap
        self.tilemap = Tilemap(self.all_sprites, self.collisions_sprites, self.player_frames)
        self.tilemap.setup()
        self.player = Player(self.all_sprites, self.tilemap.player_spawner(), self.collisions_sprites, self.player_frames, self.create_bullet)

        self.worm_spawners = self.tilemap.worm_spawner()
        self.create_worm()
        
        # timers
        self.bee_timer = Timer(600, func=self.create_bee, autostart=True, repeat=True)

        # audio
        self.audio['music'].play(loops = -1)
        self.audio['music'].set_volume(0.01)

    
    def create_bee(self):
        Bee((self.all_sprites, self.enemy_sprites), 
            (self.tilemap.level_width + WINDOW_WIDTH, 
             randint(0, self.tilemap.level_heigt)), 
             self.bee_frames)
        
    def create_worm(self):
        for spawner in self.worm_spawners:
            borders = (spawner.x, spawner.x + spawner.width)
            Worm((self.all_sprites, self.enemy_sprites), pygame.FRect(spawner.x, spawner.y, spawner.width, spawner.height), self.worm_frames)
            
        
    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 10 + self.bullet_surf.get_width() if direction == 1 else pos[0] + direction * 10 - self.bullet_surf.get_width()
        y = pos[1] + 10
        Bullet((self.all_sprites, self.bullet_sprites), (x, y), self.bullet_surf, direction)
        Fire(self.all_sprites, pos, self.fire_surf, self.player)
        self.audio['shoot'].play()
    
    def load_assets(self):
        # graphics 
        self.player_frames = import_folder('images', 'player')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')
        
        # audio
        self.audio = import_audio('audio')
        
        
    def collision(self):
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()
                    
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = True
        
    def run(self):
        dt = self.clock.tick(FRAMERATE) / 10000
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            # update
            self.all_sprites.update(dt)
            self.bee_timer.update()
            self.collision()
        
            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()
        
        
if __name__ == '__main__':
    game = Game()
    game.run()
        
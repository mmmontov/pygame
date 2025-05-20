from settings import *

from sprites import *

class Tilemap:
    def __init__(self, all_sprites, collision_sprites, player_frames):
        self.player_frames = player_frames
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.level_width = self.map.width * TILE_SIZE
        self.level_heigt = self.map.height * TILE_SIZE
        
    
    def player_spawner(self) -> tuple[int]:
        for obj in self.map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                return (obj.x, obj.y)
            
    def worm_spawner(self):
        spawners = []
        for obj in self.map.get_layer_by_name('Entities'):
            if obj.name == 'Worm':
                spawners.append(obj)
        return spawners
            
    def setup(self):
        for x, y, image in self.map.get_layer_by_name('Decoration').tiles():
            Sprite(self.all_sprites, (x*TILE_SIZE, y*TILE_SIZE), image)
        for x, y, image in self.map.get_layer_by_name('Main').tiles():
            Sprite((self.all_sprites, self.collision_sprites), (x*TILE_SIZE, y*TILE_SIZE), image)
        
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
        
        
    def draw(self, target_pos):
        # return super().draw(surface)
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH // 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT // 2)
        
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        objects_sprites =  sorted([sprite for sprite in self if not hasattr(sprite, 'ground')], key=lambda x: x.rect.centery)
        # sorted_sprites = sorted(objects_sprites, key=lambda x: x.rect.centery)
        for sprite in ground_sprites + objects_sprites:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
            
            
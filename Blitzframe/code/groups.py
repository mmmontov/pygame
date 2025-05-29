from settings import *
from support import Timer

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
        self.camera_speed = 0.1 

    def draw(self, target_pos):
        target_offset = pygame.Vector2()
        target_offset.x = -(target_pos[0] - WINDOW_WIDTH // 2)
        target_offset.y = -(target_pos[1] - WINDOW_HEIGHT // 2)

        # Плавное движение камеры
        self.offset += (target_offset - self.offset) * self.camera_speed

        # Отрисовка
        gun_sprite = [sprite for sprite in self if hasattr(sprite, 'gun')]
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        objects_sprites = sorted([sprite for sprite in self if not hasattr(sprite, 'ground')], key=lambda x: x.rect.centery)

        for sprite in ground_sprites + objects_sprites:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
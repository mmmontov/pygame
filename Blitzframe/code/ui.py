from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, groups, pos: tuple[int], text: str, font: pygame.Font, size=(200, 50), 
                 bg_color='white', text_color='black'):
        super().__init__(groups)
        self.pos = pos
        self.size = size
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.visible = True
        
        self.image = pygame.Surface(size)
        self.rect = self.image.get_frect(center = pos)
        
        self.render_text()
        


    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_just_pressed()
        return self.rect.collidepoint(mouse_pos) and mouse_buttons[0]
     
        
    def render_text(self):
        if self.visible:
            self.image.fill(self.bg_color)
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_frect(center=(self.size[0]/2, self.size[1]/2))
            self.image.blit(text_surf, text_rect)
        
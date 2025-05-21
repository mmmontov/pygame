from settings import *

        
        
class Button(pygame.sprite.Sprite):
    def __init__(self, groups, pos: tuple[int], text: str, font: pygame.Font, size=(200, 50), 
                 bg_color='white', text_color='black'):
        super().__init__(groups)
        self.pos = pos
        self.width = size[0]
        self.height = size[1]
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
            text_rect = text_surf.get_frect(center=(self.width/2, self.height/2))
            self.image.blit(text_surf, text_rect)


class Slider(pygame.sprite.Sprite):
    def __init__(self, groups, pos: tuple[int], size=(200, 10), 
                 min_value=0.0, max_value=1.0, initial_value=0.5,
                 color_bg='#cccccc', color_fg='#CA7842', handle_color='#4B352A'):
        super().__init__(groups)

        # параметры
        self.pos = pos
        self.width = size[0]
        self.height = size[1]
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.color_bg = color_bg
        self.color_fg = color_fg
        self.handle_color = handle_color

        # поверхность и прямоугольник
        self.image = pygame.Surface((self.width, self.height + 10), pygame.SRCALPHA)
        self.rect = self.image.get_frect(center=pos)

        # внутреннее состояние
        self.dragging = False

        self.update_slider()

    def update_slider(self):
        self.image.fill((0, 0, 0, 0))  # очистка с прозрачностью

        # координаты прогресса
        progress_width = int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width)

        # фон
        pygame.draw.rect(self.image, self.color_bg, (0, self.height // 2, self.width, self.height), border_radius=5)
        # активная часть
        pygame.draw.rect(self.image, self.color_fg, (0, self.height // 2, progress_width, self.height), border_radius=5)
        # ползунок
        pygame.draw.circle(self.image, self.handle_color, (progress_width, self.height // 2 + self.height // 2), 8)

    def get_value(self):
        return self.value

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.dragging and not mouse_pressed[0]:
            self.dragging = False

        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.dragging = True

        if self.dragging:
            rel_x = mouse_pos[0] - self.rect.left
            rel_x = max(0, min(self.width, rel_x))
            self.value = self.min_value + (rel_x / self.width) * (self.max_value - self.min_value)
            self.update_slider()


    def update(self, dt):
        self.input()
from settings import *

def import_image(*path, format = 'png', alpha = True):
    full_path = join(*path) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

def import_folder(*path):
    frames = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in sorted(file_names, key=lambda x: int(x.split('.')[0])):
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
            
    return frames

def import_audio(*path):
    # audio = pygame.mixer.Sound(full_path)
    # return audio

    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(full_path)
    return audio_dict


class Timer:
    def __init__(self, duration, func = None, repeat = False, autostart = False):
        self.duration = duration
        self.start_time = 0
        self.func = func
        self.active = False
        self.repeat = repeat
        if autostart:
            self.activate()
        
    def __bool__(self):
        return self.active
        
    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        
    def deactivate(self):
        self.active = False
        self.start_time = 0    
        if self.repeat:
            self.activate()
    
    def update(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()
            
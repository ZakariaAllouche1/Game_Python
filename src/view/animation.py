import pygame

from src.settings import Settings


class Animation:
    def __init__(self, name, x, y, frame_width, frame_height, animation_speed, sprite_conf):
        self.sprite_sheet = pygame.image.load(f'../media/spritesheets/{name}.png')
        self.x = x
        self.y = y
        self.frames = []
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(self.x + (self.rect.width * 0.7) / 4, self.y + (self.rect.height * 0.75),
                                0.45 * self.rect.width, 0.15 * self.rect.height)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.type = 'idle'
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.time_since_last_frame = 0
        self.frames = self.extract_frames(self.sprite_sheet, 8, 3)
        self.sprite_conf = sprite_conf
        self.state = 'idle'

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image

    def get_image(self, x, y):
        # TODO automatiser selon les sizes des spritesheets des différents héros : homogéniser
        image = pygame.Surface([120, 120])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 120, 120))
        # return pygame.transform.scale(image, (int(image.get_width() * 0.7), int(image.get_height() * 0.7)))
        return image

    def extract_frames(self, sprite_sheet, num_cols, num_rows, start_col=0, start_row=0):
        frames = []
        w, h = sprite_sheet.get_size()
        frame_width = w / num_cols
        frame_height = h / num_rows
        if frame_width > 120:
            frame_width = 120
        if frame_height > 120:
            frame_height = 120
        for j in range(start_row, num_rows):
            for i in range(start_col, num_cols):
                x = i * frame_width
                y = j * frame_height
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self, dt, orientation='right'):
        if self.state == 'dead':
            self.frame_index = 0
            self.__image = self.frames[self.sprite_conf.get_indexes('dead').get('dead')[self.frame_index]]
            if orientation == 'left':
                self.image = pygame.transform.flip(self.__image, True, False)
        else:
            self.time_since_last_frame += dt
            if self.time_since_last_frame >= self.animation_speed:
                if self.state == 'movement' or self.state == 'idle':
                    self.frame_index = (self.frame_index + 1) % len(self.sprite_conf.get_indexes(self.state).get(self.type))
                else :
                    self.frame_index = self.frame_index + 1
                    if self.frame_index >= len(self.sprite_conf.get_indexes(self.state).get(self.type)):
                        self.frame_index = 0
                        self.time_since_last_frame = 0
                        self.state = 'idle'
                        self.type = 'idle'
                        return True
                self.__image = self.frames[self.sprite_conf.get_indexes(self.state).get(self.type)[self.frame_index]]
                if orientation == 'left':
                    self.image = pygame.transform.flip(self.__image, True, False)
                self.time_since_last_frame = 0
        return False

    def get_walkable_tiles(self, movement_range):
        settings = Settings()
        vertical, horizontal, diagonal = movement_range

        # Calculer le centre du sprite
        center_x = self.rect.x + self.rect.width / 2
        center_y = self.rect.y + self.rect.height / 2

        # Convertir le centre en coordonnées de tile
        tile_x = int(center_x / (settings.tile_width * settings.zoom))
        tile_y = int(center_y / (settings.tile_width * settings.zoom))

        walkable_tiles = []

        # Mouvement vertical
        for dy in range(-vertical, vertical + 1):
            walkable_tiles.append((tile_x, tile_y + dy))

        # Mouvement horizontal
        for dx in range(-horizontal, horizontal + 1):
            walkable_tiles.append((tile_x + dx, tile_y))

        # Mouvement diagonal
        for d in range(-diagonal, diagonal + 1):
            if d != 0:
                walkable_tiles.append((tile_x + d, tile_y + d))
                walkable_tiles.append((tile_x + d, tile_y - d))

        return walkable_tiles
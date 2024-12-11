import pygame

from src.view.effect import Effect


class Animation:
    def __init__(self, name, x, y, frame_width, frame_height, animation_speed, sprite_conf):
        self.sprite_sheet = pygame.image.load(f'../media/spritesheets/{name}.png')
        self.x = x
        self.y = y
        self.frames = []
        # self.orientation = 'right'
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(self.x + (self.rect.width * 0.7) / 4, self.y + (self.rect.height * 0.75),
                                0.45 * self.rect.width, 0.15 * self.rect.height)
        self.frame_width = frame_width
        self.frame_height = frame_height
        # self.num_frames = num_frames
        self.type = 'idle'
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.time_since_last_frame = 0
        self.frames = self.extract_frames(self.sprite_sheet, frame_width, frame_height, 8, 3)
        self.sprite_conf = sprite_conf
        self.state = 'idle'
        # self.effects = {}
        # self.set_effects()
        # self.current_effect = None
        # self.effect_frames = None
        # self.effect_x = None
        # self.effect_y = None
        # self.effect_image = None
        # self.effect_index = 0
        # self.time_since_last_effect = 0
        # self.effect = Effect(self.sprite_conf, self.animation_speed)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image

    # @property
    # def effect_image(self):
    #     return self.effect.effect_image

    def get_image(self, x, y):
        # TODO automatiser selon les sizes des spritesheets des différents héros : homogéniser
        image = pygame.Surface([120, 120])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 120, 120))
        # return pygame.transform.scale(image, (int(image.get_width() * 0.7), int(image.get_height() * 0.7)))
        return image

    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_cols, num_rows, start_col=0, start_row=0):
        frames = []
        for j in range(start_row, num_rows):
            for i in range(start_col, num_cols):
                x = i * frame_width
                y = j * frame_height
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                pygame.transform.scale(frame, (int(frame.get_width() * 0.7), int(frame.get_height() * 0.7)))
                frames.append(frame)
        return frames

    def update(self, dt, orientation='right'):
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.animation_speed:
            if self.state == 'movement' or self.state == 'idle' or self.state == 'dead':
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

    # def apply_effect(self, type, frame_width, frame_height, num_cols, num_rows, end, clock, screen, map, player):
    #
    #     # Extraire les frames de l'animation
    #     anim = self.extract_frames(self.effects[type], frame_width, frame_height, num_cols, num_rows)  # 5 lignes, 6 colonnes
    #
    #     frame_index = 0
    #     animation_speed = 0.1  # Temps entre frames (en secondes)
    #     time_since_last_frame = 0
    #     dt = clock.tick(60) / 1000  # Temps écoulé depuis la dernière frame
    #
    #     # Calcul des positions d'interpolation
    #     _X = np.linspace(self.x, end[0], len(anim))
    #     _Y = np.linspace(self.y, end[1], len(anim))
    #
    #     running = True
    #     while running:
    #
    #         # Mise à jour du temps écoulé entre les frames
    #         dt = clock.tick(60) / 1000
    #         time_since_last_frame += dt
    #
    #         # Avancer dans l'animation si temps définit écoulé
    #         if time_since_last_frame >= animation_speed:
    #             time_since_last_frame = 0
    #             frame_index += 1
    #             if frame_index >= len(anim):  # Fin de l'animation
    #                 running = False
    #
    #         map.group.update()
    #         map.update(player)
    #         player.draw(screen)
    #         pygame.display.flip()
    #
    #         # Afficher la frame courante à la bonne position
    #         if frame_index < len(anim):
    #             screen.blit(anim[frame_index], (_X[frame_index], _Y[frame_index]))
    #
    #         # Rafraîchir l'écran
    #         pygame.display.flip()
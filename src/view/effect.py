import numpy as np
import pygame


class Effect:

    def __init__(self, sprite_conf, animation_speed):
        self.sprite_conf = sprite_conf
        self.effects = {}
        self.set_effects()
        self.current_effect = None
        self.effect_frames = []
        self.effect_x = []
        self.effect_y = []
        self.effect_image = None
        self.__effect_index = 0
        self.type = None
        self.time_since_last_effect = 0
        self.animation_speed = animation_speed

    def set_effects(self):
        for effect_name in self.sprite_conf.effects.keys():
            self.effects[effect_name] = pygame.image.load(f'../media/spritesheets/{effect_name}.png') # Loading effects sheets

    # TODO exec mais animation frozen on 0
    def apply_effect(self, dt, orientation='right'):
        if self.current_effect is not None and self.effect_x is not None and self.effect_y is not None:
            self.time_since_last_effect += dt
            if self.time_since_last_effect >= self.animation_speed:
                self.time_since_last_effect = 0
                self.__effect_index += 1
                if self.__effect_index >= len(self.effect_frames):
                    self.__effect_index = 0
                    self.time_since_last_effect = 0
                    self.current_effect = None
                    # self.effect_frames = []
                    # self.effect_x = []
                    # self.effect_y = []
                    # self.effect_image = None
                    return False
                self.effect_image = self.effect_frames[self.__effect_index]
                if orientation == 'left':
                    self.effect_image = pygame.transform.flip(self.effect_image, True, False)
            return True
        return False

    # def apply_effect(self, dt, orientation='right'):
    #     if not self.effect_frames:
    #         print("Erreur : Aucune frame disponible pour l'effet.")
    #         return False
    #
    #     self.time_since_last_effect += dt
    #     print(
    #         f"Time Accumulator: {self.time_since_last_effect}, Animation Speed: {self.animation_speed}, Current Index: {self.effect_index}")
    #
    #     if self.time_since_last_effect >= self.animation_speed:
    #         self.time_since_last_effect = 0
    #         self.effect_index += 1
    #         # TODO remplacer par len(self.sprite_conf.get_indexes(self.state).get(self.type))
    #         if self.effect_index >= len(self.effect_frames):
    #             print(f"Fin de l'animation à l'index {self.effect_index}.")
    #             self.effect_index = 0  # Réinitialisez ou arrêtez l'effet
    #             self.current_effect = None
    #             self.effect_image = None
    #             return False
    #         self.effect_image = self.effect_frames[self.effect_index]
    #         if orientation == 'left' :
    #             self.effect_image = pygame.transform.flip(self.effect_image, True, False)
    #         print(f"Frame changée : Index={self.effect_index}, Image={self.effect_image}")
    #     return True

    def update(self, x, y, type, target_pos=None):
        if self.current_effect is None:
            self.type = type
            self.current_effect = self.sprite_conf.effects[type]
            self.effect_frames = self.extract_frames(
                self.effects[type],
                self.current_effect[3],
                self.current_effect[3],
                self.current_effect[0],
                self.current_effect[1],
            )

            if self.current_effect[2] and target_pos is not None:
                self.effect_x = np.linspace(x, target_pos[0], len(self.effect_frames))
                self.effect_y = np.linspace(y, target_pos[1], len(self.effect_frames))
            else:
                self.effect_x = [x]
                self.effect_y = [y]
            print(f"Interpolation X: {self.effect_x}, Y: {self.effect_y}")
            self.__effect_index = 0
            self.time_since_last_effect = 0
            self.effect_image = self.effect_frames[self.__effect_index]

    def draw(self, screen):
        if self and self.effect_image is not None:
            print(
                f"Rendering frame index: {self.__effect_index} at position ({self.effect_x[self.__effect_index % len(self.effect_x)]}, {self.effect_y[self.__effect_index  % len(self.effect_x)]})")
            screen.blit(self.effect_image, (self.effect_x[self.__effect_index  % len(self.effect_x)], self.effect_y[self.__effect_index  % len(self.effect_x)]))
            # screen.blit(self.effect_image, (100, 100))
    #         % len(self.effect_x)

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

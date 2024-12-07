import pygame
import numpy as np

class Animation:

    def __init__(self):
        pass

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

    # TODO automatiser pour les attaques similaires (à définir selon les images)
    def attaque_titania(self, start, end, clock, screen, map, player):
        # Charger la spritesheet
        sprite_sheet = pygame.image.load('../media/spritesheets/attaque_titania.png').convert_alpha()

        # Extraire les frames de l'animation
        anim = self.extract_frames(sprite_sheet, 190, 190, 5, 6)  # 5 lignes, 6 colonnes

        frame_index = 0
        animation_speed = 0.1  # Temps entre frames (en secondes)
        time_since_last_frame = 0
        dt = clock.tick(60) / 1000  # Temps écoulé depuis la dernière frame

        # Calcul des positions d'interpolation
        _X = np.linspace(start[0], end[0], len(anim))
        _Y = np.linspace(start[1], end[1], len(anim))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Mise à jour du temps écoulé entre les frames
            dt = clock.tick(60) / 1000
            time_since_last_frame += dt

            # Avancer dans l'animation si temps définit écoulé
            if time_since_last_frame >= animation_speed:
                time_since_last_frame = 0
                frame_index += 1
                if frame_index >= len(anim):  # Fin de l'animation
                    running = False

            map.group.update()
            map.update(player)
            player.draw(screen)
            pygame.display.flip()

            # Afficher la frame courante à la bonne position
            if frame_index < len(anim):
                screen.blit(anim[frame_index], (_X[frame_index], _Y[frame_index]))

            # Rafraîchir l'écran
            pygame.display.flip()
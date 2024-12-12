import math

import pygame

class Menu:

    def __init__(self):
        pass

    @staticmethod
    def start():
        # Initialisation
        is_running = True
        pressed = False

        # Configuration
        icon = pygame.image.load('../../media/UI/icon.png')
        pygame.display.set_icon(icon)
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Résolution explicite pour tester
        banner = pygame.image.load('../../media/UI/banner.jpg')
        banner = pygame.transform.scale(banner, screen.get_size())
        pygame.display.set_caption("Strategy Game")

        # Charger et vérifier le bouton
        try:
            play_button = pygame.image.load('../../media/UI/play_button.png')
            play_button_pressed = play_button.subsurface(pygame.Rect(play_button.get_width()/2, play_button.get_height()/2, play_button.get_width()/2, play_button.get_height()/2))
            play_button = play_button.subsurface(pygame.Rect(0, play_button.get_height()/2, play_button.get_width()/2, play_button.get_height()/2))
            play_button = pygame.transform.scale(play_button, (250, 100))
            play_button_rect = play_button.get_rect()
            play_button_rect.x = math.ceil(screen.get_width()/2.5)
            play_button_rect.y = math.ceil(screen.get_height()/2)
            play_button_pressed = pygame.transform.scale(play_button_pressed, (250, 100))
        except pygame.error as e:
            print(f"Erreur lors du chargement du bouton : {e}")
            return

        while is_running:
            # Afficher le background et le bouton
            screen.blit(banner, (0, 0))
            if not pressed :
                screen.blit(play_button, play_button_rect)  # Position visible pour tester
            else:
                screen.blit(play_button_pressed, play_button_rect)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        screen.blit(play_button_pressed, play_button_rect)
                        pressed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:  # Fin du jeu
                        is_running = False

            pygame.display.flip()
            # clock.tick(60)  # Limite à 60 FPS

        pygame.quit()


Menu.start()

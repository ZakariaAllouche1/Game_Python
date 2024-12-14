import math

import pygame

# from src.controller.menu_handler import MenuHandler
from src.settings import Settings


class Menu:

    def __init__(self):
        self.settings = Settings()
        pass


    def start(self, menu_handler):
        pygame.init()

        # Initialisation
        is_running = True
        pressed = False

        # Configuration
        icon = pygame.image.load('../../media/UI/icon.png')
        banner = pygame.image.load('../../media/UI/banner.png')

        pygame.display.set_icon(icon)
        pygame.display.set_caption("Strategy Game")
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Résolution explicite pour tester
        banner = pygame.transform.scale(banner, screen.get_size())

        self.menu(pressed, screen, banner, menu_handler)

        pygame.quit()


    def menu(self, pressed, screen, banner, menu_handler):
        # Charger et vérifier le bouton
        is_running = True
        clock = pygame.time.Clock()

        try:
            play_button, play_button_rect = self.settings.create_ui_element('play_button', (250, 100), math.ceil(screen.get_width() / 2.5), math.ceil(screen.get_height() / 3))

            settings_button, settings_button_rect = self.settings.create_ui_element('settings_button', (250, 100), math.ceil(screen.get_width() / 2.5), play_button_rect.y + 10)
            settings_button_rect.y += settings_button_rect.height

            exit_button, exit_button_rect = self.settings.create_ui_element('exit_button', (250, 100), math.ceil(screen.get_width() / 2.5), settings_button_rect.y + settings_button_rect.height + 10)

        except pygame.error as e:
            print(f"Erreur lors du chargement du bouton : {e}")
            return

        while is_running:
            # Afficher le background et le bouton
            screen.blit(banner, (0, 0))
            if not pressed:
                screen.blit(play_button, play_button_rect)  # Position visible pour tester
                screen.blit(settings_button, settings_button_rect)  # Position visible pour tester
                screen.blit(exit_button, exit_button_rect)  # Position visible pour tester

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        self.choose_player(screen, banner, menu_handler)
                    elif settings_button_rect.collidepoint(event.pos):
                        print("PRESSED SETTINGS")
                    elif exit_button_rect.collidepoint(event.pos):
                        is_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:  # Fin du jeu
                        is_running = False

            pygame.display.flip()
            clock.tick(60)  # Limite à 60 FPS


    def choose_player(self, screen, banner, menu_handler):
        # Initialization
        is_running = True
        active = False
        font = pygame.font.Font(None, 36)
        text = ""  # Text entered by the user

        # Input Box Configuration
        try:
            input_button = pygame.image.load('../../media/UI/input.png')
            input_button = pygame.transform.scale(input_button, (400, 150))
            input_rect = input_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))

            placeholder, placeholder_rect = self.settings.create_ui_element('placeholder', (400, 45), input_rect.x, input_rect.y - 10)

            erza_avatar, erza_rect = self.settings.create_ui_element('erza_avatar', (200, 300), 80, input_rect.y + input_rect.height + 10)

            gray_avatar, gray_rect = self.settings.create_ui_element('gray_avatar', (200, 300), 320, input_rect.y + input_rect.height + 10)

            natsu_avatar, natsu_rect = self.settings.create_ui_element('natsu_avatar', (200, 300), 560, input_rect.y + input_rect.height + 10)

            gowther_avatar, gowther_rect = self.settings.create_ui_element('gowther_avatar', (200, 300), 800, input_rect.y + input_rect.height + 10)

            heisuke_avatar, heisuke_rect = self.settings.create_ui_element('heisuke_avatar', (200, 300), 1040, input_rect.y + input_rect.height + 10)

            kansuke_avatar, kansuke_rect = self.settings.create_ui_element('kansuke_avatar', (200, 300), 1280, input_rect.y + input_rect.height + 10)

            ok_button = pygame.image.load('../../media/UI/ok_button.png')
            ok_button = pygame.transform.scale(ok_button, (200, 75))
            ok_rect = ok_button.get_rect(center=(screen.get_width() / 2, 3 * screen.get_height() / 4))

        except pygame.error as e:
            print(f"Error loading button image: {e}")
            return

        # Clock for controlling frame rate
        clock = pygame.time.Clock()

        while is_running:
            # Drawing Elements
            screen.blit(banner, (0, 0))
            screen.blit(input_button, input_rect)
            screen.blit(placeholder, placeholder_rect)

            # Create and center the overlay
            overlay_color = (0, 255, 0, 128) if active else (255, 0, 0, 128)
            overlay_surface = pygame.Surface((input_rect.width - 40, input_rect.height - 80), pygame.SRCALPHA)
            overlay_surface.fill(overlay_color)
            overlay_x = input_rect.x + 20
            overlay_y = input_rect.y + 40
            screen.blit(overlay_surface, (overlay_x, overlay_y))

            screen.blit(erza_avatar, erza_rect)
            # overlay_erza = pygame.Surface((erza_avatar.get_rect().width, erza_avatar.get_rect().height), pygame.SRCALPHA)
            # overlay_erza.fill(overlay_color)
            # screen.blit(overlay_erza, (erza_rect.x, erza_rect.y))

            screen.blit(gray_avatar, gray_rect)
            screen.blit(natsu_avatar, natsu_rect)
            screen.blit(gowther_avatar, gowther_rect)
            screen.blit(heisuke_avatar, heisuke_rect)
            screen.blit(kansuke_avatar, kansuke_rect)

            screen.blit(ok_button, ok_rect)

            # Render text
            text_surface = font.render(text, True, (255, 255, 255))  # White text
            screen.blit(text_surface, (overlay_x, overlay_y))

            for x, y in zip(menu_handler.x, menu_handler.y):
                screen.blit(pygame.image.load("../../media/UI/selected.png"), (x, y))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:  # Fin du jeu
                        is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Activate input box if clicked
                    active = input_rect.collidepoint(event.pos)

                menu_handler.select_units(event, erza_rect, gray_rect, natsu_rect, gowther_rect, kansuke_rect,
                                 heisuke_rect)

                text, active = menu_handler.get_player_name(event, input_rect, text, active)

                new_text = menu_handler.submit(event, ok_rect)
                if new_text is not None:
                    if new_text != "end":
                        text = new_text
                    else:
                        is_running = False


            pygame.display.flip()
            clock.tick(60)  # Limit frame rate to 60 FPS


    def display_settings(self):
        pass

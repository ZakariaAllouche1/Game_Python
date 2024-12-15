import math

import pygame

from src.controller.player_handler import PlayerHandler
from src.settings import Settings


class MenuHandler:

    def __init__(self):
        self.current_player = None
        self.set_player = True
        self.selected_units = {}
        self.settings = Settings()
        self.x, self.y = [], []
        pass

    def select_units(self, event, erza_rect, gray_rect, natsu_rect, gowther_rect, kansuke_rect, heisuke_rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected = None
            x, y = None, None
            if erza_rect.collidepoint(event.pos):
                selected = 'Erza'
                x, y = erza_rect.x + (erza_rect.w/2) - 20, erza_rect.y + erza_rect.h - 25
            elif gray_rect.collidepoint(event.pos):
                selected = 'Gray'
                x, y = gray_rect.x + gray_rect.w/2 - 20, gray_rect.y + gray_rect.h - 25
            elif natsu_rect.collidepoint(event.pos):
                selected = 'Natsu'
                x, y = natsu_rect.x + natsu_rect.w/2 - 20, natsu_rect.y + natsu_rect.h - 25
            elif gowther_rect.collidepoint(event.pos):
                selected = 'Gowther'
                x, y = gowther_rect.x + gowther_rect.w/2 -20, gowther_rect.y + gowther_rect.h - 25
            elif kansuke_rect.collidepoint(event.pos):
                selected = 'Kansuke'
                x, y = kansuke_rect.x + kansuke_rect.w/2 - 20, kansuke_rect.y + kansuke_rect.h - 25
            elif heisuke_rect.collidepoint(event.pos):
                selected = 'Heisuke'
                x, y = heisuke_rect.x + heisuke_rect.w / 2 - 20, heisuke_rect.y + heisuke_rect.h -25
            if selected is not None:
                if self.current_player in self.selected_units:
                    if not selected in self.selected_units[self.current_player]:
                        if len(self.selected_units[self.current_player]) < self.settings.nb_units_per_player:
                            self.selected_units[self.current_player].append(selected)
                            if x is not None and y is not None:
                                self.x.append(x)
                                self.y.append(y)
                    else:
                        self.selected_units[self.current_player].remove(selected)
                        if x is not None and y is not None:
                            if x in self.x:
                                self.x.remove(x)
                            if y in self.y:
                                self.y.remove(y)
                else:
                    print("Veuillez d'abord saisir un nom d'utilisateur")


    def get_player_name(self, event, input_rect, text, active):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activate input box if clicked
            active = input_rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and active and self.set_player:
            if event.key == pygame.K_RETURN:
                self.current_player = text
                if not self.current_player in self.selected_units:
                    self.selected_units[self.current_player] = []
                    self.set_player = False
                else:
                    print("Name already used")
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]  # Remove the last character
            else:
                text += event.unicode  # Add typed character
        return text, active


    def submit(self, event, ok_rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ok_rect.collidepoint(event.pos):
                # Vérifie si toutes les unités sélectionnées répondent aux conditions
                all_three_selected = all(len(units) == 3 for units in self.selected_units.values())

                if len(self.selected_units) == 2 and all_three_selected:
                    self.set_player = False
                    self.x, self.y = [], []
                    return "end"

                if len(self.selected_units) == 1 and all_three_selected:
                    self.set_player = True
                    print(len(self.selected_units) == 1, all_three_selected)
                    self.x, self.y = [], []
                    return ""

                self.set_player = True

        # print(self.current_player, self.selected_units)
        return None

    def start(self, clock):
        pygame.init()
        pressed = False

        # Configuration
        icon = pygame.image.load('../../media/UI/icon.png')
        banner = pygame.image.load('../../media/UI/banner.png')

        pygame.display.set_icon(icon)
        pygame.display.set_caption("Strategy Game")
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Résolution explicite pour tester
        banner = pygame.transform.scale(banner, screen.get_size())

        self.menu(pressed, banner, clock, screen)

        pygame.quit()


    def menu(self, pressed, banner, clock, screen):
        # Charger et vérifier le bouton
        is_running = True

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
                        self.choose_player(screen, banner)
                        is_running = False
                        # return self.selected_units
                    elif settings_button_rect.collidepoint(event.pos):
                        print("PRESSED SETTINGS")
                    elif exit_button_rect.collidepoint(event.pos):
                        is_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:  # Fin du jeu
                        is_running = False

            pygame.display.flip()
            clock.tick(60)  # Limite à 60 FPS


    def choose_player(self, screen, banner):
        # Initialization
        is_running = True
        active = False
        font = pygame.font.Font('../media/EagleLake-Regular.ttf', 30)
        text = ""

        try:
            input_button = pygame.image.load('media/UI/input.png')
            input_button = pygame.transform.scale(input_button, (400, 150))
            input_rect = input_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))

            placeholder, placeholder_rect = self.settings.create_ui_element('placeholder', (400, 45), input_rect.x, input_rect.y - 10)

            erza_avatar, erza_rect = self.settings.create_ui_element('erza_avatar', (200, 300), 80, input_rect.y + input_rect.height + 10)

            gray_avatar, gray_rect = self.settings.create_ui_element('gray_avatar', (200, 300), 320, input_rect.y + input_rect.height + 10)

            natsu_avatar, natsu_rect = self.settings.create_ui_element('natsu_avatar', (200, 300), 560, input_rect.y + input_rect.height + 10)

            gowther_avatar, gowther_rect = self.settings.create_ui_element('gowther_avatar', (200, 300), 800, input_rect.y + input_rect.height + 10)

            heisuke_avatar, heisuke_rect = self.settings.create_ui_element('heisuke_avatar', (200, 300), 1040, input_rect.y + input_rect.height + 10)

            kansuke_avatar, kansuke_rect = self.settings.create_ui_element('kansuke_avatar', (200, 300), 1280, input_rect.y + input_rect.height + 10)

            ok_button = pygame.image.load('media/UI/ok_button.png')
            ok_button = pygame.transform.scale(ok_button, (200, 75))
            ok_rect = ok_button.get_rect(center=(screen.get_width() / 2, 3 * screen.get_height() / 4))

        except pygame.error as e:
            print(f"Error loading button image: {e}")
            return

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

            for x, y in zip(self.x, self.y):
                screen.blit(pygame.image.load("media/UI/selected.png"), (x, y))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:  # Fin du jeu
                        is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Activate input box if clicked
                    active = input_rect.collidepoint(event.pos)

                self.select_units(event, erza_rect, gray_rect, natsu_rect, gowther_rect, kansuke_rect,
                                 heisuke_rect)

                text, active = self.get_player_name(event, input_rect, text, active)

                new_text = self.submit(event, ok_rect)

                if new_text is not None:
                    if new_text != "end":
                        text = new_text
                    else:
                        is_running = False

            pygame.display.flip()
            clock.tick(60)  # Limit frame rate to 60 FPS


    def display_settings(self):
        pass


# def run(self, clock, screen, map, animation_manager):
#     # Initialisation du gestionnaire de joueur
#
#     handler = PlayerHandler(unit, animation_manager, map)
#     is_running = True
#
#     while is_running:
#         # Calcul du delta time pour synchroniser les mises à jour
#         dt = clock.tick(60) / 1000
#
#         # # Gestion des événements utilisateur
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_END:  # Fin du jeu
#                     is_running = False
#                 handler.key_down_event(event, screen.display, dt)
#
#         # Gestion continue des touches pressées
#         handler.key_pressed_event()
#
#         # Mise à jour des éléments du jeu
#         self.update(unit, map, animation_manager)
#
#         # Dessin et rendu de l'écran
#         self.draw(clock, screen, unit, map, animation_manager)
#
#     pygame.quit()
#     print(map.width, map.height)
#
# def update(self, unit, map, animation_manager):
#     map.group.update()
#     if unit is not None:
#         anim = animation_manager.get_animation(unit.name)
#         if anim.feet.collidelist(map.collisions) > -1:
#             unit.move_back(anim.rect, anim.feet)
#     map.update(animation_manager) # ajouté
#
# def draw(self, clock, screen, unit, map, animation_manager):
#     dt = clock.tick(60) / 1000
#     animation = animation_manager.get_animation(unit.name)
#     effect = animation_manager.get_effect(unit.name)
#
#     # Mise à jour
#     if animation.update(dt, animation_manager.orientation[unit.name]) or (effect and effect.current_effect is not None) :
#         # if effect and effect.current_effect is not None:
#         if effect and not effect.apply_effect(dt, animation_manager.orientation[unit.name]):
#             print("Effect animation completed.")
#             effect.current_effect = None  # Réinitialiser l'effet une fois terminé
#
#     # Rendu (affichage)
#     map.update(animation_manager)
#
#     # Dessiner l'effet
#     if effect and effect.current_effect is not None:
#         # print(f"Drawing effect at index {effect.effect_index}")
#         effect.draw(screen.display)
#
#     # Mettre à jour l'écran
#     pygame.display.flip()
#

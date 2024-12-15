import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame

from src.controller.animation_manager import AnimationManager
from src.controller.menu_handler import MenuHandler
from src.controller.player_handler import PlayerHandler
from src.model.hero_factory import HeroFactory
from src.model.player import Player
from src.settings import SingletonMeta, Settings
from src.view.animation_factory import AnimationFactory
from src.view.map import Map
from src.view.screen import Screen


class Game(metaclass=SingletonMeta):
    def __init__(self):
        """
        Initialise le jeu avec ses composants nécessaires.
        """
        self.is_running = False
        self.players = {}
        self.screen = Screen()
        self.map = Map(self.screen)
        self.clock = pygame.time.Clock()
        self.animation_manager = AnimationManager()
        self.animation_factory = AnimationFactory()
        self.settings = Settings()
        self.current_player_index = 0
        self.current_unit_index = 0
        self.players_list = []
        self.current_player = None
        self.current_unit = None
        self.text_info = None

    def initialize_entities(self, selected_units):
        """
        Crée les entités (joueurs et unités) pour le jeu.
        :param selected_units: Dictionnaire des unités sélectionnées par les joueurs.
        """
        if selected_units:
            for i, (name, unit_names) in enumerate(selected_units.items()):
                player = Player(name)
                for j, unit_name in enumerate(unit_names):
                    unit, sprite_conf = HeroFactory.create_hero(
                        unit_name, self.settings.team_indexes[i][j][0], self.settings.team_indexes[i][j][1], name
                    )
                    if unit:
                        unit.actions = {"move": True, "attack": True, "defend": True}
                        player.units[unit_name] = unit
                        self.animation_manager.add_hero(unit)
                        self.animation_manager.add_animation(
                            unit.name, self.animation_factory.create_animation(unit, sprite_conf)
                        )
                        self.animation_manager.add_effect(
                            unit.name, self.animation_factory.create_effect(sprite_conf)
                        )
                        self.animation_manager.set_orientation(unit.name, "right")
                self.players[name] = player

            self.players_list = list(self.players.keys())
            self.current_player = self.players[self.players_list[self.current_player_index]]
            self.current_unit = list(self.current_player.units.values())[self.current_unit_index]
            self.reset_unit_actions()

    def reset_unit_actions(self):
        """
        Réinitialise les actions de l'unité courante.
        """
        if self.current_unit:
            self.current_unit.actions = {"move": True, "attack": True, "defend": True}
            print(f"Actions réinitialisées pour {self.current_unit.name}.")
            self.text_info = (f"C: '{self.current_unit.competences['attacks'][0]}' \n"
                              f"V: '{self.current_unit.competences['attacks'][1]}' \n")

    def next_unit(self):
        """
        Passe à l'unité suivante qui n'est pas morte.
        Si toutes les unités d'un joueur sont mortes, passe au joueur suivant.
        """
        while True:
            self.current_unit_index += 1
            if self.current_unit_index >= len(self.current_player.units):
                self.current_unit_index = 0
                self.next_player()
                return

            # Obtenir l'unité suivante
            self.current_unit = list(self.current_player.units.values())[self.current_unit_index]

            if self.current_unit.state != 'dead':
                print(f"Passage à l'unité suivante : {self.current_unit.name}.")
                self.reset_unit_actions()
                break






    def next_player(self):
        """
        Passe au joueur suivant. Ignore les joueurs sans unités vivantes.
        """
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players_list)
            self.current_player = self.players[self.players_list[self.current_player_index]]

            # Vérifier si le joueur a encore des unités vivantes
            if any(unit.state != 'dead' for unit in self.current_player.units.values()):
                self.current_unit_index = 0
                self.current_unit = list(self.current_player.units.values())[self.current_unit_index]
                print(f"Passage au joueur suivant : {self.current_player.name}.")
                self.reset_unit_actions()
                break

            # Vérifier si la partie est terminée (tous les joueurs sauf un sont éliminés)
            if self.check_game_over():
                return

    def check_game_over(self):
        """
        Vérifie si la partie est terminée. Si un seul joueur reste, il est déclaré gagnant.
        """
        for player_name, player in self.players.items():
            if all(unit.state == 'dead' for unit in player.units.values()):
                print(f"Le joueur {player_name} a perdu toutes ses unités.")
                self.players_list.remove(player_name)
                if len(self.players_list) == 1:
                    print(f"Le joueur {self.players_list[0]} a gagné la partie!")
                    self.is_running = False
                    rect = pygame.draw.rect(self.screen.display, (0, 0, 0, 128), pygame.Rect(0, 0, self.settings.screen_width, self.settings.screen_height))
                    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 128))
                    self.screen.display.blit(overlay, (rect.x, rect.y))

                    font = pygame.font.Font(f'{Settings().path}media/EagleLake-Regular.ttf', 20)
                    text_surface = font.render(f"Game Over {player_name}!", True, (255, 255, 255))

                    self.screen.display.blit(text_surface, (500, 300))

                    pygame.display.flip()
                    time.sleep(20)
                    return True
        return False

    def check_end_of_turn(self):
        """
        Vérifie si l'unité a terminé son tour.
        """
        if self.current_unit.state == 'dead':
            print(f"{self.current_unit.name} est morte. Son tour est sauté.")
            self.next_unit()
            return

        if not self.current_unit.actions["attack"] and not self.current_unit.actions["defend"]:
            print(f"{self.current_unit.name} a terminé son tour.")
            self.next_unit()

    def update(self):
        """
        Met à jour les animations et l'état du jeu.
        """
        # Mettre à jour toutes les unités (vivantes ou mortes)
        for player in self.players.values():
            for unit in player.units.values():
                # Récupérer l'animation de l'unité
                anim = self.animation_manager.get_animation(unit.name)
                if anim:
                    if anim.feet.collidelist(self.map.collisions) > -1:
                        unit.move_back(anim.rect, anim.feet)
                    if anim.feet.collidelist(self.map.lava_tiles) > -1:
                        if unit.name != 'Natsu':
                            unit.health = 0
                            unit.set_state('dead', None, None)
                    if unit.name != 'Gray' and anim.feet.collidelist(self.map.ice_tiles) > -1:
                        unit.move_back(anim.rect, anim.feet)

                    if unit.state == 'dead':  # Si l'unité est morte
                        anim.state = 'dead'
                        anim.type = 'dead'  # Forcer l'état "dead"
                    anim.update(self.clock.get_time(), self.animation_manager.orientation[unit.name])

                # Gestion des collisions uniquement pour les unités vivantes
                if unit.state != 'dead':
                    if anim.feet.collidelist(self.map.collisions) > -1:
                        unit.move_back(anim.rect, anim.feet)

        # Mettre à jour la carte et les animations globales
        self.map.group.update()
        self.map.update(self.animation_manager, self.current_unit)

    def run(self,avatars, avatar_names, info_box, info_box_0):
        """
        Boucle principale du jeu.
        """
        self.is_running = True

        while self.is_running:
            self.screen.display.fill((0, 0, 0))
            dt = self.clock.tick(60) / 1000

            handler = PlayerHandler(self.current_unit, self.animation_manager, self.map, self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:
                        self.is_running = False
                    handler.key_down_event(event, self.screen.display, dt)

            handler.key_pressed_event()
            self.update()
            avatar_names = list(self.current_player.units.keys())
            # Dessin et rendu de l'écran
            self.draw(avatars, avatar_names, info_box, info_box_0)


    def draw(self, avatar_rects, avatar_names, info_box, info_box_0):
        """
        Dessine les informations de tour et les animations.
        """
        selected_avatar = self.current_unit.name
        animation = self.animation_manager.get_animation(self.current_unit.name)
        effect = self.animation_manager.get_effect(self.current_unit.name)
        # Mettre à jour et dessiner les animations de toutes les unités
        for player in self.players.values():
            for unit in player.units.values():
                animation = self.animation_manager.get_animation(unit.name)
                effect = self.animation_manager.get_effect(unit.name)

                if animation:
                    # Mise à jour de l'animation de l'unité
                    animation.update(self.clock.get_time(), self.animation_manager.orientation[unit.name])
                    #animation.draw(self.screen.display)  # Dessiner l'animation sur l'écran

                if effect and effect.current_effect is not None:
                    # Appliquer les effets liés à l'unité
                    if not effect.apply_effect(self.clock.get_time(), self.animation_manager.orientation[unit.name]):
                        print(f"Effect completed for {unit.name}.")
                        effect.current_effect = None
                    effect.draw(self.screen.display)  # Dessiner les effets sur l'écran

        self.map.update(self.animation_manager, self.current_unit)

        # Dessiner l'effet
        if effect and effect.current_effect is not None:
            # print(f"Drawing effect at index {effect.effect_index}")
            effect.draw(self.screen.display)

        for i, rect in enumerate(avatar_rects):
            self.screen.display.blit(pygame.image.load(f"{Settings().path}media/UI/{avatar_names[i]}_hud.png"), rect)
            if selected_avatar == avatar_names[i]:
                self.current_unit.is_selected = True
                self.screen.display.blit(pygame.image.load(f"{Settings().path}media/UI/selected_hud.png"),
                            avatar_rects[i])  # Highlight selected avatar

        # Draw Info Section
        pygame.draw.rect(self.screen.display, (50, 50, 50), info_box)
        pygame.draw.rect(self.screen.display, (200, 200, 200), info_box, 2)

        pygame.draw.rect(self.screen.display, (50, 50, 50), info_box_0)
        pygame.draw.rect(self.screen.display, (200, 200, 200), info_box_0, 2)  # Border

        # self.draw_walkable_overlay(self.animation_manager.get_animation(self.selected_player.selected_unit.name).get_walkable_tiles(self.selected_player.selected_unit.movement_range))

        # Informations de tour
        turn_info = (
            f"Player: {self.current_player.name} | Unit: {self.current_unit.name} | "
            f"Actions: Move - {self.current_unit.actions['move']}, "
            f"Attack - {self.current_unit.actions['attack']}, Defend - {self.current_unit.actions['defend']}"
        )
        turn_text = pygame.font.Font(f'{Settings().path}media/EagleLake-Regular.ttf', 20).render(turn_info, True, (255, 255, 255))
        self.screen.display.blit(turn_text, (10, 10))

        # turn_text = pygame.font.Font(None, 36).render(self.text_info, True, (255, 255, 255))
        self.draw_multiline_text(info_box, pygame.font.Font(f'{Settings().path}media/EagleLake-Regular.ttf', 20), (255, 255, 255))
        self.draw_multiline_text(info_box_0, pygame.font.Font(f'{Settings().path}media/EagleLake-Regular.ttf', 20), (255, 255, 255), f"{self.current_unit.team} \n {self.current_unit.name} \n {self.current_unit.health}")

        pygame.display.flip()


    def start(self):
        """
        Initialise et démarre le jeu.
        """
        pygame.init()
        icon = pygame.image.load(f"{Settings().path}media/UI/icon.png")
        banner = pygame.image.load(f"{Settings().path}media/UI/banner.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Strategy Game")
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        banner = pygame.transform.scale(banner, screen.get_size())

        SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900  # Fullscreen resolution
        DISPLAY_WIDTH = 1200  # Width for the avatars
        DISPLAY_START_Y = 650  # Starting Y position for avatars
        AVATAR_SIZE = 120  # Size of each avatar
        INFO_BOX_HEIGHT = SCREEN_HEIGHT - (DISPLAY_START_Y + AVATAR_SIZE + 20)  # Remaining space for info
        AVATAR_SPACING = 20
        start_x = (SCREEN_WIDTH - DISPLAY_WIDTH) // 2

        menu_handler = MenuHandler()
        menu_handler.menu(False, banner, self.clock, screen)
        self.initialize_entities(menu_handler.selected_units)

        avatar_names = list(self.current_player.units.keys())

        info_start_y = DISPLAY_START_Y + AVATAR_SIZE + 20
        info_box_0 = pygame.Rect(DISPLAY_WIDTH / 2 + 10, info_start_y - INFO_BOX_HEIGHT - 10, DISPLAY_WIDTH / 2 - 10, INFO_BOX_HEIGHT)
        info_box = pygame.Rect(start_x, info_start_y, DISPLAY_WIDTH, INFO_BOX_HEIGHT)

        avatars = []
        for i in range(3):
            avatar = pygame.Rect(start_x + i * (AVATAR_SIZE + AVATAR_SPACING), DISPLAY_START_Y, AVATAR_SIZE,
                                 AVATAR_SIZE)
            avatars.append(avatar)

        self.run(avatars, avatar_names, info_box, info_box_0)

        # Mise à jour des éléments du jeu
        self.update()

        # Dessin et rendu de l'écran
        self.draw(avatars, avatar_names, info_box, info_box_0)

        pygame.display.flip()
        pygame.quit()


    def draw_multiline_text(self, info_box, font, color, text=None):
        max_lines = 4
        if text is None:
            text = self.text_info

        # Séparer le texte en lignes à l'aide du caractère "\n"
        lines = text.split("\n")
        x, y = info_box.x + 5, info_box.y + 5
        line_spacing = font.get_linesize()  # Espacement entre les lignes

        # Stocker uniquement le texte brut dans 'display'
        display = []
        for line in lines:
            display.append(line)  # Ajouter uniquement la chaîne de texte

            # Si le nombre de lignes dépasse la limite, supprimer la première
            if len(display) > max_lines:
                display.pop(0)

        # Affichage des lignes
        for i in range(len(display)):
            # Créer une surface de texte à partir de la chaîne de texte
            text_surface = font.render(display[i], True, color)
            self.screen.display.blit(text_surface, (x, y))
            y += line_spacing  # Décalage vertical pour la prochaine ligne


# Démarrer le jeu
if __name__ == "__main__":
    game = Game()
    game.start()

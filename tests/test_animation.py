import sys
import os

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
        self.is_running = False
        self.players = {}
        self.screen = Screen()
        self.map = Map(self.screen)
        self.clock = pygame.time.Clock()
        self.animation_manager = AnimationManager()
        self.animation_factory = AnimationFactory()
        self.selected_player = None
        self.settings = Settings()
        self.current_player_index = 0
        self.current_unit_index = 0
        self.players_list = []
        self.current_player = None
        self.current_unit = None

    def initialize_entities(self, selected_units):
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

    def reset_unit_actions(self):
        if self.current_unit:
            self.current_unit.actions = {"move": True, "attack": True, "defend": True}

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
                return  # Sortir de la méthode après changement de joueur

            # Obtenir l'unité suivante
            self.current_unit = list(self.current_player.units.values())[self.current_unit_index]

            # Ignorer les unités mortes
            if self.current_unit.state != 'dead':
                print(f"Passage à l'unité suivante : {self.current_unit.name}.")
                self.reset_unit_actions()
                break  # Unité valide trouvée, sortir de la boucle

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
                break  # Joueur valide trouvé, sortir de la boucle

            # Vérifier si la partie est terminée (tous les joueurs sauf un sont éliminés)
            if self.check_game_over():
                return

    def check_game_over(self):
        for player_name, player in self.players.items():
            if all(unit.state == 'dead' for unit in player.units.values()):
                print(f"Le joueur {player_name} a perdu toutes ses unités.")
                self.players_list.remove(player_name)
                if len(self.players_list) == 1:
                    print(f"Le joueur {self.players_list[0]} a gagné la partie!")
                    self.is_running = False
                    return

    def check_end_of_turn(self):
        if not self.current_unit.actions["attack"] and not self.current_unit.actions["defend"]:
            print(f"{self.current_unit.name} a terminé son tour.")
            self.next_unit()

    def update(self):
        unit = self.current_unit
        self.map.group.update()
        if unit:
            anim = self.animation_manager.get_animation(unit.name)
            if anim and anim.feet.collidelist(self.map.collisions) > -1:
                unit.move_back(anim.rect, anim.feet)
            if unit.name != 'Natsu' and anim.feet.collidelist(self.map.lava_tiles) > -1:
                unit.move_back(anim.rect, anim.feet)
            if unit.name != 'Gray' and anim.feet.collidelist(self.map.ice_tiles) > -1:
                unit.move_back(anim.rect, anim.feet)
        self.map.update(self.animation_manager) # ajouté

    def run(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900  # Fullscreen resolution
        DISPLAY_WIDTH = 1200  # Width for the avatars
        DISPLAY_START_Y = 650  # Starting Y position for avatars
        AVATAR_SIZE = 120  # Size of each avatar
        INFO_BOX_HEIGHT = SCREEN_HEIGHT - (DISPLAY_START_Y + AVATAR_SIZE + 20)  # Remaining space for info
        AVATAR_SPACING = 20
        start_x = (SCREEN_WIDTH - DISPLAY_WIDTH) // 2
        font = pygame.font.Font(None, 36)
        selected_avatars = []

        AVATAR_NAMES = list(self.selected_player.units.keys())
        selected_avatar = None

        info_start_y = DISPLAY_START_Y + AVATAR_SIZE + 20
        info_box = pygame.Rect(start_x, info_start_y, DISPLAY_WIDTH, INFO_BOX_HEIGHT)

        avatars = []
        i = 0
        for i in range(3):
            avatar = pygame.Rect(start_x + i * (AVATAR_SIZE + AVATAR_SPACING), DISPLAY_START_Y, AVATAR_SIZE,
                                 AVATAR_SIZE)
            avatars.append(avatar)

        # Initialisation du gestionnaire de joueur
        handler = PlayerHandler(self.selected_player.selected_unit, self.animation_manager, self.map)
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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(avatars):
                        if (rect not in selected_avatars) and rect.collidepoint(event.pos):
                            selected_avatar = AVATAR_NAMES[i]
                            selected_avatars.append(selected_avatar)

            # Gestion continue des touches pressées
            handler.key_pressed_event()
            self.update()

            # Dessin et rendu de l'écran
            self.draw(avatars, selected_avatar, AVATAR_NAMES, info_box)

        pygame.quit()

    def draw(self, avatar_rects, selected_avatar, avatar_names, info_box):
        animation = self.animation_manager.get_animation(self.current_unit.name)
        effect = self.animation_manager.get_effect(self.current_unit.name)

        if animation and animation.update(self.clock.get_time(), self.animation_manager.orientation[self.current_unit.name]):
            if effect and effect.current_effect is not None:
                if not effect.apply_effect(self.clock.get_time(), self.animation_manager.orientation[self.current_unit.name]):
                    print("Effect animation completed.")
                    effect.current_effect = None

        self.map.update(self.animation_manager)

        # Dessiner l'effet
        if effect and effect.current_effect is not None:
            # print(f"Drawing effect at index {effect.effect_index}")
            effect.draw(self.screen.display)

        for i, rect in enumerate(avatar_rects):
            self.screen.display.blit(pygame.image.load(f"../media/UI/{avatar_names[i]}_hud.png"), rect)
            if selected_avatar == avatar_names[i]:
                self.selected_player.selected_unit = self.selected_player.units[selected_avatar]
                self.selected_player.selected_unit.is_selected = True
                self.screen.display.blit(pygame.image.load(f"../media/UI/selected_hud.png"),
                            avatar_rects[i])  # Highlight selected avatar

        # Draw Info Section
        pygame.draw.rect(self.screen.display, (50, 50, 50), info_box)
        pygame.draw.rect(self.screen.display, (200, 200, 200), info_box, 2)  # Border

        # self.draw_walkable_overlay(self.animation_manager.get_animation(self.selected_player.selected_unit.name).get_walkable_tiles(self.selected_player.selected_unit.movement_range))

        turn_info = (
            f"Player: {self.current_player.name} | Unit: {self.current_unit.name} | "
            f"Actions: Move - {self.current_unit.actions['move']}, "
            f"Attack - {self.current_unit.actions['attack']}, Defend - {self.current_unit.actions['defend']}"
        )
        turn_text = pygame.font.Font(None, 36).render(turn_info, True, (255, 255, 255))
        self.screen.display.blit(turn_text, (10, 10))

        pygame.display.flip()

    def start(self):
        pygame.init()
        icon = pygame.image.load("media/UI/icon.png")
        banner = pygame.image.load("media/UI/banner.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Strategy Game")
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        banner = pygame.transform.scale(banner, screen.get_size())

        menu_handler = MenuHandler()
        menu_handler.menu(False, banner, self.clock, screen)
        self.initialize_entities(menu_handler.selected_units)

        self.run()


        # # Mise à jour des éléments du jeu
        # self.update()
        #
        # # Dessin et rendu de l'écran
        # self.draw(avatar_rects, selected_avatar, avatar_names, info_box)

    def draw_walkable_overlay(self, walkable_tiles):
        for x, y in walkable_tiles:
            tile_x = x * self.settings.tile_width * self.map.zoom_factor
            tile_y = y * self.settings.tile_height * self.map.zoom_factor
            overlay_color = (0, 255, 0, 128)  # Vert semi-transparent
            overlay_surface = pygame.Surface(
                (int(self.settings.tile_width * self.map.zoom_factor), int(self.settings.tile_height * self.map.zoom_factor)), pygame.SRCALPHA
            )
            overlay_surface.fill(overlay_color)
            self.screen.display.blit(overlay_surface, (tile_x, tile_y))

    def overlay_tile(self, x, y, color):
        overlay_surface = pygame.Surface((self.settings.tile_width, self.settings.tile_height), pygame.SRCALPHA)
        overlay_surface.fill(color)

        self.screen.display.blit(overlay_surface, (x * self.settings.tile_width, y * self.settings.tile_height))


if __name__ == "__main__":
    game = Game()
    game.start()

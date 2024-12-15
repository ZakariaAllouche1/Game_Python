import pygame

from src.controller.animation_manager import AnimationManager
# from src.controller.game_handler import AVATAR_NAMES, selected_avatar
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

    def update(self):
        unit = self.selected_player.selected_unit
        self.map.group.update()
        if unit is not None:
            anim = self.animation_manager.get_animation(unit.name)
            if anim.feet.collidelist(self.map.collisions) > -1:
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
            self.screen.display.fill((0, 0, 0))  # Black background

            # Calcul du delta time pour synchroniser les mises à jour
            dt = self.clock.tick(60) / 1000

            # # Gestion des événements utilisateur
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:  # Fin du jeu
                        self.is_running = False
                    handler.key_down_event(event, self.screen.display, dt)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(avatars):
                        if (rect not in selected_avatars) and rect.collidepoint(event.pos):
                            selected_avatar = AVATAR_NAMES[i]
                            selected_avatars.append(selected_avatar)

            # Gestion continue des touches pressées
            handler.key_pressed_event()

            # Mise à jour des éléments du jeu
            self.update()

            # Dessin et rendu de l'écran
            self.draw(avatars, selected_avatar, AVATAR_NAMES, info_box)

        pygame.quit()
        print(self.map.width, self.map.height)

    def draw(self, avatar_rects, selected_avatar, avatar_names, info_box):
        dt = self.clock.tick(60) / 1000
        animation = self.animation_manager.get_animation(self.selected_player.selected_unit.name)
        effect = self.animation_manager.get_effect(self.selected_player.selected_unit.name)

        # Mise à jour
        if animation.update(dt, self.animation_manager.orientation[self.selected_player.selected_unit.name]) or (effect and effect.current_effect is not None) :
            # if effect and effect.current_effect is not None:
            if effect and not effect.apply_effect(dt, self.animation_manager.orientation[self.selected_player.selected_unit.name]):
                print("Effect animation completed.")
                effect.current_effect = None  # Réinitialiser l'effet une fois terminé

        # Rendu (affichage)
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

        pygame.display.flip()

    def initialize_entities(self, selected_units):
        if selected_units is not None:
            i = 0
            for name in selected_units.keys():
                player = Player(name)
                j = 0
                for unit_name in selected_units[name]:
                    unit, sprite_conf = HeroFactory.create_hero(unit_name, self.settings.team_indexes[i][j][0], self.settings.team_indexes[i][j][1], name)
                    if unit is not None:
                        if j == 0:
                            unit.is_selected = True
                        player.units[unit_name] = unit
                        self.animation_manager.add_hero(unit)
                        self.animation_manager.add_animation(unit.name, self.animation_factory.create_animation(unit, sprite_conf))
                        self.animation_manager.add_effect(unit.name, self.animation_factory.create_effect(sprite_conf))
                        self.animation_manager.set_orientation(unit.name, 'right')
                        j += 1
                self.players[name] = player
                i += 1

    def start(self):
        pygame.init()

        # Initialisation
        is_running = True
        pressed = False

        # Configuration
        icon = pygame.image.load('../media/UI/icon.png')
        banner = pygame.image.load('../media/UI/banner.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Strategy Game")
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Résolution explicite pour tester
        banner = pygame.transform.scale(banner, screen.get_size())

        # handler = PlayerHandler(self.selected_player.selected_unit, self.animation_manager, self.map)
        clock = pygame.time.Clock()
        menu_handler = MenuHandler()
        menu_handler.menu(pressed, banner, clock, screen)
        self.initialize_entities(menu_handler.selected_units)
        print(self.players)
        self.selected_player = self.players[list(menu_handler.selected_units.keys())[0]]
        print(self.selected_player)
        self.selected_player.select_unit()
        self.run()
        # for name, unit_dict in self.players.items():
        #     for unit_name, unit in unit_dict.items():
        #         print(name, unit_name, unit)
        pygame.quit()

    # TODO je suis ici
    def handle_turn(self, handler, avatar_rects, selected_avatar, avatar_names, info_box):
        for unit in self.selected_player.units.values():
            has_acted = False
            self.selected_player.selected_unit = unit
            self.selected_player.selected_unit.is_selected = True
            self.update()
            self.draw(avatar_rects, selected_avatar, avatar_names, info_box)

            while not has_acted:
                for event in pygame.event.get():
                    # Calcul du delta time pour synchroniser les mises à jour
                    dt = self.clock.tick(60) / 1000

                    # # Gestion des événements utilisateur
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_END:  # Fin du jeu
                                self.is_running = False
                            elif event.key == pygame.K_KP1:
                                self.selected_player.selected_unit.attack()
                            handler.name = self.selected_player.selected_unit.name
                            handler.key_down_event(event, self.screen.display, dt)

                    # Gestion continue des touches pressées
                    handler.key_pressed_event()

                    # Mise à jour des éléments du jeu
                    self.update()

                    # Dessin et rendu de l'écran
                    self.draw(avatar_rects, selected_avatar, avatar_names, info_box)

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


game = Game()
# print(game.screen.get_size())
game.start()

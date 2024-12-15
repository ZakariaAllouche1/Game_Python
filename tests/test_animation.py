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

    def reset_unit_actions(self):
        """
        Réinitialise les actions de l'unité courante.
        """
        if self.current_unit:
            self.current_unit.actions = {"move": True, "attack": True, "defend": True}
            print(f"Actions réinitialisées pour {self.current_unit.name}.")

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

            # Obtenez l'unité suivante
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

            # Vérifiez si le joueur a encore des unités vivantes
            if any(unit.state != 'dead' for unit in self.current_player.units.values()):
                self.current_unit_index = 0
                self.current_unit = list(self.current_player.units.values())[self.current_unit_index]
                print(f"Passage au joueur suivant : {self.current_player.name}.")
                self.reset_unit_actions()
                break

            # Vérifiez si la partie est terminée
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
        self.map.update(self.animation_manager)
    def run(self):
        """
        Boucle principale du jeu.
        """
        self.is_running = True

        while self.is_running:
            self.screen.display.fill((0, 0, 0))  # Fond noir
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
            self.draw()

        pygame.quit()

    def draw(self):
        """
        Dessine les informations de tour et les animations.
        """
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

        # Mise à jour et affichage de la carte
        self.map.update(self.animation_manager)

        # Informations de tour
        turn_info = (
            f"Player: {self.current_player.name} | Unit: {self.current_unit.name} | "
            f"Actions: Move - {self.current_unit.actions['move']}, "
            f"Attack - {self.current_unit.actions['attack']}, Defend - {self.current_unit.actions['defend']}"
        )
        turn_text = pygame.font.Font(None, 36).render(turn_info, True, (255, 255, 255))
        self.screen.display.blit(turn_text, (10, 10))

        # Rafraîchir l'écran
        pygame.display.flip()


    def start(self):
        """
        Initialise et démarre le jeu.
        """
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


# Démarrer le jeu
if __name__ == "__main__":
    game = Game()
    game.start()

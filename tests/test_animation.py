import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame

from src.controller.animation_manager import AnimationManager
from src.controller.player_handler import PlayerHandler
from src.model.hero_factory import HeroFactory
from src.settings import SingletonMeta
from src.view.animation_factory import AnimationFactory
from src.view.map import Map
from src.view.screen import Screen

class Game(metaclass=SingletonMeta):

    def __init__(self):
        self.is_running = False
        self.players = {'Player 1': [], 'Player 2': []}  # Dictionnaire pour les personnages des joueurs
        self.screen = Screen()
        self.map = Map(self.screen)
        self.map.map_layer.zoom = 2
        self.clock = pygame.time.Clock()
        self.animation_manager = AnimationManager()
        self.animation_factory = AnimationFactory()

        # Créer les personnages pour les joueurs
        self.players['Player 1'].append(HeroFactory.erza(250, 50, 'Player 1 - Erza')[0])  # Personnage 1 du joueur 1
        self.players['Player 1'].append(HeroFactory.gray(250, 150, 'Player 1 - Gray')[0])  # Personnage 2 du joueur 1
        self.players['Player 2'].append(HeroFactory.natsu(700, 300, 'Player 2 - Natsu')[0])  # Personnage 1 du joueur 2
        self.players['Player 2'].append(HeroFactory.kansuke(700, 450, 'Player 2 - Kansuke')[0])  # Personnage 2 du joueur 2

        # Ajouter les personnages à l'animation manager
        for player in self.players['Player 1'] + self.players['Player 2']:
            self.animation_manager.add_hero(player)

        # Ajouter les animations et effets pour chaque personnage
        for player in self.players['Player 1'] + self.players['Player 2']:
            sprite_conf = HeroFactory.sprite_config(player.name)
            self.animation_manager.add_animation(player.name, self.animation_factory.create_animation(player, sprite_conf))
            self.animation_manager.add_effect(player.name, self.animation_factory.create_effect(sprite_conf))

        # Définir l'orientation des personnages
        for player in self.players['Player 1']:
            self.animation_manager.set_orientation(player.name, 'right')
        for player in self.players['Player 2']:
            self.animation_manager.set_orientation(player.name, 'left')

    def update(self):
        # Mise à jour des éléments du jeu (collisions, etc.)
        self.map.group.update()

        # Animation et mouvement des personnages
        for player in self.players['Player 1'] + self.players['Player 2']:
            anim = self.animation_manager.get_animation(player.name)
            if anim.feet.collidelist(self.map.collisions) > -1:
                player.move_back(anim.rect, anim.feet)

        # Mise à jour de la carte
        self.map.update(self.animation_manager)

    def run(self):
        # Initialisation du gestionnaire de joueur
        handler = PlayerHandler(self.players, self.animation_manager, self.map)
        self.is_running = True

        while self.is_running:
            # Calcul du delta time pour synchroniser les mises à jour
            dt = self.clock.tick(60) / 1000

            # Gestion des événements utilisateur
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:  # Fin du jeu
                        self.is_running = False
                    handler.key_down_event(event, self.screen.display, dt)

            # Gestion continue des touches pressées
            handler.key_pressed_event()

            # Mise à jour des éléments du jeu
            self.update()

            # Dessin et rendu de l'écran
            self.draw()

        pygame.quit()
        print(self.map.width, self.map.height)

    def draw(self):
        # Dessin de l'animation
        dt = self.clock.tick(60) / 1000

        # Mise à jour de l'animation et des effets
        for player in self.players['Player 1'] + self.players['Player 2']:
            animation = self.animation_manager.get_animation(player.name)
            effect = self.animation_manager.get_effect(player.name)
            if animation.update(dt, self.animation_manager.orientation[player.name]) or (effect and effect.current_effect is not None):
                if effect and not effect.apply_effect(dt, self.animation_manager.orientation[player.name]):
                    print(f"Effect animation completed for {player.name}.")
                    effect.current_effect = None

        # Rendu (affichage)
        self.map.update(self.animation_manager)

        # Dessiner les effets
        for player in self.players['Player 1'] + self.players['Player 2']:
            effect = self.animation_manager.get_effect(player.name)
            if effect and effect.current_effect is not None:
                effect.draw(self.screen.display)

        # Mettre à jour l'écran
        pygame.display.flip()

game = Game()
print(game.screen.get_size())
game.run()

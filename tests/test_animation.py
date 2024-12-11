import pygame

from src.controller.animation_manager import AnimationManager
from src.controller.player_handler import PlayerHandler
from src.model.unit import Unit
from src.model.attack import Attack
from src.model.defense import Defense
from src.settings import SingletonMeta
from src.view.animation_factory import AnimationFactory
from src.view.map import Map
from src.view.screen import Screen
from src.view.sprites_config import SpriteConfig
import time


class Game(metaclass=SingletonMeta):

    def __init__(self):
        self.player, sprite_conf = self.erza(250, 50, 10, 'player 1')
        self.screen = Screen()
        self.map = Map(self.screen)
        self.map.map_layer.zoom = 2
        self.clock = pygame.time.Clock()
        self.animation_manager = AnimationManager()
        self.animation_factory = AnimationFactory()
        self.animation_manager.add_hero(self.player)
        self.animation_manager.add_animation(self.player.name, self.animation_factory.create_animation(self.player, sprite_conf))
        self.animation_manager.add_effect(self.player.name, self.animation_factory.create_effect(sprite_conf))
        # self.map.group.add(self.player)

    def erza(self, x, y, health, team):
        erza = Unit("Erza", x, y, health, team, 10)
        roue_celeste = Attack("Roue Celeste", 10, (0, 0, 0), 10, (0, 0, 0), None)
        attaque_titania = Attack("Attaque Titania",  10, (0, 0, 0), 10, (0, 0, 0), None)
        erza.add_competence(roue_celeste, "attack")
        erza.add_competence(attaque_titania, "attack")

        armure_protectrice = Defense("Armure protectrice",  10, (0, 0, 0), 10, (0, 0, 0))
        armure_reflechissante = Defense("Armure réfléchissante",  10, (0, 0, 0), 10, (0, 0, 0))
        erza.add_competence(armure_protectrice, "defense")
        erza.add_competence(armure_reflechissante, "defense")

        sprite_conf = SpriteConfig({'idle': [6, 7]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [14, 6, 7]},
                     {'Sword of destiny': [4, 5, 6, 7], 'Titania attack': [8, 9, 10, 11, 22, 14]},
                     {'Fairy aura': [0, 1, 2, 3], 'Diamond shield': [6, 7]},
                     {'Titania attack': (5, 6, True, 190), 'Darkness': (5, 5, True, 190),
                      'Sword of destiny': (5, 2, True, 120)}, {'dead': [15]})
        return erza, sprite_conf

    def update(self):
        self.map.group.update()
        anim = self.animation_manager.get_animation(self.player.name)
        if anim.feet.collidelist(self.map.collisions) > -1:
            self.player.move_back(anim.rect, anim.feet)
        self.map.update(self.animation_manager) # ajouté

    # def run(self):
    #     handler = PlayerHandler(self.player, self.animation_manager)
    #     running = True
    #     while running:
    #         dt = self.clock.tick(60) / 1000
    #
    #         self.player.save_location()
    #         handler.key_pressed_event()
    #         self.update()
    #         # self.map.update(self.animation_manager)
    #
    #         pygame.display.flip()
    #
    #         for event in pygame.event.get():
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_END:
    #                     running = False
    #                 handler.key_down_event(event, self.screen.display, dt)
    #         self.draw()
    #
    #                 # if event.key == pygame.K_a:
    #                 #     self.player.set_state('attacks', (self.player.x + 200, self.player.y))
    #                 #     # type = 'Sword of destiny'
    #                 #     self.player.animation.update(dt, self.player.state, type)
    #                 #     self.player.draw(self.screen.display)
    #                 #     pygame.display.flip()
    #                 #     # anim.attaque_titania('attaque_2', (self.player.x, self.player.y), (self.player.x + 50, self.player.y), self.clock, self.screen.display, self.map, self.player)
    #
    #
    #     pygame.quit()

    def run(self):
        # Initialisation du gestionnaire de joueur
        handler = PlayerHandler(self.player, self.animation_manager)
        running = True

        while running:
            # Calcul du delta time pour synchroniser les mises à jour
            dt = self.clock.tick(60) / 1000

            # # Gestion des événements utilisateur
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:  # Fin du jeu
                        running = False
                    handler.key_down_event(event, self.screen.display, dt)

            # Gestion continue des touches pressées
            handler.key_pressed_event()

            # Mise à jour des éléments du jeu
            self.update()

            # Dessin et rendu de l'écran
            self.draw()

        pygame.quit()

    # TODO pas de runtime error mais logique foirreuse
    # def draw(self):
    #     dt = self.clock.tick(60) / 1000
    #     apply_effect = self.animation_manager.get_animation(self.player.name).update(dt, self.animation_manager.orientation)
    #     effect = self.animation_manager.get_effect(self.player.name)
    #     if apply_effect and effect is not None and effect.current_effect is not None:
    #         running = True
    #         while running:
    #             running = effect.apply_effect(dt, self.animation_manager.orientation)
    #             self.animation_manager.draw(self.screen.display)
    #     self.map.update(self.animation_manager)
    #     apply_effect = self.animation_manager.get_animation(self.player.name).update(dt, self.animation_manager.orientation)
    #     effect = self.animation_manager.get_effect(self.player.name)
    #     if apply_effect and effect is not None and effect.current_effect is not None:
    #         running = True
    #         while running:
    #             running = effect.apply_effect(dt, self.animation_manager.orientation)
    #             effect.draw(self.screen.display)
    #             print(effect.effect_index, effect.effect_frames)
    #
    #     # self.player.draw(self.screen.display)
    #     pygame.display.flip()

    def draw(self):
        dt = self.clock.tick(60) / 1000
        animation = self.animation_manager.get_animation(self.player.name)
        effect = self.animation_manager.get_effect(self.player.name)

        # Mise à jour
        if animation.update(dt, self.animation_manager.orientation) or (effect and effect.current_effect is not None) :
            # if effect and effect.current_effect is not None:
            if effect and not effect.apply_effect(dt, self.animation_manager.orientation):
                print("Effect animation completed.")
                effect.current_effect = None  # Réinitialiser l'effet une fois terminé

        # Rendu (affichage)
        self.map.update(self.animation_manager)

        # Dessiner l'effet
        if effect and effect.current_effect is not None:
            # print(f"Drawing effect at index {effect.effect_index}")
            effect.draw(self.screen.display)

        # Mettre à jour l'écran
        pygame.display.flip()


game = Game()
print(game.screen.get_size())
game.run()

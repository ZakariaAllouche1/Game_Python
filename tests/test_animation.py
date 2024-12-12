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
        self.player_1 = []
        self.player_2 = []
        self.screen = Screen()
        self.map = Map(self.screen)
        self.map.map_layer.zoom = 2
        self.clock = pygame.time.Clock()
        self.animation_manager = AnimationManager()
        self.animation_factory = AnimationFactory()
        self.player, sprite_conf = HeroFactory.erza(250, 50, 'Player 1')
        self.animation_manager.add_hero(self.player)
        self.animation_manager.add_animation(self.player.name, self.animation_factory.create_animation(self.player, sprite_conf))
        self.animation_manager.add_effect(self.player.name, self.animation_factory.create_effect(sprite_conf))
        self.animation_manager.set_orientation(self.player.name, 'right')


    def update(self):
        self.map.group.update()
        anim = self.animation_manager.get_animation(self.player.name)
        if anim.feet.collidelist(self.map.collisions) > -1:
            self.player.move_back(anim.rect, anim.feet)
        self.map.update(self.animation_manager) # ajouté

    def run(self):
        # Initialisation du gestionnaire de joueur
        handler = PlayerHandler(self.player, self.animation_manager, self.map)
        self.is_running = True

        while self.is_running:
            # Calcul du delta time pour synchroniser les mises à jour
            dt = self.clock.tick(60) / 1000

            # # Gestion des événements utilisateur
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:  # Fin du jeu
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
        dt = self.clock.tick(60) / 1000
        animation = self.animation_manager.get_animation(self.player.name)
        effect = self.animation_manager.get_effect(self.player.name)

        # Mise à jour
        if animation.update(dt, self.animation_manager.orientation[self.player.name]) or (effect and effect.current_effect is not None) :
            # if effect and effect.current_effect is not None:
            if effect and not effect.apply_effect(dt, self.animation_manager.orientation[self.player.name]):
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

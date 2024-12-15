import pygame

from src.controller.animation_manager import AnimationManager
from src.model.unit import Unit
from src.view.map import Map


class PlayerHandler:
    def __init__(self, player: Unit, animation_manager: AnimationManager, map: Map, game):
        """
        Gestion des actions des unités d'un joueur.
        :param player: Unité actuelle contrôlée.
        :param animation_manager: Gestionnaire d'animations.
        :param map: Carte actuelle.
        :param game: Référence au jeu principal.
        """
        self.name = player.name
        self.animation_manager = animation_manager
        self.map = map
        self.game = game

    @property
    def player(self):
        """Retourne l'unité actuelle contrôlée."""
        return self.animation_manager.heros[self.name]

    def get_effect(self, type):
        if type in self.animation_manager.effects:
            return self.animation_manager.effects[type]
        return None

    def key_pressed_event(self):
        """
        Gère les événements de déplacement (maintenir les touches).
        """
        if self.game.text_info is None:
            self.game.text_info = ""

        if self.player.state == 'dead':
            # Affiche directement l'animation "dead"
            self.animation_manager.update_animation(self.player, 'dead', 'dead')
            return

        pressed = pygame.key.get_pressed()
        anim = self.animation_manager.get_animation(self.name)
        effect = self.animation_manager.get_effect(self.name)

        if effect is not None and effect.current_effect is None:
            move_distance = self.player.speed

            if pressed[pygame.K_LEFT]:
                self.player.move(-move_distance, 0, anim.rect, anim.feet, self.map)
                self.player.set_state('movement', 'side', None)
                self.animation_manager.update_animation(self.player, 'movement', 'side')
                self.animation_manager.set_orientation(self.name, 'left')

            elif pressed[pygame.K_RIGHT]:
                self.player.move(move_distance, 0, anim.rect, anim.feet, self.map)
                self.player.set_state('movement', 'side', None)
                self.animation_manager.update_animation(self.player, 'movement', 'side')
                self.animation_manager.set_orientation(self.name, 'right')

            elif pressed[pygame.K_UP]:
                self.player.move(0, -move_distance, anim.rect, anim.feet, self.map)
                self.player.set_state('movement', 'up-down', None)
                self.animation_manager.update_animation(self.player, 'movement', 'up-down')

            elif pressed[pygame.K_DOWN]:
                self.player.move(0, move_distance, anim.rect, anim.feet, self.map)
                self.player.set_state('movement', 'up-down', None)
                self.animation_manager.update_animation(self.player, 'movement', 'up-down')

            else:
                # Si aucune touche de direction, revenir à l'état "idle"
                self.player.set_state('idle', 'idle', None)
                self.animation_manager.update_animation(self.player, 'idle', 'idle')

    def find_target(self, attack):
        """
        Trouve une cible valide pour l'unité actuelle en fonction de l'attaque spécifiée.
        :param attack: L'attaque en cours.
        :return: Une unité cible ou None si aucune cible valide n'est trouvée.
        """
        user_position = (self.player.x, self.player.y)

        # Parcourt toutes les unités sur la carte pour trouver une cible valide
        for unit in self.animation_manager.heros.values():
            if unit.team != self.player.team and unit.state != 'dead':
                target_position = (unit.x, unit.y)
                if attack.is_within_range(user_position, target_position):
                    self.game.text_info += f"Target found : {unit.name} at {target_position} position\n"
                    print(f"Cible trouvée : {unit.name} à la position {target_position}")
                    return unit

        print("Aucune cible valide trouvée.")
        return None

    def key_down_event(self, event, screen, dt):
        """
        Gère les événements de défense, d'attaque et la vérification de fin de tour.
        """
        if self.player.state == 'dead':
            self.game.text_info += self.game.current_unit.name + " is dead and can't act!\n"
            print(f"{self.player.name} est mort et ne peut pas agir.")
            self.animation_manager.heros[self.name].set_state('dead', 'dead',
                                                              self.animation_manager.get_effect(
                                                                  self.animation_manager.heros[self.name].name), None)
            self.animation_manager.update_animation(self.player, 'dead', 'dead')
            self.game.check_end_of_turn()
            self.game.check_game_over()
            return

        # Activation de la défense : Toujours afficher l'animation
        if event.key == pygame.K_a or event.key == pygame.K_b and self.player.actions["defend"]:
            if self.player.competences['defenses']:
                if event.key == pygame.K_a :
                    defense = self.player.competences['defenses'][0]
                else:
                    defense = self.player.competences['defenses'][1]
                self.animation_manager.heros[self.name].set_state('defenses', defense.name, self.animation_manager.get_effect(self.animation_manager.heros[self.name].name), None)
                self.game.text_info += f"{self.player.name} activates '{defense.name}' defense\n"
                print(f"{self.player.name} active la défense : {defense.name}")
                damage = 50  # Exemple de dégâts reçus
                reduced_damage = self.player.activate_defense(damage, self.animation_manager)
                print(f"Dégâts après défense : {reduced_damage}")
                self.game.text_info += f"Damage after defense activation {reduced_damage}\n"
                self.animation_manager.update_animation(self.player, 'defenses', defense.name)
                self.player.actions["defend"] = False
                self.game.check_end_of_turn()
                self.game.check_game_over()
            return None

        # Gestion des attaques : Toujours afficher l'animation
        if (event.key == pygame.K_c or event.key == pygame.K_v) and self.player.actions["attack"]:
            attack_index = 0 if event.key == pygame.K_c else 1  # 0 pour C, 1 pour V
            if attack_index < len(self.player.competences['attacks']):
                target_pos = None
                attack = self.player.competences['attacks'][attack_index]
                target = self.find_target(attack)
                if target is not None:
                    target_pos = (target.x, target.y)
                self.animation_manager.heros[self.name].set_state('attacks', attack.name, self.animation_manager.get_effect(self.animation_manager.heros[self.name].name), target_pos)

                if target:
                    self.game.text_info += f"{self.player.name} activates '{attack.name}' attack on {target.name}\n"
                    print(f"{self.player.name} utilise l'attaque : {attack.name} sur {target.name}")
                    self.player.attack(target, attack, self.animation_manager)
                else:
                    self.game.text_info += f"No target found for '{attack.name}' attack\n"
                    print(f"Aucune cible valide trouvée pour l'attaque {attack.name}.")

                # Toujours afficher l'animation d'attaque
                self.animation_manager.update_animation(self.player, 'attacks', attack.name)
                self.player.actions["attack"] = False
                self.game.check_end_of_turn()
                self.game.check_game_over()
            self.game.text_info += (f"A: {self.player.competences['defenses'][0]} \n"
                              f"B: {self.player.competences['defenses'][1]} \n")
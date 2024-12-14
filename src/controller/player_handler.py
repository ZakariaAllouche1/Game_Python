import pygame

from src.controller.animation_manager import AnimationManager
from src.model.unit import Unit
from src.view.map import Map

class PlayerHandler:

    def __init__(self, players, animation_manager: AnimationManager, map: Map):
        self.players = players
        self.animation_manager = animation_manager
        self.map = map
        self.current_turn = 'Player 1'
        self.current_hero_index = 0

    @property
    def current_player(self):
        return self.players[self.current_turn][self.current_hero_index]

    def get_effect(self, type):
        if type in self.animation_manager.effects:
            return self.animation_manager.effects[type]
        return None

    def key_pressed_event(self):
        pressed = pygame.key.get_pressed()
        anim = self.animation_manager.get_animation(self.current_player.name)
        effect = self.animation_manager.get_effect(self.current_player.name)

        if effect is not None and effect.current_effect is None:
            if pressed[pygame.K_LEFT]:
                self.current_player.move(-self.current_player.speed, 0, anim.rect, anim.feet, self.map)
                self.current_player.set_state('movement', 'side', None)
                self.animation_manager.update_animation(self.current_player, 'movement', 'side')
                self.animation_manager.set_orientation(self.current_player.name, 'left')
                return 'side'
            if pressed[pygame.K_RIGHT]:
                self.current_player.move(+self.current_player.speed, 0, anim.rect, anim.feet, self.map)
                self.current_player.set_state('movement', 'side', None)
                self.animation_manager.update_animation(self.current_player, 'movement', 'side')
                self.animation_manager.set_orientation(self.current_player.name, 'right')
                return 'side'
            if pressed[pygame.K_UP]:
                self.current_player.move(0, -self.current_player.speed, anim.rect, anim.feet, self.map)
                self.current_player.set_state('movement', 'up-down', None)
                self.animation_manager.update_animation(self.current_player, 'movement', 'up-down')
                return 'up-down'
            if pressed[pygame.K_DOWN]:
                self.current_player.move(0, +self.current_player.speed, anim.rect, anim.feet, self.map)
                self.current_player.set_state('movement', 'up-down', None)
                self.animation_manager.update_animation(self.current_player, 'movement', 'up-down')
                return 'up-down'
            else:
                if not pressed[pygame.K_a] and not pressed[pygame.K_d]:
                    self.current_player.set_state('idle', 'idle', None)
                    self.animation_manager.update_animation(self.current_player, 'idle', 'idle')
        return 'idle'

    def key_down_event(self, event, screen, dt):
        if self.current_turn == 'Player 1':
            if event.key == pygame.K_r:
                self.perform_attack(self.current_player, 0)
            elif event.key == pygame.K_t:
                self.perform_attack(self.current_player, 1)
        elif self.current_turn == 'Player 2':
            if event.key == pygame.K_r:
                self.perform_attack(self.current_player, 0)
            elif event.key == pygame.K_t:
                self.perform_attack(self.current_player, 1)

    def perform_attack(self, attacker, attack_index):
        target = self.get_opponent_hero(attacker)
        if target:
            attack = attacker.competences['attacks'][attack_index]
            if attack.is_within_range((attacker.x, attacker.y), (target.x, target.y)):
                attack.activate(attacker, target, self.animation_manager.heros.values())
                self.switch_turn()
            else:
                print(f"{target.name} est hors de portée de {attacker.name}.")
        else:
            print(f"Aucune cible valide pour {attacker.name}.")

    def get_opponent_hero(self, attacker):
        opponents = []
        if self.current_turn == 'Player 1':
            opponents = self.players['Player 2']
        else:
            opponents = self.players['Player 1']

        for opponent in opponents:
            attack = attacker.competences['attacks'][0]  # Utiliser la première attaque pour vérifier la portée
            if attack.is_within_range((attacker.x, attacker.y), (opponent.x, opponent.y)):
                return opponent
        return None

    def switch_turn(self):
        if self.current_turn == 'Player 1':
            if self.current_hero_index + 1 < len(self.players['Player 1']):
                self.current_hero_index += 1
            else:
                self.current_turn = 'Player 2'
                self.current_hero_index = 0
        else:
            if self.current_hero_index + 1 < len(self.players['Player 2']):
                self.current_hero_index += 1
            else:
                self.current_turn = 'Player 1'
                self.current_hero_index = 0

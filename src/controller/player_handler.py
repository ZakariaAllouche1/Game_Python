import pygame

from src.controller.animation_manager import AnimationManager
from src.model.unit import Unit


class PlayerHandler:

    def __init__(self, player: Unit, animation_manager: AnimationManager):
        self.name = player.name
        self.animation_manager = animation_manager

    @property
    def player(self):
        return self.animation_manager.heros[self.name]

    def get_effect(self, type):
        if type in self.animation_manager.effects:
            return self.animation_manager.effects[type]
        return None

    def key_pressed_event(self):
        pressed = pygame.key.get_pressed()
        anim = self.animation_manager.get_animation(self.name)
        effect = self.animation_manager.get_effect(self.name)
        print(f"Effect active: {effect.effect_image is not None}")
        if effect is not None and effect.current_effect is None:
            if pressed[pygame.K_LEFT]:
                self.animation_manager.heros[self.name].move(-self.animation_manager.heros[self.name].speed, 0, anim.rect, anim.feet)
                self.animation_manager.heros[self.name].set_state('movement', 'side', None)
                self.animation_manager.update_animation(self.animation_manager.heros[self.name], 'movement', 'side')
                self.animation_manager.orientation = 'left'
                return 'side'
            if pressed[pygame.K_RIGHT]:
                self.animation_manager.heros[self.name].move(+self.animation_manager.heros[self.name].speed, 0, anim.rect, anim.feet)
                self.animation_manager.heros[self.name].set_state('movement', 'side', None)
                self.animation_manager.update_animation(self.animation_manager.heros[self.name], 'movement', 'side')
                self.animation_manager.orientation = 'right'
                return 'side'
            if pressed[pygame.K_UP]:
                self.animation_manager.heros[self.name].move(0, -self.animation_manager.heros[self.name].speed, anim.rect, anim.feet)
                self.animation_manager.heros[self.name].set_state('movement', 'up-down', None)
                self.animation_manager.update_animation(self.animation_manager.heros[self.name], 'movement', 'up-down')
                return 'up-down'
            if pressed[pygame.K_DOWN]:
                self.animation_manager.heros[self.name].move(0, +self.animation_manager.heros[self.name].speed, anim.rect, anim.feet)
                self.animation_manager.heros[self.name].set_state('movement', 'up-down', None)
                self.animation_manager.update_animation(self.animation_manager.heros[self.name], 'movement', 'up-down')
                return 'up-down'
            else:
                if not pressed[pygame.K_a]:
                    self.animation_manager.heros[self.name].set_state('idle', 'idle', None)
                    self.animation_manager.update_animation(self.animation_manager.heros[self.name], 'idle', 'idle')
        return 'idle'

    def key_down_event(self, event, screen, dt):
        if event.key == pygame.K_a:
            if dt is not None:
                type = 'Titania attack'
                print(f"Setting state to 'attacks' with type {type} at position ({self.animation_manager.heros[self.name].x}, {self.animation_manager.heros[self.name].y})")
                self.animation_manager.heros[self.name].set_state('attacks', type, self.animation_manager.get_effect(self.animation_manager.heros[self.name].name), (self.animation_manager.heros[self.name].x + 200, self.animation_manager.heros[self.name].y))
                # print("---------------------------------", self.animation_manager.get_effect(self.animation_manager.heros[self.name].name))
                self.animation_manager.update(self.animation_manager.heros[self.name], 'attacks', type, dt, screen)
                print(f"State after attack: {self.animation_manager.heros[self.name].state}")
                print(f"Effect image: {self.animation_manager.get_effect(self.name).effect_image}")



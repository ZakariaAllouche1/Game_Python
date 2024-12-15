from src.model.unit import Unit
from src.view.animation import Animation
from src.view.effect import Effect
from src.view.sprites_config import SpriteConfig


class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.effects = {}
        self.orientation = {}
        self.sprite_configurations = {}
        self.heros = {}

    def set_orientation(self, name, orientation):
        if not name in self.orientation or self.orientation[name] != orientation:
            if orientation == 'right' or orientation == 'left':
                self.orientation[name] = orientation
            else:
                self.orientation[name] = 'right'
                print('orientation must be "right" or "left"')

    def add_animation(self, name, animation: Animation):
        if name not in self.animations:
            self.animations[name] = animation

    def add_hero(self, hero: Unit):
        if hero.name not in self.heros:
            self.heros[hero.name] = hero

    def add_effect(self, name, effect: Effect):
        if name not in self.effects:
            self.effects[name] = effect

    def add_sprite_conf(self, name, sprite_conf: SpriteConfig):
        if name not in self.sprite_configurations:
            self.sprite_configurations[name] = sprite_conf

    def get_animation(self, name) -> Animation:
        if name in self.animations:
            # print(name, self.animations[name])
            return self.animations[name]

    def get_effect(self, name):
        if name in self.effects:
            return self.effects[name]
        return None

    def draw(self, screen):
        for name, animation in self.animations.items():
            screen.blit(animation.image, (animation.x, animation.y))
        # for name, effect in self.effects.items():
        #     effect.draw(screen)
        #     # print("INDEX ", effect.effect_index)

    def update_animation(self, hero, state, type):
        if hero.name in self.heros:
            self.animations[hero.name].x = hero.x
            self.animations[hero.name].y = hero.y
            self.animations[hero.name].type = type
            self.animations[hero.name].state = state

    # def update(self, hero, state, type, dt, screen):
    #     self.update_animation(hero, state, type)
    #     effect = self.get_effect(hero.name)
    #     apply_effect = self.get_animation(hero.name).update(dt, self.orientation)
    #     if apply_effect and effect is not None and effect.current_effect is not None:
    #         running = True
    #         while running:
    #             running = effect.apply_effect(dt, self.orientation)
    #             print("APPLY EFFECT ", running)
    #             effect.draw(screen)
    #             print(effect.effect_index, effect.effect_frames, self.orientation)

    #def update(self, hero, state, type, dt, screen):
        #self.update_animation(hero, state, type)
        # Supprimer la gestion directe de `apply_effect` ici
        #effect = self.get_effect(hero.name)
        #apply_effect = self.get_animation(hero.name).update(dt, self.orientation[hero.name])
        #if apply_effect and effect is not None and effect.current_effect is not None:
         #   print(f"Effect ready to be applied for hero: {hero.name}")
        #if apply_effect and effect is not None:
        

    def update(self, hero, state, type, dt, screen):
        self.update_animation(hero, state, type)
        effect = self.get_effect(hero.name)

        apply_effect = self.get_animation(hero.name).update(dt, self.orientation[hero.name])
        if apply_effect and effect is not None:
            if effect.current_effect is None:
                effect.start_effect(type)  # Démarrage immédiat de l'effet
            effect.apply_effect(dt, self.orientation[hero.name])
            effect.draw(screen)  # S'assurer que l'effet est dessiné
            print(f"Effet appliqué pour {hero.name}.")


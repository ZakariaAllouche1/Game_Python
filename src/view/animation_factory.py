from src.model.unit import Unit
from src.settings import Settings
from src.view.animation import Animation
from src.view.effect import Effect


class AnimationFactory:
    def __init__(self):
        self.settings = Settings()

    def create_animation(self, hero: Unit, sprite_conf):
        return Animation(hero.name, hero.x, hero.y, self.settings.sprite_width, self.settings.sprite_height, self.settings.animation_speed, sprite_conf)

    def create_effect(self, sprite_conf):
        return Effect(sprite_conf,  self.settings.effect_speed)

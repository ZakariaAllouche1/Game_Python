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
        



    #def update(self, hero, state, type, dt, screen):
     #   self.update_animation(hero, state, type)
      #  effect = self.get_effect(hero.name)

       # apply_effect = self.get_animation(hero.name).update(dt, self.orientation[hero.name])
        #if apply_effect and effect is not None:
         #   if effect.current_effect is None:
          #      effect.start_effect(type)  # Démarrage immédiat de l'effet
           # effect.apply_effect(dt, self.orientation[hero.name])
            #effect.draw(screen)  # S'assurer que l'effet est dessiné
       #     print(f"Effet appliqué pour {hero.name}.")


    def update(self, hero, state, type, dt, screen):
        """
        Met à jour l'animation et l'effet pour un héros donné.
        :param hero: L'unité dont l'animation est mise à jour.
        :param state: L'état actuel du héros (e.g., "dead", "movement").
        :param type: Le type d'action (e.g., "idle", "attack").
        :param dt: Temps écoulé depuis la dernière mise à jour.
        :param screen: Surface d'affichage où dessiner les animations.
        """
        # Mettre à jour l'animation du héros
        self.update_animation(hero, state, type)

        # Récupérer les composants associés au héros
        animation = self.get_animation(hero.name)
        effect = self.get_effect(hero.name)

        if not animation:
            print(f"[DEBUG] Aucun composant d'animation trouvé pour {hero.name}.")
            return

        # Mettre à jour l'animation
        animation_updated = animation.update(dt, self.orientation.get(hero.name, 'right'))

        # Gérer les effets pour les états spécifiques
        if state == 'dead' and effect:
            # Démarrage ou continuation de l'effet "dead"
            if effect.current_effect is None:
                effect.start_effect(type)
            effect.apply_effect(dt, self.orientation.get(hero.name, 'right'))
            effect.draw(screen)
            print(f"[DEBUG] Effet 'dead' appliqué pour {hero.name}.")
            return

        # Pour d'autres états, appliquer les effets si nécessaire
        if animation_updated and effect:
            if effect.current_effect is None:
                effect.start_effect(type)
            effect.apply_effect(dt, self.orientation.get(hero.name, 'right'))
            effect.draw(screen)
            print(f"[DEBUG] Effet '{type}' appliqué pour {hero.name}.")

    
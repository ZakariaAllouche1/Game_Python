from typing import Tuple
from src.model.competence import Competence
from src.model.unit import Unit


class Defense(Competence):
    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int, int]):
        super().__init__(name, power, effect_zone, speed, range)

    def reduce_damage(self, damage, animation_manager, user):
        """
        Réduit les dégâts subis en fonction de la puissance de la défense.
        :param damage: Dégâts initiaux.
        :param animation_manager: Gestionnaire des animations.
        :param user: Unité utilisant la défense.
        :return: Dégâts après réduction.
        """
        reduction = (self.power / 100) * damage
        final_damage = max(0, damage - reduction)

        print(f"[LOG] {user.name} réduit les dégâts de {reduction:.2f} avec {self.name}.")
    
        effect = animation_manager.get_effect(user.name)
        if effect:
            effect.update(user.x, user.y, 'defenses', self.name)
        else:
            print(f"[LOG] Aucune animation trouvée pour {user.name}. Défense : {self.name}")
    
        return final_damage


    def activate(self, user: Unit, animation_manager):
        """
        Active la défense pour protéger l'unité et affiche une animation.
        :param user: Unité utilisant la défense.
        :param animation_manager: Gestionnaire des animations.
        """
        print(f"[LOG] {user.name} active {self.name}. Santé actuelle : {user.health}")
        effect = animation_manager.get_effect(user.name)
        if effect:
            effect.update(user.x, user.y, 'defenses', self.name)
        else:
            print(f"[LOG] Aucune animation trouvée pour {user.name}. Défense : {self.name}")

    def __str__(self):
        return f"Defense -- [Nom: {self.name} | Puissance: {self.power}% | Zone: {self.effect_zone} | Portée: {self.range}]"

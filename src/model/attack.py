from typing import Tuple
from src.model.competence import Competence


class Attack(Competence):
    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int, int], target=None):
        super().__init__(name, power, effect_zone, speed, range)
        self.__target = target

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = target

    def calcul_degat(self, target_position: Tuple[int, int], center_position: Tuple[int, int]) -> int:
        """
        Calcule les dégâts infligés à une cible en fonction de sa distance par rapport au centre de la zone d'effet.
        """
        effect_x = abs(target_position[0] - center_position[0])
        effect_y = abs(target_position[1] - center_position[1])
        if effect_x <= self.effect_zone[0] and effect_y <= self.effect_zone[1]:
            return self.power if effect_x == 0 and effect_y == 0 else int(self.power * 0.4)
        return 0

    def activate(self, user, target, animation_manager):
        """
        Active l'attaque sur une cible principale et applique les dégâts aux unités dans la zone d'effet.
        """
        if self.is_within_range((user.x, user.y), (target.x, target.y)):
            damage = self.calcul_degat((target.x, target.y), (target.x, target.y))
            if damage > 0:
                print(f"[LOG] {user.name} attaque {target.name} infligeant {damage} dégâts.")
                target.health = damage

                #target.health -= damage
                animation_manager.get_effect(target.name).update(target.x, target.y, 'attacks', self.name)

    def __str__(self):
        return f"Attack -- [Nom: {self.name} | Puissance: {self.power} | Zone: {self.effect_zone} | Portée: {self.range}]"

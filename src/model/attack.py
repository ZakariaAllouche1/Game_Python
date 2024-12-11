from typing import Tuple
from src.model.competence import Competence


class Attack(Competence):
    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int, int], target):
        """
        Instanciates an Attack Competence.
        :param name: name of the attack
        :param power: power of the attack
        :param effect_zone: the zone in terms of tiles affected by the attack
        :param speed: speed of the attack
        :param range: the range of possible movement before activating the attack
        :param target: target # TODO Unit or Tile
        """
        super().__init__(name, power, effect_zone, speed, range)
        self.__target = target

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = target

    def calcul_degat(self, defense_target):
        """"calcule les degats """
        degat = max(0, self.power - defense_target)
        return degat

    def activate(self, user, target):
        """active l'attaque"""
        if self.is_within_range((user.x, user.y), (target.x, target.y)):
            raw_damage = self.power
            damage_after_defense = target.activate_defense(raw_damage)
            target.health = damage_after_defense  
            

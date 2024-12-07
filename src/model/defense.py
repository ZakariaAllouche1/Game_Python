from abc import ABC
from typing import Tuple

from Game_Python.src.model.competence import Competence


class Defense(Competence):

    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int, int]):
        """
        Instanciates a Defense Competence.
        :param name: name of the defense mechanism
        :param power: power of the defense mechanism
        :param effect_zone: the zone in terms of tiles protected by the defense mechanism
        :param speed: speed of the defense mechanism
        :param range: the range of possible movement before activating the defense mechanism
        """
        super().__init__(name, power, effect_zone, speed, range)


    def reduce_damage(self, damage):
        """
        Calcule les dégâts après réduction.
        :param damage: Dégâts initiaux.
        :return: Dégâts réduits.
        """
        reduction = (self.power / 100) * damage
        return max(0, damage - reduction)

    def __str__(self):
        return f"Defense -- [Nom: {self.name} | Puissance: {self.power}% | Zone: {self.effect_zone} | Vitesse: {self.speed} | Portée: {self.range}]"

    def activate(self):
        pass
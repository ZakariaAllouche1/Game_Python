from typing import Tuple
from src.model.competence import Competence
from src.model.unit import Unit


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
        Réduit les degats reçus en fonction de la puissance de la défense.
        :param damage: Dégâts initiaux.
        :return: Dégâts réduits.
        """
        reduction = (self.power / 100) * damage
        return max(0, damage - reduction)

    def activate(self, user: Unit):
        """
        Active la compétence de défense pour protéger l'unité.
        :param user: Unité utilisant la défense.
        """
        print(f"{user.name} active {self.name} pour réduire les dégâts subis.")

    def __str__(self):
        return f"Defense -- [Nom: {self.name} | Puissance: {self.power}% | Zone: {self.effect_zone} | Vitesse: {self.speed} | Portée: {self.range}]"

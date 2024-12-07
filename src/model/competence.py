from abc import ABC, abstractmethod
from typing import Tuple


class Competence(ABC):
    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int, int]):
        """
        Classe abstraite pour les compétences.
        :param name: Nom de la compétence.
        :param power: Puissance de base.
        :param effect_zone: Zone affectée par la compétence.
        :param speed: Vitesse d'activation.
        :param range: Portée de la compétence (portée en nombre de cases).
        """
        self.__name = name
        self.__power = power
        self.__effect_zone = effect_zone
        self.__speed = speed
        self.__range = range

    @property
    def name(self):
        return self.__name

    @property
    def power(self):
        return self.__power

    @property
    def effect_zone(self):
        return self.__effect_zone

    @property
    def speed(self):
        return self.__speed

    @property
    def range(self):
        return self.__range

    def is_within_range(self, user_position: Tuple[int, int], target_position: Tuple[int, int]) -> bool:
        """
        Verifie si la cible est a portee de la competence en considerant des portees distinctes pour les axes x et y.
        :param user_position: Position de l'utilisateur (x, y).
        :param target_position: Position de la cible (x, y).
        :return: True si la cible est a portee, False sinon.
        """
        distance_x = abs(target_position[0] - user_position[0])
        distance_y = abs(target_position[1] - user_position[1])
        
        
        return distance_x <= self.range[0] or distance_y <= self.range[1]

    @abstractmethod
    def activate(self, user, target):
        """
        Méthode à implémenter dans les sous-classes.
        Définit comment activer la compétence.
        """
        pass

    def __str__(self):
        return f"Competence -- [Nom: {self.name} | Puissance: {self.power} | Zone: {self.effect_zone} | Vitesse: {self.speed} | Portée: {self.range}]"

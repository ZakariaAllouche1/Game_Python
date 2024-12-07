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
        Vérifie si la cible est à portée de la compétence.
        :param user_position: Position de l'utilisateur (x, y).
        :param target_position: Position de la cible (x, y).
        :return: True si la cible est à portée, False sinon.
        """
        distance = abs(target_position[0] - user_position[0]) + abs(target_position[1] - user_position[1])
        return distance <= self.range[0]  # Utilise la portée maximale définie dans range

    @abstractmethod
    def activate(self, user, target):
        """
        Méthode à implémenter dans les sous-classes.
        Définit comment activer la compétence.
        """
        pass

    def __str__(self):
        return f"Competence -- [Nom: {self.name} | Puissance: {self.power} | Zone: {self.effect_zone} | Vitesse: {self.speed} | Portée: {self.range}]"

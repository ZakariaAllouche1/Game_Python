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
        if power < 0 or any(dim < 0 for dim in effect_zone + range) or speed <= 0:
            raise ValueError("Les valeurs de puissance, de zone d'effet, de portée, et de vitesse doivent être positives.")

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
        Vérifie si la cible est à portée de la compétence en incluant les diagonales.
        :param user_position: Position de l'utilisateur (x, y).
        :param target_position: Position de la cible (x, y).
        :return: True si la cible est à portée, False sinon.
        """
        distance_x = abs(target_position[0] - user_position[0])
        distance_y = abs(target_position[1] - user_position[1])
        diagonal_distance = max(distance_x, distance_y)

        in_range = (
            distance_x <= self.range[0] and
            distance_y <= self.range[1] and
            diagonal_distance <= self.range[2]
        )
        print(f"[LOG] Vérification de portée: X={distance_x}, Y={distance_y}, Diagonale={diagonal_distance}, Résultat={in_range}")
        return in_range

    @abstractmethod
    def activate(self, user, target):
        """
        Méthode abstraite à implémenter dans les sous-classes.
        Définit comment activer la compétence.
        """
        pass

    def __str__(self):
        return f"Competence -- [Nom: {self.name} | Puissance: {self.power} | Zone: {self.effect_zone} | Vitesse: {self.speed} | Portée: {self.range}]"

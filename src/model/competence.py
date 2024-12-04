from abc import ABC, abstractmethod
from typing import Tuple


class Competence(ABC):

    def __init__(self, name: str, power: int=None, effect_zone: Tuple[int, int, int]=(3, 3, 1), speed: int=10, range: Tuple[int, int, int]=(7, 2, 1)):
        """
        Used to instanciate its derived classes as it is an abstract one.
        :param name: name of the attack
        :param power: power of the attack
        :param effect_zone: the zone in terms of tiles affected by the attack
        :param speed: speed of the attack
        :param range: the range of possible movement before activating the attack
        """
        self.__name = name
        self.__power = power
        self.__effect_zone = effect_zone
        self.__speed = speed
        self.__range = range


    # TODO NOTE les caractéristiques des compétences sont fixes durant le jeu, elles ne doivent pas risquer d'être modifiées
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

    def __str__(self):
        return f"Competence -- [Nom: {self.name} | Puissance: {self.power} | Zone: {self.effect_zone} | Vitesse: {self.speed} | Portée: {self.range}]"

    # TODO complete
    @abstractmethod
    def activate(self):
        pass
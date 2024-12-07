from typing import Tuple


from Game_Python.src.model.competence import Competence


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

    # TODO remplacer par une property (degat) pour simplifier l'attaque de l'unité
    def calcul_degat(self, defense_target):
        """"calcule les degats """
        degat= max(0, self.power - defense_target)
        return degat
    
    def __str__(self):
        return f"Attack -- [Nom: {self.name} | Puissance: {self.power} | Zone: {self.effect_zone} | Vitesse: {self.speed} | Portée: {self.range} | Cible: {self.target}]"

    def activate(self):
        # TODO définir comment activer l'attaque, selon si target donne l'unité ennemie ou la case où elle se trouve
        pass

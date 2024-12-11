from typing import Tuple
from competence import Competence

class Attack(Competence):
    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int,int], target=None):
        """
        Initialise une attaque avec des paramètres de puissance, de zone d'effet, de portée, etc.
        :param name: Nom de l'attaque.
        :param power: Puissance de l'attaque.
        :param effect_zone: Zone d'effet de l'attaque (en forme de tuple (x, y)).
        :param speed: Vitesse de l'attaque.
        :param range: Portée de l'attaque (en nombre de cases).
        :param target: La cible de l'attaque (par défaut None, à définir lors de l'activation).
        """
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
        :param target_position: Position de la cible.
        :param center_position: Position du centre de la zone d'effet (la cible principale attaquée).
        :return: Dégâts infligés à la cible.
        """
        effect_x = abs(target_position[0] - center_position[0])
        effect_y = abs(target_position[1] - center_position[1])

        # Vérifie si la cible est dans la zone d'effet
        if effect_x <= self.effect_zone[0] and effect_y <= self.effect_zone[1]:
            if effect_x == 0 and effect_y == 0:
                return self.power  # 100% des dégâts pour le centre
            else:
                return int(self.power * 0.5)  # 50% des dégâts pour les cibles proches
        return 0  # Hors de la zone d'effet, aucun dégât

    def activate(self, user, target, all_units):
        """
        Active l'attaque sur une cible principale et applique les dégâts aux unités dans la zone d'effet.
        :param user: L'unité qui effectue l'attaque.
        :param target: La cible principale de l'attaque.
        :param all_units: Liste de toutes les unités sur le champ de bataille (peut inclure l'attaquant et d'autres cibles).
        """
        if self.is_within_range((user.x, user.y), (target.x, target.y)):
            # La position du centre de la zone devient celle de la cible principale
            center_position = (target.x, target.y)

            for unit in all_units:
                # Ignorer l'attaquant dans la boucle
                if unit == user:
                    continue  # Passe à l'unité suivante sans infliger de dégâts à l'attaquant
                
                unit_position = (unit.x, unit.y)
                damage = self.calcul_degat(unit_position, center_position)
                
                if damage > 0:
                    print(f"{user.name} attaque {unit.name} à ({unit.x}, {unit.y}) et inflige {damage} dégâts.")
                    unit.health -= damage
                else:
                    print(f"{unit.name} à ({unit.x}, {unit.y}) est hors de la zone d'effet.")
        else:
            print(f"{target.name} est hors de portée de {user.name}.")

class Defense:
    def __init__(self, damage_reduction):
        """
        Classe pour représenter une défense.
        :param damage_reduction: Pourcentage de réduction des dégâts (0-100).
        """
        self.damage_reduction = max(0, damage_reduction)

    def reduce_damage(self, damage):
        """
        Calcule les dégâts après réduction.
        :param damage: Dégâts initiaux.
        :return: Dégâts réduits.
        """
        reduction = (self.damage_reduction / 100) * damage
        return max(0, damage - reduction)

    def __str__(self):
        return f"Réduction de dégâts: {self.damage_reduction}%"

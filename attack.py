class Attack:
    def __init__(self, power, speed, range, damage_zone="single"):
        """
        :param power: Puissance de l'attaque.
        :param speed: Vitesse de l'attaque.
        :param range: Portée de l'attaque (en cases).
        :param damage_zone: Zone de dégâts ('single', 'area', 'line').
        """
        self.power = max(0, power)
        self.speed = max(0, speed)
        self.range = max(0, range)
        self.damage_zone = damage_zone  # single, area, or line

    def calcul_degat(self, defense_target):
        """"calcule les degats """
        degat= max(0, self.power - defense_target)
        return degat
    
    def __str__(self):
        return f"Puissance: {self.power}, Vitesse: {self.speed}, Portée: {self.range}, Zone: {self.damage_zone}"


class SingletonMeta(type):
    """Métaclasse pour créer des singletons."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # Crée une instance si elle n'existe pas encore, sinon retourne l'instance existante
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Settings(metaclass=SingletonMeta):
    """Classe Settings utilisant le pattern Singleton."""
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 30
        self.sprite_width = 120
        self.sprite_height = 120
        self.animation_speed = 0.1
        self.effect_speed = 0.01
        self.tile_width = 16
        self.tile_height = 16
        self.nb_tiles_width = 50
        self.nb_tiles_height = 20
        self.tiles = {'movement_range': [],
                      'effect_zone': [],
                      'effect_range': []}

    def update_resolution(self, width, height):
        """Mise à jour de la résolution."""
        self.screen_width = width
        self.screen_height = height

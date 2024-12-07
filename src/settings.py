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
        self.tile_size = 120
        self.nb_tiles = 120

    def update_resolution(self, width, height):
        """Mise à jour de la résolution."""
        self.screen_width = width
        self.screen_height = height

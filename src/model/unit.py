import pygame
from src.model.attack import Attack

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Unit(pygame.sprite.Sprite):
    def __init__(self, name: str, x: int, y: int, health: int, team: str, speed: int):
        """
        Instamciates the Units representing the characters/Heros of the game.
        :param name: the name of the Hero
        :param x: position of the Hero on x-axis
        :param y: position of the Hero on y-axis
        :param health: points of health of the Hero
        :param team: the team of the Hero ['Player 1', 'Player 2']
        :param speed: speed of the Hero
        """
        super().__init__()
        self.__name = name
        self.__x = x
        self.__y = y
        self.__health = float(health)
        self.__team = team
        self.__speed = speed
        self.__movement_range = (0, 0, 0)  # v, h, d
        self.__is_selected = False
        self.__competences = {"attacks": [], "defenses": []}
        self.sprite_sheet = pygame.image.load(f'media/spritesheets/{self.name}.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(self.x + (self.rect.width * 0.7) /4, self.y + (self.rect.height * 0.75), 0.35 * self.rect.width, 0.15 * self.rect.height)
        self.old_position = [self.__x, self.__y].copy()

    @property
    def name(self):
        return self.__name

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        """Maj de pos en x (verification des limites)"""
        if 0 <= value < SCREEN_WIDTH:
            self.__x = value
        else:
            print(f"Position X invalide : {value}")

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        """Maj de position en y (vrification des limites)"""
        if 0 <= value < SCREEN_HEIGHT:
            self.__y = value
        else:
            print(f"Position Y invalide : {value}")
    @property
    def movement_range(self):
        return self.__movement_range
    
    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, damage):
        """Setter pour health - calcul de santé"""
        if damage >= 0:
            old_health = self.__health
            self.__health = max(0, self.__health - damage)
     
    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self, image):
        self.__image = image
    
    @property
    def competences(self):
        return self.__competences

    @property
    def team(self):
        return self.__team
    @property
    def speed(self):
        return self.__speed

    @property
    def is_selected(self):
        return self.__is_selected


    def get_image(self, x, y):
        # TODO automatiser selon les sizes des spritesheets des différents héros : homogéniser
        image = pygame.Surface([120, 120])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 120, 120))
        # return pygame.transform.scale(image, (int(image.get_width() * 0.7), int(image.get_height() * 0.7)))
        return image

    def add_competence(self, competence, type):
        """Ajoute une compétence à l'unité."""
        if type == "attack":
            self.__competences["attacks"].append(competence)
        elif type == "defense":
            self.__competences["defenses"].append(competence)
        else:
            # TODO log
            print("Cannot add this competence, unknown competence type !")

    #def move(self, dx, dy):
        #""" deplacement de l'unite """
        # TODO améliorer les vérifications selon la vraie screen size : codée en dur pour le moment (passer par la classe Settings)
        #if 0 <= self.feet.x + dx and self.feet.x + dx + self.feet.width < 1600 and 0 <= self.feet.y + dy and self.feet.y + dy + self.feet.height < 900:
            #self.__x += dx
            #self.__y += dy
        #self.update()

    def move(self, dx, dy):
        """Déplace l'unité.(pour tester)"""
        new_x = self.__x + dx
        new_y = self.__y + dy
        if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT:
            self.__x = new_x
            self.__y = new_y
            print(f"{self.name} se déplace vers ({self.__x}, {self.__y}).")
        else:
            print(f"Déplacement impossible pour {self.name} ({new_x}, {new_y} hors limite).")

    def attack(self, target, attack):
        """Effectue une attaque."""
        if isinstance(attack, Attack):
            attack.activate(self, target)

    def activate_defense(self, damage: int) -> int:
        """
        Applique les compétences de défense pour réduire les dégâts.
        :param damage: Dégâts initiaux.
        :return: Dégâts après réduction.
        """
        for defense in self.__competences["defenses"]:
            defense.activate(self)
            damage = defense.reduce_damage(damage)  
        return damage

    def update(self):
        self.rect.topleft = (self.x, self.y)
        self.feet.x = self.x + (self.rect.width * 0.7) / 4
        self.feet.y = self.y + (self.rect.height * 0.75)

    def move_back(self):
        self.__x = self.old_position[0]
        self.__y = self.old_position[1]
        self.rect.topleft = (self.x, self.y)
        self.feet.midbottom = self.rect.midbottom
        self.update()

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        screen.blit(self.image, (self.x, self.y))
        # TODO remove après : Que pour le debug des collisions
        # pygame.draw.rect(screen, (0, 255, 0), self.feet, 2)  # Vert

    def save_location(self):
        self.old_position = [self.x, self.y].copy()
import pygame
import random

from Game_Python.src.model.attack import Attack

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
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
        self.__health = health
        self.__team = team
        self.__speed = speed
        self.__movement_range = (0, 0, 0)  # v, h, d
        self.__is_selected = False
        self.__competences = {"attacks": [], "defenses": []}
        self.sprite_sheet = pygame.image.load(f'../media/spritesheets/{self.name}.png')
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

    @property
    def y(self):
        return self.__y

    @property
    def health(self):
        """Getter pour health"""
        return self.__health

    @property
    def team(self):
        return self.__team

    @property
    def speed(self):
        return self.__speed

    @property
    def movement_range(self):
        return self.__movement_range

    @property
    def competences(self):
        return self.__competences

    @property
    def is_selected(self):
        return self.__is_selected

    @property
    def image(self):
        return self.__image

    @x.setter
    def x(self, x):
        # TODO ajouter les vérifications selon la screen size
        self.__x = x

    @y.setter
    def y(self, y):
        # TODO ajouter les vérifications selon la screen size
        self.__y = y

    @image.setter
    def image(self, image):
        self.__image = image

    @health.setter
    def health(self, damage):
        """Setter pour health - calcul de santé"""
        if damage >= 0:
            self.__health = max(0, self.health - damage)

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

    def move(self, dx, dy):
        """ deplacement de l'unite """
        # TODO améliorer les vérifications selon la vraie screen size : codée en dur pour le moment (passer par la classe Settings)
        if 0 <= self.feet.x + dx and self.feet.x + dx + self.feet.width < 1600 and 0 <= self.feet.y + dy and self.feet.y + dy + self.feet.height < 900:
            self.__x += dx
            self.__y += dy
        self.update()

    def attack(self, target, attack):
        """Attaque une unité cible."""
        if isinstance(attack, Attack):
            if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
                target.health -= self.attack.activate()

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
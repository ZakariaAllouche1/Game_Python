import pygame
import random

from attack import Attack

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

class Unit:
    def __init__(self, name: str, x: int, y: int, health: int, team: str, speed: int):
        """
        Instamciates the Units representing the characters/Heros of the game.
        :param name: the name of the Hero
        :param x: position of the Hero on x axis
        :param y: position of the Hero on y axis
        :param health: points of health of the Hero
        :param team: the team of the Hero ['Player 1', 'Player 2']
        :param speed: speed of the Hero
        """
        self.__name = name
        self.__x = x
        self.__y = y
        self.__health = health
        self.__team = team
        self.__speed = speed
        self.__movement_range = (0, 0, 0)  # v, h, d
        self.__is_selected = False
        self.__current_image = None
        self.__competences = {"attacks": [], "defenses": []}


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
    def current_image(self):
        return self.__current_image

    @health.setter
    def health(self, damage):
        """Setter pour health - calcul de santé"""
        self.__health = max(0, self.health - damage)

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
        if 0 <= self.__x + dx < GRID_SIZE and 0 <= self.__y + dy < GRID_SIZE:
            self.__x += dx
            self.__y += dy

    def attack(self, target, attack):
        """Attaque une unité cible."""
        if isinstance(attack, Attack):
            if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
                target.health -= self.attack.activate()

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
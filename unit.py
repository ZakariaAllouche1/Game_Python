import pygame
import random

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
    def __init__(self, name, health, attack, defense, speed,team, x, y):
        """
        Classe de base pour représenter une unité.
        :param name: Nom de l'unité.
        :param health: Points de vie de l'unité.
        :param attack: Statistique d'attaque.
        :param defense: Statistique de défense.
        :param speed: Vitesse de déplacement.
        :param x: Position X de l'unité.
        :param y: Position Y de l'unité.
        """
        self.name = name
        self.health = max(0, health)
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.x = x
        self.y = y
        self.competences = []

    def add_competence(self, competence):
        """Ajoute une compétence à l'unité."""
        self.competences.append(competence)

    def move(self, dx, dy):
        """ deplacement de l'unite """
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
    
    def sante(self, damage):
        """calcul de sante de l'unite"""
        self.health = max(0, self.health - damage)

    def perform_attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


    
from typing import Tuple
import pygame
from pygame import Rect
from src.model.attack import Attack
from src.settings import Settings
from src.view.map import Map


# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE


class Unit(pygame.sprite.Sprite):
    def __init__(self, name: str, x: int, y: int, health: int, team: str, speed: int, range: Tuple[int, int, int] = (2, 3, 1)):
        """
        Instancie une unité représentant un héros du jeu.
        :param name: Nom de l'unité.
        :param x: Position initiale sur l'axe X.
        :param y: Position initiale sur l'axe Y.
        :param health: Points de vie initiaux.
        :param team: Équipe de l'unité.
        :param speed: Vitesse de déplacement.
        :param range: Portée de déplacement (vertical, horizontal, diagonal).
        """
        super().__init__()
        self.__name = name
        self.__x = x
        self.__y = y
        self.__health = float(health)
        self.__team = team
        self.__speed = speed
        self.__movement_range = range  # (vertical, horizontal, diagonal)
        self.__is_selected = False
        self.__competences = {"attacks": [], "defenses": []}
        self.__image = None
        self.state = 'idle'
        self.old_position = [self.__x, self.__y].copy()  # Sauvegarde de la dernière position
        self.actions = {"move": True, "attack": True, "defend": True}  # Actions disponibles dans un tour

    # === PROPRIÉTÉS ===

    @property
    def name(self):
        """Retourne le nom de l'unité."""
        return self.__name

    @property
    def x(self):
        """Retourne la position X de l'unité."""
        return self.__x

    @x.setter
    def x(self, value):
        """Met à jour la position X (vérification des limites)."""
        if 0 <= value < SCREEN_WIDTH:
            self.__x = value
        else:
            print(f"Position X invalide : {value}")

    @property
    def y(self):
        """Retourne la position Y de l'unité."""
        return self.__y

    @y.setter
    def y(self, value):
        """Met à jour la position Y (vérification des limites)."""
        if 0 <= value < SCREEN_HEIGHT:
            self.__y = value
        else:
            print(f"Position Y invalide : {value}")

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, damage):
        """Met à jour les points de vie en réduisant les dégâts."""
        if damage > 0:
            old_health = self.__health
            self.__health = max(0, self.__health - damage)
            print(f"[LOG] {self.name}: Santé mise à jour de {old_health:.2f} à {self.__health:.2f}")
            if self.__health <= 0:
                self.state = 'dead'
                print(f"[LOG] {self.name} est maintenant mort.")
                
    @property
    def team(self):
        """Retourne l'équipe de l'unité."""
        return self.__team

    @property
    def speed(self):
        """Retourne la vitesse de déplacement de l'unité."""
        return self.__speed

    @property
    def movement_range(self):
        """Retourne la portée de mouvement de l'unité."""
        return self.__movement_range

    @property
    def is_selected(self):
        """Retourne si l'unité est sélectionnée."""
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, value):
        """Définit si l'unité est sélectionnée."""
        self.__is_selected = value

    @property
    def competences(self):
        """Retourne les compétences (attaques et défenses) de l'unité."""
        return self.__competences

    @property
    def image(self):
        """Retourne l'image associée à l'unité."""
        return self.__image

    @image.setter
    def image(self, value):
        """Met à jour l'image associée à l'unité."""
        self.__image = value

    # === MÉTHODES ===

    def add_competence(self, competence, type):
        """
        Ajoute une compétence à l'unité.
        :param competence: La compétence à ajouter.
        :param type: Type de compétence (attaque ou défense).
        """
        if type == "attack":
            self.__competences["attacks"].append(competence)
        elif type == "defense":
            self.__competences["defenses"].append(competence)
        else:
            print(f"Type de compétence inconnu : {type}")

    def activate_defense(self, damage: int, animation_manager) -> int:
        if self.state == 'dead':
            print(f"{self.name} est déjà mort et ne peut pas se défendre.")
            return damage
        for defense in self.__competences["defenses"]:
            old_damage = damage
            defense.activate(self, animation_manager)
            damage = defense.reduce_damage(damage, animation_manager, self)
            print(f"[LOG] {self.name}: Dégâts réduits de {old_damage} à {damage} par {defense.name}.")
        return damage


    def attack(self, target, attack, animation_manager):
        """
        Effectue une attaque sur une cible.
        :param target: La cible principale.
        :param attack: Compétence d'attaque à utiliser.
        """
        if self.state == 'dead':
            print(f"{self.name} est mort et ne peut pas attaquer.")
            return
        if target is None:
            print(f"{self.name} n'a pas de cible pour l'attaque.")
            return
        if isinstance(attack, Attack):
            attack.activate(self, target, animation_manager)
        else:
            print(f"Compétence invalide utilisée par {self.name}.")
    def move(self, dx: int, dy: int, rect: Rect, feet: Rect, map_obj: Map):
        """
        Déplace l'unité sur le champ de bataille.
        :param dx: Déplacement sur l'axe X.
        :param dy: Déplacement sur l'axe Y.
        :param rect: Rectangle représentant l'unité.
        :param feet: Rectangle représentant les pieds de l'unité.
        :param map_obj: Carte actuelle.
        """
        if self.state == 'dead':
            print(f"{self.name} est mort et ne peut pas se déplacer.")
            return
        setting = Settings()
        new_x = self.__x + dx
        new_y = self.__y + dy

        # Vérifie les limites de la carte
        if 0 <= new_x + (setting.sprite_width / 2) <= map_obj.width and \
           0 <= new_y + (setting.sprite_height / 2) <= map_obj.height:
            self.save_location()
            self.__x = new_x
            self.__y = new_y
            self.update(rect, feet)
            # print(f"{self.name} se déplace vers ({self.__x}, {self.__y}).")
        else:
            print(f"Déplacement impossible pour {self.name} ({new_x}, {new_y} hors limite).")

    def save_location(self):
        """Sauvegarde la position actuelle de l'unité."""
        self.old_position = [self.__x, self.__y].copy()

    def move_back(self, rect: Rect, feet: Rect):
        """
        Réinitialise la position de l'unité si le déplacement est invalide.
        :param rect: Rectangle représentant l'unité.
        :param feet: Rectangle représentant les pieds de l'unité.
        """
        self.__x = self.old_position[0]
        self.__y = self.old_position[1]
        rect.topleft = (self.__x, self.__y)
        feet.midbottom = rect.midbottom
        self.update(rect, feet)

    def update(self, rect: Rect, feet: Rect):
        """
        Met à jour la position graphique de l'unité.
        :param rect: Rectangle représentant l'unité.
        :param feet: Rectangle représentant les pieds de l'unité.
        """
        rect.topleft = (self.__x, self.__y)
        feet.x = self.__x + (rect.width * 0.7) / 4
        feet.y = self.__y + (rect.height * 0.75)

    def set_state(self, state, action_type, effect, target_pos=None):
        """
        Définit l'état de l'unité pour synchroniser avec l'animation.
        :param state: État de l'unité (idle, attacks, defenses).
        :param action_type: Type d'action (attaque ou défense).
        :param effect: Effet visuel à appliquer.
        :param target_pos: Position cible (optionnel).
        """
        if self.state != 'dead':
            self.state = state
            if (state == 'attacks' or state == 'defenses') and effect is not None:
                effect.update(self.__x, self.__y, state, action_type, target_pos)


    def reset_movement_range(self):
        """Réinitialise la portée de mouvement de l'unité."""
        self.old_position = [self.__x, self.__y].copy()

    def __str__(self):
        return f"Unit -- [Nom: {self.name} | Santé: {self.health} | Position: ({self.__x}, {self.__y}) | Équipe: {self.team}]"

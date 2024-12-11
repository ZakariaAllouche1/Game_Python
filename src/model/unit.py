import pygame
from pygame import Rect

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
        self.state = 'idle'
        # self.animation = Animation(name, x, y, 120, 120, 24, 0.1)
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

    # @property
    # def image(self):
    #     return self.__image

    @x.setter
    def x(self, x):
        # TODO ajouter les vérifications selon la screen size
        self.__x = x

    @y.setter
    def y(self, y):
        # TODO ajouter les vérifications selon la screen size
        self.__y = y

    # @image.setter
    # def image(self, image):
    #     self.__image = image

    @health.setter
    def health(self, damage):
        """Setter pour health - calcul de santé"""
        if damage >= 0:
            self.__health = max(0, self.health - damage)

    # def get_image(self, x, y):
    #     # TODO automatiser selon les sizes des spritesheets des différents héros : homogéniser
    #     image = pygame.Surface([120, 120])
    #     image.blit(self.sprite_sheet, (0, 0), (x, y, 120, 120))
    #     # return pygame.transform.scale(image, (int(image.get_width() * 0.7), int(image.get_height() * 0.7)))
    #     return image

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

    def move(self, dx, dy, rect: Rect, feet: Rect):
        """Déplace l'unité.(pour tester)"""
        new_x = self.__x + dx
        new_y = self.__y + dy
        if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT:
            self.save_location()
            self.__x = new_x
            self.__y = new_y
            # TODO vérifier si c'est bien là
            self.update(rect, feet)
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

    def update(self, rect: Rect, feet: Rect):
        rect.topleft = (self.x, self.y)
        feet.x = self.x + (rect.width * 0.7) / 4
        feet.y = self.y + (rect.height * 0.75)


    def move_back(self, rect: Rect, feet: Rect):
        self.__x = self.old_position[0]
        self.__y = self.old_position[1]
        rect.topleft = (self.x, self.y)
        feet.midbottom = rect.midbottom
        self.update(rect, feet)

    # def draw(self, screen):
    #     """Affiche l'unité sur l'écran."""
    #     screen.blit(self.animation.image, (self.x, self.y))
    #     if self.animation.effect_image is not None:
    #         self.animation.effect.draw(screen)
    #     # TODO remove après : Que pour le debug des collisions
    #     # pygame.draw.rect(screen, (0, 255, 0), self.feet, 2)  # Vert

    def save_location(self):
        self.old_position = [self.x, self.y].copy()

    def set_state(self, state, type, effect, target_pos=None):
        self.state = state
        if (state == 'attacks' or state == 'defenses') and effect is not None :
            effect.update(self.x, self.y, type, target_pos)

            # self.animation.current_effect = self.animation.sprite_conf.effects[type]  # Tuple int, int, boolean, int
            # self.animation.effect_frames = self.animation.extract_frames(self.animation.effects[type], self.animation.current_effect[3], self.animation.current_effect[3], self.animation.current_effect[0], self.animation.current_effect[1])
            # if self.animation.current_effect[2] and target_pos is not None:
            #     # Calcul des positions d'interpolation
            #     self.animation.effect_x = np.linspace(self.x, target_pos[0], len(self.animation.effect_frames))
            #     self.animation.effect_y = np.linspace(self.y, target_pos[1], len(self.animation.effect_frames))
            #     self.animation.frame_index = 0
            #     self.animation.time_since_last_frame = 0
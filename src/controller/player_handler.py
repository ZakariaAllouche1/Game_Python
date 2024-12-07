import pygame

from Game_Python.src.model.unit import Unit


class PlayerHandler:

    def __init__(self, player: Unit):
        self.__player = player

    def key_event(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            self.__player.move(-self.__player.speed, 0)
        elif pressed[pygame.K_RIGHT]:
            self.__player.move(+self.__player.speed, 0)
        elif pressed[pygame.K_UP]:
            self.__player.move(0, -self.__player.speed)
        elif pressed[pygame.K_DOWN]:
            self.__player.move(0, +self.__player.speed)

import pygame


class Screen:
    def __init__(self):
        self.__display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Strategy Game")
        self.__clock = pygame.time.Clock()
        self.__framerate = 60

    def update(self):
        pygame.display.flip()
        pygame.display.update()
        self.__clock.tick(self.__framerate)
        self.__display.fill((0, 0, 0))

    def get_size(self):
        return self.__display.get_size()

    @property
    def display(self):
        return self.__display
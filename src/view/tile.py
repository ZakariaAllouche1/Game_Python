import pygame

from src.settings import Settings


class Tile:
    def __init__(self,x,y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.setting = Settings()

    def draw(self, screen):
        if type in self.setting.tiles:
            pygame.draw.rect(screen,self.setting.tiles[type],(self.x,self.y,self.width,self.height))
        print("Tile ", self.type)


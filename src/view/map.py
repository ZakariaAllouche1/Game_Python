import pygame
import pytmx
import pyscroll

from src.settings import Settings
from src.view.screen import Screen


class Map:
    def __init__(self, screen: Screen, zoom_factor = 2):
        self.__screen = screen
        self.__tmx_data = None
        self.__map_layer = None
        self.__group = None
        self.__zoom_factor = zoom_factor
        self.switch_map('map_1')
        self.__collisions = []
        self.get_collisions()

    @property
    def screen(self):
        return self.__screen

    @property
    def tmx_data(self):
        return self.__tmx_data

    @property
    def map_layer(self):
        return self.__map_layer

    @property
    def group(self):
        return self.__group

    @property
    def zoom_factor(self):
        return self.__zoom_factor

    @property
    def collisions(self):
        return self.__collisions

    @property
    def width(self):
        setting = Settings()
        return setting.tile_width * self.__zoom_factor * setting.nb_tiles_width

    @property
    def height(self):
        setting = Settings()
        return setting.tile_height * self.__zoom_factor * setting.nb_tiles_height

    def switch_map(self, map: str):
        self.__tmx_data = pytmx.load_pygame(f'../media/map/{map}.tmx')
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.__map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.__group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

    def update(self, animation_manager):
        for layer in self.tmx_data.visible_layers:

            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile is not None:
                        zoomed_tile = pygame.transform.scale(tile, (int(self.tmx_data.tilewidth * self.zoom_factor),
                                                                    int(self.tmx_data.tileheight * self.zoom_factor)))

                        zoomed_x = x * self.tmx_data.tilewidth * self.zoom_factor
                        zoomed_y = y * self.tmx_data.tileheight * self.zoom_factor

                        self.screen.display.blit(zoomed_tile, (zoomed_x, zoomed_y))

            if layer.name == "PlayerLayer":
                animation_manager.draw(self.screen.display)

    def get_collisions(self):
        for obj in self.tmx_data.objects:
            if obj.type == 'collision':
                self.collisions.append(pygame.Rect(obj.x * self.zoom_factor, obj.y * self.zoom_factor, obj.width * self.zoom_factor, obj.height * self.zoom_factor))
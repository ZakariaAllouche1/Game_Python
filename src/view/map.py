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
        self.ice_tiles =  []
        self.lava_tiles =  []
        self.get_tiles()

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
        return setting.tile_width * (setting.nb_tiles_width - 1) * self.__zoom_factor

    @property
    def height(self):
        setting = Settings()
        return setting.tile_height * (setting.nb_tiles_height - 1) * self.__zoom_factor

    def switch_map(self, map: str):
        self.__tmx_data = pytmx.load_pygame(f'media/map/{map}.tmx')
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.__map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = self.__zoom_factor
        self.__group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

    def update(self, animation_manager, current_unit):
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
                # if current_unit is not None:
                #     anim = animation_manager.get_animation(current_unit.name)
                #     if anim:
                #         self.draw_walkable_overlay(anim.get_walkable_tiles(current_unit.movement_range))
                animation_manager.draw(self.screen.display)

    def get_collisions(self):
        for obj in self.tmx_data.objects:
            if obj.type == 'collision':
                self.collisions.append(pygame.Rect(obj.x * self.zoom_factor, obj.y * self.zoom_factor, obj.width * self.zoom_factor, obj.height * self.zoom_factor))

    def get_tiles(self):
        for obj in self.tmx_data.objects:
            if obj.type == 'Ice':
                self.ice_tiles.append(pygame.Rect(obj.x * self.zoom_factor, obj.y * self.zoom_factor, obj.width * self.zoom_factor, obj.height * self.zoom_factor))
            elif obj.type == 'Lava':
                self.lava_tiles.append(pygame.Rect(obj.x * self.zoom_factor, obj.y * self.zoom_factor, obj.width * self.zoom_factor, obj.height * self.zoom_factor))

    def draw_walkable_overlay(self, walkable_tiles):
        settings = Settings()
        for x, y in walkable_tiles:
            tile_x = x * settings.tile_width * self.zoom_factor
            tile_y = y * settings.tile_height * self.zoom_factor
            overlay_color = (0, 255, 0, 128)
            overlay_surface = pygame.Surface(
                (int(settings.tile_width * self.zoom_factor), int(settings.tile_height * self.zoom_factor)), pygame.SRCALPHA
            )
            overlay_surface.fill(overlay_color)
            self.screen.display.blit(overlay_surface, (tile_x, tile_y))

    def overlay_tile(self, x, y, color):
        settings = Settings()
        overlay_surface = pygame.Surface((settings.tile_width, settings.tile_height), pygame.SRCALPHA)
        overlay_surface.fill(color)

        self.screen.display.blit(overlay_surface, (x * settings.tile_width, y * settings.tile_height))
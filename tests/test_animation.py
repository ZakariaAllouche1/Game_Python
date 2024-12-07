# import pygame
# import pytmx
#
# from Game_Python.src.view import Map
# from Game_Python.src.view.screen import Screen
#
# # Initialize Pygame
# pygame.init()
#
# # Set up screen
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# clock = pygame.time.Clock()
#
# # Load the TMX map
# tmx_map = pytmx.load_pygame("../media/map/map_2.tmx")
#
# map = Map(Screen())
#
# # Character class to manage animations
# class Character:
#     def __init__(self, x, y, sprite_sheet, frame_width, frame_height, num_frames, animation_speed):
#         self.x = x
#         self.y = y
#         self.sprite_sheet = sprite_sheet
#         self.frame_width = frame_width
#         self.frame_height = frame_height
#         self.num_frames = num_frames
#         self.animation_speed = animation_speed
#         self.frame_index = 0
#         self.time_since_last_frame = 0
#
#         # Extract the frames from the sprite sheet
#         self.frames = [self.sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for
#                        i in range(num_frames)]
#
#     def update(self, dt):
#         self.time_since_last_frame += dt
#         if self.time_since_last_frame >= self.animation_speed:
#             self.time_since_last_frame = 0
#             self.frame_index = (self.frame_index + 1) % self.num_frames
#
#     def draw(self, surface):
#         surface.blit(self.frames[self.frame_index], (self.x, self.y))
#
#     def move(self, dx, dy):
#         self.x += dx
#         self.y += dy
#
#
#
# # Load the sprite sheet
# sprite_sheet = pygame.image.load("../media/spritesheets/Erza.png").convert_alpha()
# character = Character(100, 100, sprite_sheet, 120, 120, 4, 0.1)
#
# # Game loop
# running = True
# while running:
#     dt = clock.tick(60) / 1000  # Time since the last frame (in seconds)
#
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         # Gestion des touches du clavier
#         if event.type == pygame.KEYDOWN:
#
#             # Déplacement (touches fléchées)
#             dx, dy = 0, 0
#             if event.key == pygame.K_LEFT:
#                 dx = -10
#             elif event.key == pygame.K_RIGHT:
#                 dx = 10
#             elif event.key == pygame.K_UP:
#                 dy = -10
#             elif event.key == pygame.K_DOWN:
#                 dy = 10
#
#             # for x in range(0, WIDTH, CELL_SIZE):
#             #     for y in range(0, HEIGHT, CELL_SIZE):
#             #         rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
#             #         pygame.draw.rect(screen, WHITE, rect, 1)
#
#             character.move(dx, dy)
#             character.draw(screen)
#             pygame.display.flip()
#
#     # Update character animation
#     character.update(dt)
#
#     # Draw everything
#     screen.fill((0, 0, 0))  # Fill screen with black before drawing the map
#
#     # Draw the TMX map layers
#     for layer_index, layer in enumerate(map.tmx_data.visible_layers):
#         if isinstance(layer, pytmx.TiledTileLayer):
#             for x, y, tile in layer:
#                 # Get the image for the current tile from the correct layer
#                 tile_image = map.tmx_data.get_tile_image(x, y, layer_index)
#
#                 # If the tile has an image, draw it
#                 if tile_image:
#                     screen.blit(tile_image, (x * map.tmx_data.tilewidth, y * map.tmx_data.tileheight))
#
#     # Draw the character above the map
#     character.draw(screen)
#     pygame.display.flip()
#
# pygame.quit()
import pygame
from pytmx import pytmx

from Game_Python.src.controller.player_handler import PlayerHandler
from Game_Python.src.model.unit import Unit
from Game_Python.src.model.attack import Attack
from Game_Python.src.model.defense import Defense
from Game_Python.src.view.animation_factory import Animation
from Game_Python.src.view.map import Map
from Game_Python.src.view.screen import Screen


class Game:

    def __init__(self):
        self.player = self.Erza(250, 50, 10, 'player 1')
        self.screen = Screen()
        self.map = Map(self.screen)
        self.map.map_layer.zoom = 2
        self.clock = pygame.time.Clock()
        # self.map.group.add(self.player)

    def Erza(self, x, y, health, team):
        erza = Unit("Erza", x, y, health, team, 10)
        roue_celeste = Attack("Roue Celeste", 10, (0, 0, 0), 10, (0, 0, 0), None)
        attaque_titania = Attack("Attaque Titania",  10, (0, 0, 0), 10, (0, 0, 0), None)
        erza.add_competence(roue_celeste, "attack")
        erza.add_competence(attaque_titania, "attack")

        armure_protectrice = Defense("Armure protectrice",  10, (0, 0, 0), 10, (0, 0, 0))
        armure_reflechissante = Defense("Armure réfléchissante",  10, (0, 0, 0), 10, (0, 0, 0))
        erza.add_competence(armure_protectrice, "defense")
        erza.add_competence(armure_reflechissante, "defense")
        return erza

    def update(self):
        self.map.group.update()
        if self.player.feet.collidelist(self.map.collisions) > -1:
            self.player.move_back()

    def run(self):
        handler = PlayerHandler(self.player)
        anim = Animation()
        running = True
        while running:

            self.player.save_location()
            handler.key_event()
            self.update()
            self.map.update(self.player)
            # TODO remove après : Que pour le debug des collisions
            # for rect in self.map.collisions:
            #     pygame.draw.rect(self.map.screen.display, (255, 0, 0), rect, 2)  # Rouge pour les collisions

            # self.player.update()
            # self.player.draw(self.screen.get_display())

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:
                        running = False

                    if event.key == pygame.K_a:
                        anim.attaque_titania((self.player.x, self.player.y), (self.player.x + 50, self.player.y), self.clock, self.screen.display, self.map, self.player)

        pygame.quit()


game = Game()
print(game.screen.get_size())
game.run()

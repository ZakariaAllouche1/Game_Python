import pygame
from pytmx import load_pygame, pytmx

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Overlay sur une carte TMX")

# Couleurs
RED_OVERLAY = (255, 0, 0, 120)  # Rouge semi-transparent

# Chargement de la carte TMX
tmx_data = load_pygame("../media/map/map_1.tmx")  # Remplace par le chemin de ta carte TMX

# Calcul des dimensions des tiles
tile_width = tmx_data.tilewidth
tile_height = tmx_data.tileheight

# Création d'une surface pour l'overlay (semi-transparent)
overlay_surface = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
overlay_surface.fill(RED_OVERLAY)

# Fonction pour dessiner la carte
def draw_map(screen, tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tile_width, y * tile_height))

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacement de l'écran
    screen.fill((0, 0, 0))

    # Dessiner la carte TMX
    draw_map(screen, tmx_data)

    # Exemple : dessiner un overlay sur la tile (3, 2)
    overlay_x, overlay_y = 20, 20  # Coordonnées de la tile
    screen.blit(overlay_surface, (overlay_x * tile_width, overlay_y * tile_height))

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()

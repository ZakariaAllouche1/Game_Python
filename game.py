import pygame
from unit import *


class Game:
    """
    Classe pour représenter le jeu.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player1_units = [Unit(0, 0, 10, 2, 'player1'),
                              Unit(1, 0, 10, 2, 'player1')]

        self.player2_units = [Unit(6, 6, 10, 2, 'player2'),
                              Unit(7, 6, 10, 2, 'player2')]

        self.current_player = 1  # 1 pour Player 1, 2 pour Player 2

    def handle_player_turn(self, player_units):
        """
        Gestion du tour d'un joueur.

        Paramètres
        ----------
        player_units : list[Unit]
            Liste des unités du joueur actuel.
        """
        for selected_unit in player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        if event.key == pygame.K_SPACE:  # Attaque
                            opponent_units = (
                                self.player2_units if self.current_player == 1 else self.player1_units
                            )
                            for opponent in opponent_units:
                                if abs(selected_unit.x - opponent.x) <= 1 and abs(selected_unit.y - opponent.y) <= 1:
                                    selected_unit.attack(opponent)
                                    if opponent.health <= 0:
                                        opponent_units.remove(opponent)

                            has_acted = True
                            selected_unit.is_selected = False

    def flip_display(self):
        """
        Affiche le jeu à l'écran.
        """
        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.player1_units + self.player2_units:
            unit.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()

def main():
    """
    Fonction principale du jeu.
    """
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        if game.current_player == 1:
            game.handle_player_turn(game.player1_units)
            game.current_player = 2
        else:
            game.handle_player_turn(game.player2_units)
            game.current_player = 1


if __name__ == "__main__":
    main()

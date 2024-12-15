import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen and fonts
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Text Example")

font = pygame.font.Font(None, 36)
text = "Hello, welcome to the fantasy world! This text will scroll if it's too long."

# Define the rect where the text will appear
text_rect = pygame.Rect(100, 100, 600, 50)  # x, y, width, height

# Variables for scrolling text
text_surface = font.render(text, True, (255, 255, 255))
text_width = text_surface.get_width()  # Width of the rendered text
scroll_speed = 2  # Pixels per frame

# Initial position of the text
x_pos = text_rect.x
y_pos = text_rect.y

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black background

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # If the text is wider than the rect, start scrolling
    if text_width > text_rect.width:
        x_pos -= scroll_speed  # Move the text to the left

        # If the text has completely moved out of the rect, reset position
        if x_pos + text_width < text_rect.x:
            x_pos = text_rect.x + text_rect.width

    # Blit the text at the new position
    screen.blit(text_surface, (x_pos, y_pos))

    # Draw the bounding rect (for visual reference)
    pygame.draw.rect(screen, (255, 255, 255), text_rect, 2)  # White border

    # Update the screen
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

pygame.quit()
sys.exit()

import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900  # Fullscreen resolution
DISPLAY_WIDTH = 1600  # Width for the avatars
DISPLAY_START_Y = 610  # Starting Y position for avatars
AVATAR_SIZE = 120  # Size of each avatar
INFO_BOX_HEIGHT = SCREEN_HEIGHT - (DISPLAY_START_Y + AVATAR_SIZE + 20)  # Remaining space for info
AVATAR_SPACING = 20
AVATAR_NAMES = ["Hero1", "Hero2", "Hero3", "Hero4"]
AVATAR_STATS = {
    "Hero1": {"Health": 100, "Attack": 20, "Defense": 15, "Attacks": ["Slash", "Punch"], "Defenses": ["Shield"]},
    "Hero2": {"Health": 120, "Attack": 15, "Defense": 20, "Attacks": ["Smash", "Strike"], "Defenses": ["Barrier"]},
    "Hero3": {"Health": 90, "Attack": 25, "Defense": 10, "Attacks": ["Pierce", "Jab"], "Defenses": ["Evasion"]},
    "Hero4": {"Health": 110, "Attack": 18, "Defense": 18, "Attacks": ["Slice", "Kick"], "Defenses": ["Parry"]},
}

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Character Selection")
font = pygame.font.Font(None, 36)

# Load Avatars
avatars = []
for i in range(4):
    avatar = pygame.Surface((AVATAR_SIZE, AVATAR_SIZE))
    avatar.fill((100 + i * 30, 100, 200))  # Placeholder colors for avatars
    avatars.append(avatar)

# Get rects for avatars
avatar_rects = []
start_x = (SCREEN_WIDTH - DISPLAY_WIDTH) // 2
for i in range(4):
    rect = pygame.Rect(start_x + i * (AVATAR_SIZE + AVATAR_SPACING), DISPLAY_START_Y, AVATAR_SIZE, AVATAR_SIZE)
    avatar_rects.append(rect)

# Main Loop
running = True
selected_avatar = None
while running:
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(avatar_rects):
                if rect.collidepoint(event.pos):
                    selected_avatar = AVATAR_NAMES[i]

    # Draw avatars
    for i, rect in enumerate(avatar_rects):
        screen.blit(avatars[i], rect)
        if selected_avatar == AVATAR_NAMES[i]:
            pygame.draw.rect(screen, (255, 255, 0), rect, 4)  # Highlight selected avatar

    # Draw Info Section
    info_start_y = DISPLAY_START_Y + AVATAR_SIZE + 20
    info_box = pygame.Rect(start_x, info_start_y, DISPLAY_WIDTH, INFO_BOX_HEIGHT)
    pygame.draw.rect(screen, (50, 50, 50), info_box)
    pygame.draw.rect(screen, (200, 200, 200), info_box, 2)  # Border

    if selected_avatar:
        stats = AVATAR_STATS[selected_avatar]
        y_offset = info_start_y + 10
        for key, value in stats.items():
            if isinstance(value, list):
                value = ", ".join(value)
            text_surface = font.render(f"{key}: {value}", True, (255, 255, 255))
            screen.blit(text_surface, (start_x + 10, y_offset))
            y_offset += text_surface.get_height() + 5

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

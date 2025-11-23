# config.py
import pygame
import sys

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (243, 156, 18)
VIOLET = (125, 60, 152)

# Pygame initialization
pygame.init()

# Get screen resolution
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_desktop_sizes()[0]

# Font size (adapted to block size)
taille_police = 25
correcteur_police = (WINDOW_WIDTH + WINDOW_HEIGHT) // 2 / 1000

# Create a full-screen window
SCREEN = pygame.display.set_mode(flags=pygame.FULLSCREEN, depth=pygame.SRCALPHA)

# Clock for managing FPS
CLOCK = pygame.time.Clock()
FPS = 120

# Function to quit the game
def quit_game(dummy_arg=None):
    pygame.quit()
    sys.exit()

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

# Create a full-screen window first to get the correct resolution
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SRCALPHA)

# Get screen resolution from the created surface
WINDOW_WIDTH, WINDOW_HEIGHT = SCREEN.get_size()

# Font size (adapted to block size)
taille_police = 25
correcteur_police = (WINDOW_WIDTH + WINDOW_HEIGHT) // 2 / 1000

# Clock for managing FPS
CLOCK = pygame.time.Clock()
FPS = 120

# Function to quit the game
def quit_game(dummy_arg=None):
    pygame.quit()
    sys.exit()

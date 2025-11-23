# config.py
import pygame
import sys

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (243, 156, 18)
VIOLET = (125, 60, 152)

# Initialisation de Pygame
pygame.init()

# Récupération de la résolution de l'écran
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_desktop_sizes()[0]

# Taille de la police (adaptée à la taille des blocs)
taille_police = 25
correcteur_police = (WINDOW_WIDTH + WINDOW_HEIGHT) // 2 / 1000

# Création de la fenêtre en plein écran
SCREEN = pygame.display.set_mode(flags=pygame.FULLSCREEN, depth=pygame.SRCALPHA)

# Horloge pour gérer les FPS
CLOCK = pygame.time.Clock()
FPS = 120

# Fonction pour quitter le jeu
def quit_game(dummy_arg=None):
    pygame.quit()
    sys.exit()

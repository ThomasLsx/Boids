# ui.py
import pygame
from config import BLACK, WHITE, taille_police, correcteur_police, SCREEN

class Text:  # Classe pour afficher du texte à l'écran
    def __init__(self, text, x, y, color=WHITE, taille=int(taille_police*correcteur_police), surface=SCREEN):
        self.x = x  # Coordonnée x du centre du texte
        self.y = y  # Coordonnée y du centre du texte
        self.text = text  # Texte à afficher
        self.color = color  # Couleur du texte
        self.surface = surface  # Surface sur laquelle afficher le texte
        self.font = pygame.font.SysFont(None, int(taille*correcteur_police))  # Police du texte

    def Draw(self, surface=None):  # surface argument for flexibility
        if surface is None:
            surface = self.surface # Use default surface if none provided

        text_obj = self.font.render(self.text, True, self.color)  # Rend le texte en tant qu'image
        text_rect = text_obj.get_rect(center=(self.x, self.y))  # Crée un rectangle centré sur les coordonnées x et y
        surface.blit(text_obj, text_rect)  # Dessine le texte sur la surface
        return text_rect  # Retourne le rectangle du texte


class Button:
    def __init__(self, text, color=WHITE, text_color=BLACK, padding=10, margin=5, font_size=None, surface=SCREEN):
        self.text = text  # Texte du bouton
        self.color = color  # Couleur du bouton
        self.padding = padding  # Padding autour du texte
        self.margin = margin  # Marge autour du bouton
        self.font_size = font_size if font_size else taille_police # Utilise la taille de police globale si non spécifiée

        self.font = pygame.font.SysFont(None, int(self.font_size * correcteur_police))
        self.text_surface = self.font.render(self.text, True, text_color)
        text_width, text_height = self.text_surface.get_size()
        self.rect = pygame.Rect(0, 0, text_width + 2 * self.padding, text_height + 2 * self.padding)


    def draw(self, surface=SCREEN, x=0, y=0):
        self.rect.topleft = (x, y)  # Définit la position avant de dessiner
        pygame.draw.rect(surface, self.color, self.rect)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def handle_event(self, event, pos_override=None): # Ajout de l'argument pos_override
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pos_override if pos_override else event.pos # Utilise la position surchargée si fournie
            if self.rect.collidepoint(pos):
                return True
        return False


class SliderButton:
    def __init__(self, x, y, width, height, min_val, max_val, current_val, text_color=BLACK, color=WHITE, text="", font_size=taille_police, surface=SCREEN):
        self.x = x  # Coordonnée x du slider
        self.y = y  # Coordonnée y du slider
        self.width = width  # Largeur du slider
        self.height = height  # Hauteur du slider
        self.min_val = min_val  # Valeur minimale du slider
        self.max_val = max_val  # Valeur maximale du slider
        self.current_val = current_val  # Valeur actuelle du slider
        self.color = color  # Couleur du slider
        self.text = text  # Texte du slider
        self.font_size = font_size  # Taille de la police
        self.surface = surface  # Surface sur laquelle dessiner le slider

        self.dragging = False  # Indicateur de glissement
        self.font = pygame.font.SysFont(None, int(self.font_size * correcteur_police))
        self.text_surface = self.font.render(self.text, True, text_color)

        self.slider_rect = pygame.Rect(self.x, self.y + self.height, self.width, 10)  # Hauteur plus petite pour le slider
        self.cursor_radius = 10  # Rayon du curseur
        self.cursor_x = self.x + int((self.current_val - self.min_val) / (self.max_val - self.min_val) * self.width)

    

    def draw(self, bar_color = WHITE, cursor_color = BLACK):
        # Dessine la barre du slider
        pygame.draw.rect(self.surface, bar_color, self.slider_rect)

        # Dessine le curseur
        pygame.draw.circle(self.surface, cursor_color, (self.cursor_x, self.slider_rect.centery), self.cursor_radius)

        # Dessine le texte (si présent)
        if self.text:
            text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height//4 ))
            self.surface.blit(self.text_surface, text_rect)
        
        # Dessine les valeurs
        Text(f"{round(self.current_val)} %", self.x - 50, self.slider_rect[1], cursor_color, 20).Draw()


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.cursor_x = max(self.x, min(event.pos[0], self.x + self.width))
                self.current_val = self.min_val + (self.cursor_x - self.x) / self.width * (self.max_val - self.min_val)

    def get_value(self):
        return self.current_val

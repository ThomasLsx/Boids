# ui.py
import pygame
from config import BLACK, WHITE, taille_police, correcteur_police, SCREEN

class Text:
    """Class to display text on the screen."""
    def __init__(self, text: str, x: int, y: int, color: tuple = WHITE, taille: int = int(taille_police * correcteur_police), surface: pygame.Surface = SCREEN):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.surface = surface
        self.font = pygame.font.SysFont(None, int(taille * correcteur_police))

    def draw(self, surface: pygame.Surface = None) -> pygame.Rect:
        """Draws the text and returns its collision rectangle."""
        if surface is None:
            surface = self.surface

        text_obj = self.font.render(self.text, True, self.color)
        text_rect = text_obj.get_rect(center=(self.x, self.y))
        surface.blit(text_obj, text_rect)
        return text_rect


class Button:
    def __init__(self, text: str, color: tuple = WHITE, text_color: tuple = BLACK, padding: int = 10, margin: int = 5, font_size: int = None, surface: pygame.Surface = SCREEN):
        self.text = text
        self.color = color
        self.padding = padding
        self.margin = margin
        self.font_size = font_size if font_size else taille_police

        self.font = pygame.font.SysFont(None, int(self.font_size * correcteur_police))
        self.text_surface = self.font.render(self.text, True, text_color)
        text_width, text_height = self.text_surface.get_size()
        self.rect = pygame.Rect(0, 0, text_width + 2 * self.padding, text_height + 2 * self.padding)

    def draw(self, surface: pygame.Surface = SCREEN, x: int = 0, y: int = 0):
        self.rect.topleft = (x, y)
        pygame.draw.rect(surface, self.color, self.rect)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event, pos_override: tuple = None) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pos_override if pos_override else event.pos
            if self.rect.collidepoint(pos):
                return True
        return False


class SliderButton:
    def __init__(self, x: int, y: int, width: int, height: int, min_val: float, max_val: float, current_val: float, text_color: tuple = BLACK, color: tuple = WHITE, text: str = "", font_size: int = taille_police, surface: pygame.Surface = SCREEN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = current_val
        self.color = color
        self.text = text
        self.font_size = font_size
        self.surface = surface

        self.dragging = False
        self.font = pygame.font.SysFont(None, int(self.font_size * correcteur_police))
        self.text_surface = self.font.render(self.text, True, text_color)

        self.slider_rect = pygame.Rect(self.x, self.y + self.height, self.width, 10)
        self.cursor_radius = 10
        self.cursor_x = self.x + int((self.current_val - self.min_val) / (self.max_val - self.min_val) * self.width)

    def draw(self, bar_color: tuple = WHITE, cursor_color: tuple = BLACK):
        # Draw the slider bar
        pygame.draw.rect(self.surface, bar_color, self.slider_rect)

        # Draw the cursor
        pygame.draw.circle(self.surface, cursor_color, (self.cursor_x, self.slider_rect.centery), self.cursor_radius)

        # Draw the text (if present)
        if self.text:
            text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 4))
            self.surface.blit(self.text_surface, text_rect)
        
        # Draw the values
        Text(f"{round(self.current_val)} %", self.x - 50, self.slider_rect[1], cursor_color, 20).draw()

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
                return True # Indicate handled

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.cursor_x = max(self.x, min(event.pos[0], self.x + self.width))
                self.current_val = self.min_val + (self.cursor_x - self.x) / self.width * (self.max_val - self.min_val)
                return True
        return False

    def get_value(self) -> float:
        return self.current_val

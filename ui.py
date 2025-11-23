# ui.py
import pygame
from config import BLACK, WHITE, taille_police, correcteur_police, SCREEN

class Text:  # Class to display text on the screen
    def __init__(self, text, x, y, color=WHITE, taille=int(taille_police*correcteur_police), surface=SCREEN):
        self.x = x  # x-coordinate of the center of the text
        self.y = y  # y-coordinate of the center of the text
        self.text = text  # Text to display
        self.color = color  # Color of the text
        self.surface = surface  # Surface on which to display the text
        self.font = pygame.font.SysFont(None, int(taille*correcteur_police))  # Font of the text

    def Draw(self, surface=None):  # surface argument for flexibility
        if surface is None:
            surface = self.surface # Use default surface if none provided

        text_obj = self.font.render(self.text, True, self.color)  # Render the text as an image
        text_rect = text_obj.get_rect(center=(self.x, self.y))  # Create a rectangle centered on the x and y coordinates
        surface.blit(text_obj, text_rect)  # Draw the text on the surface
        return text_rect  # Return the rectangle of the text


class Button:
    def __init__(self, text, color=WHITE, text_color=BLACK, padding=10, margin=5, font_size=None, surface=SCREEN):
        self.text = text  # Text of the button
        self.color = color  # Color of the button
        self.padding = padding  # Padding around the text
        self.margin = margin  # Margin around the button
        self.font_size = font_size if font_size else taille_police # Use the global font size if not specified

        self.font = pygame.font.SysFont(None, int(self.font_size * correcteur_police))
        self.text_surface = self.font.render(self.text, True, text_color)
        text_width, text_height = self.text_surface.get_size()
        self.rect = pygame.Rect(0, 0, text_width + 2 * self.padding, text_height + 2 * self.padding)


    def draw(self, surface=SCREEN, x=0, y=0):
        self.rect.topleft = (x, y)  # Set the position before drawing
        pygame.draw.rect(surface, self.color, self.rect)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def handle_event(self, event, pos_override=None): # Added pos_override argument
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pos_override if pos_override else event.pos # Use the overridden position if provided
            if self.rect.collidepoint(pos):
                return True
        return False


class SliderButton:
    def __init__(self, x, y, width, height, min_val, max_val, current_val, text_color=BLACK, color=WHITE, text="", font_size=taille_police, surface=SCREEN):
        self.x = x  # x-coordinate of the slider
        self.y = y  # y-coordinate of the slider
        self.width = width  # Width of the slider
        self.height = height  # Height of the slider
        self.min_val = min_val  # Minimum value of the slider
        self.max_val = max_val  # Maximum value of the slider
        self.current_val = current_val  # Current value of the slider
        self.color = color  # Color of the slider
        self.text = text  # Text of the slider
        self.font_size = font_size  # Font size
        self.surface = surface  # Surface on which to draw the slider

        self.dragging = False  # Dragging indicator
        self.font = pygame.font.SysFont(None, int(self.font_size * correcteur_police))
        self.text_surface = self.font.render(self.text, True, text_color)

        self.slider_rect = pygame.Rect(self.x, self.y + self.height, self.width, 10)  # Smaller height for the slider
        self.cursor_radius = 10  # Radius of the cursor
        self.cursor_x = self.x + int((self.current_val - self.min_val) / (self.max_val - self.min_val) * self.width)

    

    def draw(self, bar_color = WHITE, cursor_color = BLACK):
        # Draw the slider bar
        pygame.draw.rect(self.surface, bar_color, self.slider_rect)

        # Draw the cursor
        pygame.draw.circle(self.surface, cursor_color, (self.cursor_x, self.slider_rect.centery), self.cursor_radius)

        # Draw the text (if present)
        if self.text:
            text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height//4 ))
            self.surface.blit(self.text_surface, text_rect)
        
        # Draw the values
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

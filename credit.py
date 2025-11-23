# credit.py
import pygame
from ui import Text
from config import quit_game, SCREEN, WINDOW_HEIGHT, WINDOW_WIDTH, WHITE, GREEN, CLOCK, correcteur_police

class Credits:
    def __init__(self):
        # Credits text
        self.credits_text = [
            "Boids Project",
            "",
            "Developed by:",
            "BARTCZAK Antoine",
            "BRIAUT Lilian",
            "LESIEUX Thomas",
            
            "",
            "Polytech Dijon",
            "Year 2024-2025",
        ]
        self.font_size = 30  # Font size

    def run(self, return_to_menu):
        while True:
            # Black background
            SCREEN.fill((0, 0, 0))

            # Calculate the total height of the text block
            total_text_height = len(self.credits_text) * self.font_size * correcteur_police
            # Calculate the starting y-coordinate to center the text block
            start_y = (WINDOW_HEIGHT - total_text_height) // 2

            # Display each line of text
            for i, line in enumerate(self.credits_text):
                Text(line, WINDOW_WIDTH // 2, start_y + i * self.font_size * correcteur_police, WHITE, self.font_size).draw()

            # Return button
            return_button = Text(
                "Back", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100, GREEN, 50
            ).draw()

            # Update the display
            pygame.display.update()

            # Event handling
            for event in pygame.event.get():
                # Close the window
                if event.type == pygame.QUIT:
                    quit_game()
                # Mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click on the return button
                    if return_button.collidepoint(event.pos):
                        return_to_menu()
                # Key press
                if event.type == pygame.KEYDOWN:
                    # Escape key
                    if event.key == pygame.K_ESCAPE:
                        return_to_menu()
                    # Enter key
                    if event.key == pygame.K_RETURN:
                        return_to_menu()

            # Limit the frame rate
            CLOCK.tick(30)

# Import necessary modules
import pygame
import simulation
from ui import Text
from credit import Credits
from config import quit_game, SCREEN, CLOCK, FPS, WINDOW_HEIGHT, WINDOW_WIDTH, WHITE, GREEN

# Main menu function
def menu():
    credits_use = Credits()  # Instance of the Credits class
    
    # Menu options: displayed text and associated action
    options = [
        ("Simulation", simulation.run),  # Option to launch the simulation
        ("Credits", credits_use.run),  # Option to display credits
        ("Quit", quit_game),  # Option to quit the game
    ]
    selected = 0  # Index of the selected option

    while True:
        SCREEN.fill((0, 0, 0))  # Clear the screen

        # Draw menu options
        option_rects = []  # List to store collision rectangles of the options
        for i, (text, action) in enumerate(options):  # Iterate over the options
            # Create a Text object for each option and draw it
            option_text = Text(
                text,  # Text of the option
                WINDOW_WIDTH // 2,  # Centered x position
                (i + 1) * WINDOW_HEIGHT // (len(options) + 1),  # Dynamic y position based on the number of options
                GREEN if selected == i else WHITE,  # Green if selected, otherwise white
                50,  # Font size
            ).draw()  # Draw the text and return its collision rectangle
            option_rects.append(option_text)  # Add the rectangle to the list

        pygame.display.update()  # Update the display

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Window closed
                quit_game()

            if event.type == pygame.KEYDOWN:  # Key press
                if event.key == pygame.K_ESCAPE:  # Escape key
                    quit_game()
                if event.key == pygame.K_DOWN:  # Down arrow
                    selected = (selected + 1) % len(options)  # Select the next option
                elif event.key == pygame.K_UP:  # Up arrow
                    selected = (selected - 1) % len(options)  # Select the previous option
                elif event.key == pygame.K_RETURN:  # Enter key
                    options[selected][1](None if selected == 2 else menu)  # Execute the action associated with the selected option

            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click
                for i, option_rect in enumerate(option_rects):  # Iterate over the collision rectangles
                    if option_rect.collidepoint(event.pos):  # Check if the click is on an option
                        options[i][1](None if options[i][1] == quit_game else menu)  # Execute the action, pass menu to simulation.run if necessary
                        break  # Exit the loop after a click

        CLOCK.tick(FPS)  # Limit the refresh rate

# Main function of the program
def main():
    menu()  # Launch the menu

# Entry point of the program
if __name__ == "__main__":
    main()  # Execute the main function if the script is executed directly

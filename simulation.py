# simulation.py
import pygame
import numpy as np
from math import pi, atan2, degrees
from flock import Flock
from ui import Button, Text, SliderButton
from config import SCREEN, CLOCK, FPS, WINDOW_HEIGHT, WINDOW_WIDTH, BLACK, ORANGE, WHITE, BLUE, RED, GREEN, quit_game

# Boids initialization
nbBoids = 100

# Button creation
button_labels = ["Back", "Reset", "Add", "Remove", "Pause", "Zones"] # Removed Grid
buttons = []
x_offset = 20
y_offset_top = 20
y_offset_bottom = WINDOW_HEIGHT - 55
margin = 5

for label in button_labels:
    button = Button(label)
    buttons.append(button)

# Slider creation
slider_labels = ["Cohesion", "Alignment", "Separation", "Max Speed"]
sliders = []
slider_x = WINDOW_WIDTH - 235
slider_y_start = 20
slider_spacing = 50

for i, label in enumerate(slider_labels):
    max_val = (100 if i < 2 else 200)
    current_val = (max_val if i < 2 else max_val / 2)
    slider = SliderButton(
        x=slider_x,
        y=slider_y_start + i * 1.5 * slider_spacing,
        width=200,
        height=35,
        min_val=0,
        max_val=max_val,
        current_val=current_val,
        color=WHITE,
        text=label,
        text_color=ORANGE
    )
    sliders.append(slider)

def run(return_to_menu):
    global flock

    running = True
    zone_on = False

    # Flock initialization
    flock = Flock(nbBoids)
    
    while True:
        SCREEN.fill(BLACK)

        if running:
            # Get slider values
            cohesion_val = sliders[0].get_value() * 2 
            alignment_val = sliders[1].get_value() * 2
            separation_val = sliders[2].get_value() * 0.5 
            max_speed_val = sliders[3].get_value() * 0.05 

            # Update flock
            flock.update(cohesion_val, alignment_val, separation_val, max_speed_val)
            flock.draw(SCREEN)

            if zone_on:
                buttons[5] = Button("Zones", text_color=GREEN)
                if flock.num_boids > 0:
                    # Visualize for the first boid
                    pos = flock.positions[0]
                    vel = flock.velocities[0]
                    
                    # Calculate angle
                    angle = atan2(vel[1], vel[0])
                    start_angle = angle - np.radians(flock.vision_angle / 2)
                    end_angle = angle + np.radians(flock.vision_angle / 2)
                    
                    # Pygame arc takes rectangle, start_angle, stop_angle
                    # Angles are in radians, 0 is right, clockwise? No, standard trig usually but pygame is weird.
                    # Pygame arc angles are in radians, 0 is right, counter-clockwise.
                    # But we need to convert to degrees for logic if needed, or just use radians.
                    # Wait, original code used degrees conversion: (start_angle + direction_angle) * pi / 180
                    # Let's stick to radians since numpy uses radians.
                    # Note: Pygame coordinate system y is down.
                    
                    # Draw Separation
                    if separation_val > 1:
                        rect = pygame.Rect(pos[0] - separation_val, pos[1] - separation_val, separation_val * 2, separation_val * 2)
                        pygame.draw.arc(SCREEN, BLUE, rect, -end_angle, -start_angle, 2)
                        
                    # Draw Alignment
                    if alignment_val > 1:
                        rect = pygame.Rect(pos[0] - alignment_val, pos[1] - alignment_val, alignment_val * 2, alignment_val * 2)
                        pygame.draw.arc(SCREEN, RED, rect, -end_angle, -start_angle, 2)
                        # Draw velocity vector
                        end_pos = pos + vel * 20 # Scale for visibility
                        pygame.draw.line(SCREEN, ORANGE, pos, end_pos, 2)

                    # Draw Cohesion
                    if cohesion_val > 1:
                        rect = pygame.Rect(pos[0] - cohesion_val, pos[1] - cohesion_val, cohesion_val * 2, cohesion_val * 2)
                        pygame.draw.arc(SCREEN, GREEN, rect, -end_angle, -start_angle, 2)
                        
                        # Draw center of mass
                        cohe_center = flock.cohesion_centers[0]
                        pygame.draw.line(SCREEN, WHITE, pos, cohe_center, 2)
                        pygame.draw.circle(SCREEN, RED, (int(cohe_center[0]), int(cohe_center[1])), 5)
            else:
                buttons[5] = Button("Zones", text_color=RED)

        # Display "PAUSE" text if the simulation is paused
        buttons[4] = Button("Pause", text_color=RED)
        if not running:
            flock.draw(SCREEN)
            buttons[4] = Button("Pause", text_color=GREEN)
            Text("PAUSE", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, ORANGE, 70).draw()

        # Display buttons
        x_offset = 20
        for button in buttons[1:]:
            button.draw(surface=SCREEN, x=x_offset, y=y_offset_bottom)
            x_offset += button.rect.width + margin
        buttons[0].draw(surface=SCREEN, x=20, y=y_offset_top)

        # Draw sliders
        for slider in sliders:
            slider.draw(bar_color=WHITE, cursor_color=ORANGE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            # Slider handling
            for i, slider in enumerate(sliders):
                if event.type == pygame.MOUSEBUTTONDOWN and slider.handle_event(event):
                    pass
                elif event.type == pygame.MOUSEBUTTONUP:
                    slider.handle_event(event)

                elif event.type == pygame.MOUSEMOTION:
                    slider.handle_event(event)

            # Button handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.handle_event(event):
                        if i == 0:  # Back
                            return_to_menu()
                        elif i == 1:  # Reset
                            flock = Flock(nbBoids)
                        elif i == 2:  # Add
                            flock.add_boids(25)
                        elif i == 3:  # Remove
                            flock.remove_boids(25)
                        elif i == 4:  # Pause
                            running = not running
                        elif i == 5:  # Zones (index shifted because Grid removed)
                            zone_on = not zone_on

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_menu()

        # Display FPS and boid count
        Text(
            f"~fps: {round(CLOCK.get_fps())}     ~Number of boids: {flock.num_boids}",
            WINDOW_WIDTH // 2,
            30,
            color=ORANGE,
            taille=25,
        ).draw()

        pygame.display.update()
        CLOCK.tick(FPS)


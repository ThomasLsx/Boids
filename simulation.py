# Simulation.py
import pygame
import random as rd
from math import pi
from Boids import Boid, Quadtree
from ui import Button, Text, SliderButton
from config import quit_game, SCREEN, CLOCK, FPS, WINDOW_HEIGHT, WINDOW_WIDTH, BLACK, ORANGE, WHITE, BLUE, RED, GREEN

# Initialisation des boids
nbBoids = 100

# Création des boutons
button_labels = ["Retour", "Reset", "Ajouter", "Retirer", "Pause", "Grille", "Zones"]
buttons = []
x_offset = 20
y_offset_top = 20
y_offset_bottom = WINDOW_HEIGHT - 55
margin = 5

for label in button_labels:
    button = Button(label)
    buttons.append(button)

# Création des sliders
slider_labels = ["Cohésion", "Alignement", "Distanciation", "Vitesse Max"]
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
    global boids

    running = True
    grid_active = True
    zone_on = False

    # Initialisation des boids
    boids = [Boid(rd.randint(0, WINDOW_WIDTH), rd.randint(0, WINDOW_HEIGHT)) for _ in range(nbBoids)]
    
    # Créer le quadtree une seule fois en dehors de la boucle principale
    quadtree = Quadtree(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, capacity=5, max_depth=6)

    while True:
        SCREEN.fill(BLACK)

        if running:
            # Réinitialiser le quadtree (plus efficace que de le recréer)
            quadtree.boids.clear()
            quadtree.divided = False

            # Réinsérer tous les boids
            for boid in boids:
                quadtree.insert(boid)

            for boid in boids:
                # Créer le rectangle de recherche une seule fois
                search_radius = max(boid.vision, boid.separation_slider)
                range_rect = pygame.Rect(
                    boid.position.x - search_radius, 
                    boid.position.y - search_radius, 
                    search_radius * 2, 
                    search_radius * 2
                )
                
                # Rechercher les boids à proximité de manière plus efficace
                nearby_boids = quadtree.query(range_rect)
                
                boid.apply_behaviors(nearby_boids)
                boid.move()
                boid.Draw()

            if grid_active:
                buttons[5] = Button("Grille", text_color=GREEN)
                quadtree.Draw() 
            else:
                buttons[5] = Button("Grille", text_color=RED)

            if zone_on:
                buttons[6] = Button("Zones", text_color=GREEN)
                if len(boids) > 0:
                    boid = boids[0]
                    start_angle = -boid.vision_angle / 2
                    end_angle = boid.vision_angle / 2
                    direction_angle = boid.velocity.angle_to(pygame.math.Vector2(1, 0))
                    if boid.separation_slider > 1:
                        pygame.draw.arc(SCREEN, BLUE, (boid.position.x - boid.separation_slider, boid.position.y - boid.separation_slider, boid.separation_slider * 2, boid.separation_slider * 2), (start_angle + direction_angle) * pi / 180, (end_angle + direction_angle) * pi / 180, 2)
                    if boid.alignment_slider > 1:
                        pygame.draw.arc(SCREEN, RED, (boid.position.x - boid.alignment_slider, boid.position.y - boid.alignment_slider, boid.alignment_slider * 2, boid.alignment_slider * 2), (start_angle + direction_angle) * pi / 180, (end_angle + direction_angle) * pi / 180, 2)
                        pygame.draw.line(SCREEN, ORANGE, boid.position, boid.position + 30 * boid.velocity, 2)
                    if boid.cohesion_slider > 1:
                        pygame.draw.arc(SCREEN, GREEN, (boid.position.x - boid.cohesion_slider, boid.position.y - boid.cohesion_slider, boid.cohesion_slider * 2, boid.cohesion_slider * 2), (start_angle + direction_angle) * pi / 180, (end_angle + direction_angle) * pi / 180, 2)
                        pygame.draw.line(SCREEN, WHITE, boid.position, boid.point_cohe, 2)
                        pygame.draw.circle(SCREEN, RED, boid.point_cohe, 5)
            else:
                buttons[6] = Button("Zones", text_color=RED)

        # Affichage du texte "PAUSE" si la simulation est en pause
        buttons[4] = Button("Pause", text_color=RED)
        if not running:
            for boid in boids:
                boid.Draw()
            if grid_active:
                quadtree.Draw()
            buttons[4] = Button("Pause", text_color=GREEN)
            Text("PAUSE", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, ORANGE, 70).Draw()

        # Affichage des boutons
        x_offset = 20
        for button in buttons[1:]:
            button.draw(x=x_offset, y=y_offset_bottom)
            x_offset += button.rect.width + margin
        buttons[0].draw(x=20, y=y_offset_top)

        # Dessin des sliders
        for slider in sliders:
            slider.draw(bar_color=WHITE, cursor_color=ORANGE)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            # Gestion des sliders
            for i, slider in enumerate(sliders):
                if event.type == pygame.MOUSEBUTTONDOWN and slider.handle_event(event):
                    pass
                elif event.type == pygame.MOUSEBUTTONUP:
                    slider.handle_event(event)

                elif event.type == pygame.MOUSEMOTION:
                    slider.handle_event(event)
                    if slider.dragging:
                        if i == 0:  # Cohesion
                            for boid in boids:
                                boid.cohesion_slider = boid.vision * slider.current_val / 100
                        elif i == 1:  # Alignement
                            for boid in boids:
                                boid.alignment_slider = boid.vision * slider.current_val / 100
                        elif i == 2:  # Distance
                            for boid in boids:
                                boid.separation_slider = boid.avoid_radius * slider.current_val / 100
                        elif i == 3:  # Max Speed
                            for boid in boids:
                                boid.speed_slider = max(0.1, boid.max_speed * slider.current_val / 100)

            # Gestion des boutons
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.handle_event(event):
                        if i == 0:  # Retour
                            return_to_menu()
                        elif i == 1:  # Reset
                            boids = [Boid(rd.randint(0, WINDOW_WIDTH), rd.randint(0, WINDOW_HEIGHT)) for _ in range(nbBoids)]
                        elif i == 2:  # Ajouter
                            if len(boids) + 25 <= 100000:  # Limite arbitraire
                                boids.extend([Boid(rd.randint(0, WINDOW_WIDTH), rd.randint(0, WINDOW_HEIGHT)) for _ in range(25)])
                        elif i == 3:  # Retirer
                            if len(boids) >= 25:
                                del boids[-25:]
                        elif i == 4:  # Pause
                            running = not running
                        elif i == 5:  # Grille
                            grid_active = not grid_active
                        elif i == 6:  # Zones
                            zone_on = not zone_on

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_menu()

        # Affichage des FPS et du nombre de boids
        Text(
            f"~fps: {round(CLOCK.get_fps())}     ~Nombres de boids: {len(boids)}",
            WINDOW_WIDTH // 2,
            30,
            color=ORANGE,
            taille=25,
        ).Draw()

        pygame.display.update()
        CLOCK.tick_busy_loop(FPS)


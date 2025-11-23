#credit.py
import pygame
from ui import Text
from config import quit_game, SCREEN, WINDOW_HEIGHT, WINDOW_WIDTH, WHITE, GREEN, CLOCK, correcteur_police

class Credits:
    def __init__(self):
        # Texte des crédits
        self.credits_text = [
            "Projet Boids",
            "",
            "Développé par :",
            "BARTCZAK Antoine",
            "BRIAUT Lilian",
            "LESIEUX Thomas",
            
            "",
            "École Polytech de l'Université de Dijon",
            "Année 2024-2025",
        ]
        self.taille = 30  # Taille de la police

    def run(self, return_to_menu):
        while True:
            # Fond noir
            SCREEN.fill((0, 0, 0))

            # Calcul de la hauteur totale du bloc de texte
            total_text_height = len(self.credits_text) * self.taille * correcteur_police
            # Calcul de la coordonnée y de départ pour centrer le bloc de texte
            start_y = (WINDOW_HEIGHT - total_text_height) // 2

            # Affichage de chaque ligne de texte
            for i, line in enumerate(self.credits_text):
                Text(line, WINDOW_WIDTH // 2, start_y + i * self.taille * correcteur_police, WHITE, self.taille).Draw()

            # Bouton retour
            return_button = Text(
                "Retour", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100, GREEN, 50
            ).Draw()

            # Mise à jour de l'affichage
            pygame.display.update()

            # Gestion des événements
            for event in pygame.event.get():
                # Fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    quit_game()
                # Clic de souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Clic sur le bouton retour
                    if return_button.collidepoint(event.pos):
                        return_to_menu()
                # Appui sur une touche
                if event.type == pygame.KEYDOWN:
                    # Touche Echap
                    if event.key == pygame.K_ESCAPE:
                        return_to_menu()
                    # Touche Entrée
                    if event.key == pygame.K_RETURN:
                        return_to_menu()

            # Limitation de la fréquence d'images
            CLOCK.tick(30)


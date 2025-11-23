# Importation des modules nécessaires
import pygame
import simulation
from ui import Text
from credit import Credits
from config import quit_game, SCREEN, CLOCK, FPS, WINDOW_HEIGHT, WINDOW_WIDTH, WHITE, GREEN

# Fonction principale du menu
def menu():
    credits_use = Credits()  # Instance de la classe Credits
    
    # Options du menu : texte affiché et action associée
    options = [
        ("Simulation", simulation.run),  # Option pour lancer la simulation
        ("Crédits", credits_use.run),  # Option pour afficher les crédits
        ("Quitter", quit_game),  # Option pour quitter le jeu
    ]
    selected = 0  # Index de l'option sélectionnée

    # Chargement et mise à l'échelle de l'image de fond (commenté)
    # background_image = pygame.image.load("data/acceuil.jpeg").convert() # .convert() pour optimiser l'affichage
    # background_image = pygame.transform.scale(background_image, (WINDOW_HEIGHT, WINDOW_WIDTH))
    # background_image.set_alpha(150)

    while True:
        SCREEN.fill((0, 0, 0))  # Efface l'écran
        # SCREEN.blit(background_image, (0, 0)) # Affiche l'image de fond (commenté)

        # Dessiner les options de menu
        option_rects = []  # Liste pour stocker les rectangles de collision des options
        for i, (text, action) in enumerate(options):  # Itère sur les options
            # Crée un objet Text pour chaque option et le dessine
            option_text = Text(
                text,  # Texte de l'option
                WINDOW_WIDTH // 2,  # Position x centrée
                (i + 1) * WINDOW_HEIGHT // (len(options) + 1),  # Position y dynamique en fonction du nombre d'options
                GREEN if selected == i else WHITE,  # Couleur verte si sélectionnée, blanche sinon
                50,  # Taille de la police
            ).Draw()  # Dessine le texte et retourne son rectangle de collision
            option_rects.append(option_text)  # Ajoute le rectangle à la liste

        pygame.display.update()  # Met à jour l'affichage

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Fermeture de la fenêtre
                quit_game()

            if event.type == pygame.KEYDOWN:  # Appui d'une touche
                if event.key == pygame.K_ESCAPE:  # Touche Echap
                    quit_game()
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected = (selected + 1) % len(options)  # Sélectionne l'option suivante
                elif event.key == pygame.K_UP:  # Flèche haut
                    selected = (selected - 1) % len(options)  # Sélectionne l'option précédente
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    options[selected][1](None if selected == 2 else menu)  # Exécute l'action associée à l'option sélectionnée

            if event.type == pygame.MOUSEBUTTONDOWN:  # Clic de souris
                for i, option_rect in enumerate(option_rects):  # Itère sur les rectangles de collision
                    if option_rect.collidepoint(event.pos):  # Vérifie si le clic est sur une option
                        options[i][1](None if options[i][1] == quit_game else menu)  # Exécute l'action, passe menu à simulation.run si nécessaire
                        break  # Sort de la boucle après un clic

        CLOCK.tick(FPS)  # Limite la fréquence de rafraîchissement

# Fonction principale du programme
def main():
    menu()  # Lance le menu

# Point d'entrée du programme
if __name__ == "__main__":
    main()  # Exécute la fonction main si le script est exécuté directement

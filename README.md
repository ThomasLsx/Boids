**Boids**

![CI](https://github.com/ThomasLsx/Boids/actions/workflows/python-ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)

Description
Le projet Boids est une simulation en Python des comportements collectifs (boids) basée sur l'approche de Craig Reynolds. L'affichage est fait avec Pygame.

Fonctionnalités
- Classe `Boid` : comportements (cohesion, separation, alignment, déplacement).
- `Quadtree` : accélère les recherches spatiales.
- Éléments UI : `Text`, `Button`, `SliderButton`.

Structure
- `main.py` : menu principal et point d'entrée.
- `simulation.py` : logique de la simulation.
- `Boids.py` : classes `Boid` et `Quadtree`.
- `ui.py` / `credit.py` / `config.py` : interface, crédits et configuration.

Installation (recommandé : environnement virtuel)
1. Créez et activez un environnement virtuel (Windows PowerShell) :
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```
2. Installez les dépendances :
```powershell
pip install -r requirements.txt
```

Exécution
```powershell
python main.py
```

Licence
Ce projet est sous licence MIT — voir le fichier `LICENSE`.

Contribution
Voir `CONTRIBUTING.md` pour les instructions de contribution et `CODE_OF_CONDUCT.md` pour le comportement attendu.

Crédits
- Antoine BARTCZAK
- Lilian BRIAUT
- Thomas LESIEUX
# Projet Boids

## Description
Le projet Boids est une simulation de comportement de groupe d'oiseaux ou de poissons (boids) utilisant le modèle de Craig Reynolds
pour les algorithmes de cohésion, séparation et alignement.
Le projet est développé en Python avec la bibliothèque Pygame pour l'affichage graphique.

## Fonctionnalités
- **Boid class**: Gère les comportements individuels des boids.
  - `in_vision_cone(other)`
  - `cohesion(boids)`
  - `separation(boids)`
  - `alignment(boids)`
  - `apply_force(force)`
  - `apply_behaviors(boids)`
  - `move()`
  - `Draw()`

- **Quadtree class**: Optimise la recherche spatiale pour les boids.
  - `subdivide()`
  - `insert(boid)`
  - `query(range_rect)`
  - `Draw()`

- **UI Elements**: Composants graphiques pour l'interaction utilisateur.
  - `Text`
  - `Button`
  - `SliderButton`

## Configuration
Le fichier `config.py` contient les paramètres de configuration et initialise Pygame, définit les couleurs, crée la fenêtre et gère les FPS.

## Simulation
Le fichier `simulation.py` contient la logique principale de la simulation, y compris la création des boutons et sliders, et la boucle principale de la simulation.

## Menu Principal
Le fichier `main.py` définit les fonctions pour le menu principal et le lancement de l'application.

## Crédits
Le fichier `credit.py` affiche les informations de crédit pour le projet.

## Installation et Exécution
1. Clonez le dépôt:
    ```sh
    git clone https://github.com/Bouhbou/Biods.git
    ```
2. Installez les dépendances requises:
    ```sh
    pip install pygame
    ```
3. Exécutez l'application:
    ```sh
    python main.py
    ```

## Contributeurs
- Antoine BARTCZAK
- Lilian BRIAUT
- Thomas LESIEUX

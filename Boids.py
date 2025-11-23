# Boid.py
import pygame
import random as rd
from config import WINDOW_HEIGHT, WINDOW_WIDTH, SCREEN, WHITE, RED, GREEN, BLUE, GRAY, VIOLET


class Boid:
    def __init__(self, x=0, y=0):
        # Initialisation des attributs du boid
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(rd.uniform(-2, 2), rd.uniform(-2, 2))
        self.smoothed_direction = self.velocity.normalize() if self.velocity.length() > 0 else pygame.math.Vector2(1, 0)
        self.sizeBoids = 10
        self.max_speed = 2
        self.min_speed = 1
        self.speed_slider = self.max_speed 
        self.vision = 200
        self.vision_angle = 270
        self.cohesion_slider = self.vision
        self.alignment_slider = self.vision
        self.avoid_radius = self.sizeBoids * 2.5
        self.separation_slider = self.avoid_radius
        self.color = WHITE
        self.frame_counter = 0
        self.point_cohe = self.position 

    def move(self):
        """Déplace le boid et gère le bord de l'écran."""
        # Ajuste la vitesse si elle est trop lente
        if self.velocity.length() < self.min_speed:
            self.velocity = self.velocity.normalize() * self.min_speed
        # Met à jour la position
        self.position += self.velocity 
        # Gère le bord de l'écran
        self.position.x %= WINDOW_WIDTH
        self.position.y %= WINDOW_HEIGHT

    def apply_force(self, force):
        """Applique une force (vecteur) au boid."""
        self.velocity += force
        # Limite la vitesse à la valeur du slider
        if self.velocity.length() > self.speed_slider:
            self.velocity.scale_to_length(self.speed_slider)

    def in_vision_cone(self, other):
        """Vérifie si un autre boid est dans le cône de vision."""
        direction_to_other = other.position - self.position
        angle = self.velocity.angle_to(direction_to_other)
        return abs(angle) < self.vision_angle / 2

    def cohesion(self, boids):
        """Calcule la force de cohésion en combinant calcul différé, distance minimale, et réduction en zones denses."""
        if self.cohesion_slider > 1:
            # Calcul différé : tous les 5 frames 
            self.frame_counter += 1
            if self.frame_counter % 5 != 0:  # Changez 5 pour ajuster la fréquence
                return pygame.math.Vector2(0, 0)  
            self.frame_counter = 0
            center_mass = pygame.math.Vector2(0, 0)
            count = 0
            for other in boids:
                if other != self and self.position.distance_to(other.position) < self.cohesion_slider and self.in_vision_cone(other):
                    center_mass += other.position
                    count += 1

            if count > 0:
                center_mass /= count
                self.point_cohe = center_mass
                # Calcul de la force de cohésion, réduit en zones denses
                force = (center_mass - self.position) * 0.01
                return force / count  # Diminue la force si beaucoup de boids sont proches
        self.point_cohe = self.position
        return pygame.math.Vector2(0, 0)      

    def separation(self, boids):
        """Calcule la force de séparation."""
        steer = pygame.math.Vector2(0, 0)
        for other in boids:
            if other != self and self.position.distance_to(other.position) < self.separation_slider and self.in_vision_cone(other):
                steer -= (other.position - self.position)
        return steer * 0.03  # Ajuste la force

    def alignment(self, boids):
        """Calcule la force d'alignement."""
        if self.alignment_slider > 1:
            average_velocity = pygame.math.Vector2(0, 0)
            count = 0
            for other in boids:
                if other != self and self.position.distance_to(other.position) < self.alignment_slider and self.in_vision_cone(other):
                    average_velocity += other.velocity
                    count += 1
            if count > 0:
                average_velocity /= count
                return (average_velocity - self.velocity) * 0.03  # Ajuste la force
        return pygame.math.Vector2(0, 0)

    def apply_behaviors(self, boids):
        """Applique toutes les règles (cohésion, séparation, alignement)."""
        force_cohesion = self.cohesion(boids)
        force_separation = self.separation(boids)
        force_alignment = self.alignment(boids)

        self.apply_force(force_cohesion)
        self.apply_force(force_separation)
        self.apply_force(force_alignment)
 
    def Draw(self):
        # Lissage de la direction
        if self.velocity.length() > 0:
            target_direction = self.velocity.normalize()
            self.smoothed_direction = self.smoothed_direction.lerp(target_direction, 0.2)  # Facteur de lissage (0.2)

        # Taille du triangle
        base_length = self.sizeBoids 
        height = self.sizeBoids * 1.5

        # Calcul des sommets du triangle
        front = self.position + self.smoothed_direction * height  # Sommet avant
        left = self.position + self.smoothed_direction.rotate(135) * base_length  # Coin gauche
        right = self.position + self.smoothed_direction.rotate(-135) * base_length  # Coin droit

        # Couleur en fonction des états
        if self.cohesion_slider > self.alignment_slider and self.cohesion_slider > self.separation_slider:
            self.color = GREEN
        elif self.alignment_slider > self.cohesion_slider and self.alignment_slider > self.separation_slider:
            self.color = RED
        elif self.separation_slider > self.cohesion_slider and self.separation_slider > self.alignment_slider:
            self.color = BLUE
        else :
            self.color = VIOLET

        # Dessiner le triangle
        pygame.draw.polygon(SCREEN, self.color, [front, left, right])
        # pygame.draw.circle(SCREEN, self.color, self.position, self.sizeBoids)


        

class Quadtree:
    def __init__(self, x, y, width, height, capacity=5, depth=0, max_depth=6):
        # Initialisation des attributs du quadtree
        self.boundary = pygame.Rect(x, y, width, height) 
        self.capacity = capacity 
        self.boids = [] 
        self.divided = False
        self.depth = depth
        self.max_depth = max_depth
        
        # Initialiser à None pour éviter l'AttributeError
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def subdivide(self):
        # Vérifier la profondeur maximale
        if self.depth >= self.max_depth:
            return False

        w, h = self.boundary.width // 2, self.boundary.height // 2
        x, y = self.boundary.x, self.boundary.y
        
        # Créer les sous-quadrants
        self.northwest = Quadtree(x, y, w, h, self.capacity, self.depth + 1, self.max_depth)
        self.northeast = Quadtree(x + w, y, w, h, self.capacity, self.depth + 1, self.max_depth)
        self.southwest = Quadtree(x, y + h, w, h, self.capacity, self.depth + 1, self.max_depth)
        self.southeast = Quadtree(x + w, y + h, w, h, self.capacity, self.depth + 1, self.max_depth)
        
        self.divided = True
        return True

    def insert(self, boid):
        # Vérifier si le boid est dans le rectangle
        if not self.boundary.collidepoint(boid.position.x, boid.position.y):
            return False
        
        # Si la capacité n'est pas atteinte, insérer
        if len(self.boids) < self.capacity:
            self.boids.append(boid)
            return True
        
        # Si le noeud n'est pas divisé, essayer de subdiviser
        if not self.divided:
            if not self.subdivide():
                # Si la subdivision échoue (profondeur max), forcer l'insertion
                self.boids.append(boid)
                return True
        
        # Essayer d'insérer dans les sous-quadrants
        if self.northwest.insert(boid):
            return True
        if self.northeast.insert(boid):
            return True
        if self.southwest.insert(boid):
            return True
        if self.southeast.insert(boid):
            return True
        
        # Si aucune insertion n'a réussi, ajouter au noeud actuel
        self.boids.append(boid)
        return True

    def query(self, range_rect):
        found = []
        
        # Vérifier l'intersection avec le rectangle de recherche
        if not self.boundary.colliderect(range_rect):
            return found
        
        # Ajouter les boids du noeud courant
        for boid in self.boids:
            if range_rect.collidepoint(boid.position.x, boid.position.y):
                found.append(boid)
        
        # Si le noeud est divisé, rechercher dans les sous-quadrants
        if self.divided:
            found.extend(self.northwest.query(range_rect))
            found.extend(self.northeast.query(range_rect))
            found.extend(self.southwest.query(range_rect))
            found.extend(self.southeast.query(range_rect))
        
        return found

    def Draw(self):
        # Dessine le quadtree
        pygame.draw.rect(SCREEN, GRAY, self.boundary, 1)
        if self.divided:
            self.northwest.Draw()
            self.northeast.Draw()
            self.southwest.Draw()
            self.southeast.Draw()
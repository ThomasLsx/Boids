# Boid.py
import pygame
import random as rd
from config import WINDOW_HEIGHT, WINDOW_WIDTH, SCREEN, WHITE, RED, GREEN, BLUE, GRAY, VIOLET


class Boid:
    def __init__(self, x=0, y=0):
        # Initialization of the boid's attributes
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
        """Moves the boid and handles screen wrapping."""
        # Adjust speed if it's too slow
        if self.velocity.length() < self.min_speed:
            self.velocity = self.velocity.normalize() * self.min_speed
        # Update position
        self.position += self.velocity 
        # Handle screen wrapping
        self.position.x %= WINDOW_WIDTH
        self.position.y %= WINDOW_HEIGHT

    def apply_force(self, force):
        """Applies a force (vector) to the boid."""
        self.velocity += force
        # Limit the speed to the slider value
        if self.velocity.length() > self.speed_slider:
            self.velocity.scale_to_length(self.speed_slider)

    def in_vision_cone(self, other):
        """Checks if another boid is in the vision cone."""
        direction_to_other = other.position - self.position
        angle = self.velocity.angle_to(direction_to_other)
        return abs(angle) < self.vision_angle / 2

    def apply_behaviors(self, boids):
        """Applies all rules (cohesion, separation, alignment) in a single loop."""
        center_mass = pygame.math.Vector2(0, 0)
        average_velocity = pygame.math.Vector2(0, 0)
        steer_separation = pygame.math.Vector2(0, 0)
        cohesion_count = 0
        alignment_count = 0
        separation_count = 0

        self.frame_counter += 1
        use_cohesion = self.cohesion_slider > 1 and self.frame_counter % 5 == 0

        for other in boids:
            if other != self:
                distance = self.position.distance_to(other.position)
                if self.in_vision_cone(other):
                    # Cohesion
                    if use_cohesion and distance < self.cohesion_slider:
                        center_mass += other.position
                        cohesion_count += 1
                    
                    # Alignment
                    if self.alignment_slider > 1 and distance < self.alignment_slider:
                        average_velocity += other.velocity
                        alignment_count += 1

                    # Separation
                    if distance < self.separation_slider:
                        steer_separation -= (other.position - self.position)
                        separation_count += 1

        # Apply Cohesion Force
        if use_cohesion:
            if cohesion_count > 0:
                center_mass /= cohesion_count
                self.point_cohe = center_mass
                force_cohesion = (center_mass - self.position) * 0.01 / cohesion_count
                self.apply_force(force_cohesion)
            else:
                self.point_cohe = self.position
            if self.frame_counter % 5 == 0:
                self.frame_counter = 0

        # Apply Alignment Force
        if self.alignment_slider > 1 and alignment_count > 0:
            average_velocity /= alignment_count
            force_alignment = (average_velocity - self.velocity) * 0.03
            self.apply_force(force_alignment)

        # Apply Separation Force
        if separation_count > 0:
            force_separation = steer_separation * 0.03
            self.apply_force(force_separation)
 
    def Draw(self):
        # Smooth the direction
        if self.velocity.length() > 0:
            target_direction = self.velocity.normalize()
            self.smoothed_direction = self.smoothed_direction.lerp(target_direction, 0.2)  # Smoothing factor (0.2)

        # Triangle size
        base_length = self.sizeBoids 
        height = self.sizeBoids * 1.5

        # Calculate triangle vertices
        front = self.position + self.smoothed_direction * height  # Front vertex
        left = self.position + self.smoothed_direction.rotate(135) * base_length  # Left corner
        right = self.position + self.smoothed_direction.rotate(-135) * base_length  # Right corner

        # Color based on states
        if self.cohesion_slider > self.alignment_slider and self.cohesion_slider > self.separation_slider:
            self.color = GREEN
        elif self.alignment_slider > self.cohesion_slider and self.alignment_slider > self.separation_slider:
            self.color = RED
        elif self.separation_slider > self.cohesion_slider and self.separation_slider > self.alignment_slider:
            self.color = BLUE
        else :
            self.color = VIOLET

        # Draw the triangle
        pygame.draw.polygon(SCREEN, self.color, [front, left, right])
        # pygame.draw.circle(SCREEN, self.color, self.position, self.sizeBoids)


        

class Quadtree:
    def __init__(self, x, y, width, height, capacity=5, depth=0, max_depth=6):
        # Initialization of the quadtree attributes
        self.boundary = pygame.Rect(x, y, width, height) 
        self.capacity = capacity 
        self.boids = [] 
        self.divided = False
        self.depth = depth
        self.max_depth = max_depth
        
        # Initialize to None to avoid AttributeError
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def subdivide(self):
        # Check maximum depth
        if self.depth >= self.max_depth:
            return False

        w, h = self.boundary.width // 2, self.boundary.height // 2
        x, y = self.boundary.x, self.boundary.y
        
        # Create sub-quadrants
        self.northwest = Quadtree(x, y, w, h, self.capacity, self.depth + 1, self.max_depth)
        self.northeast = Quadtree(x + w, y, w, h, self.capacity, self.depth + 1, self.max_depth)
        self.southwest = Quadtree(x, y + h, w, h, self.capacity, self.depth + 1, self.max_depth)
        self.southeast = Quadtree(x + w, y + h, w, h, self.capacity, self.depth + 1, self.max_depth)
        
        self.divided = True
        return True

    def insert(self, boid):
        # Check if the boid is in the rectangle
        if not self.boundary.collidepoint(boid.position.x, boid.position.y):
            return False
        
        # If capacity is not reached, insert
        if len(self.boids) < self.capacity:
            self.boids.append(boid)
            return True
        
        # If the node is not divided, try to subdivide
        if not self.divided:
            if not self.subdivide():
                # If subdivision fails (max depth), force insertion
                self.boids.append(boid)
                return True
        
        # Try to insert into sub-quadrants
        if self.northwest.insert(boid):
            return True
        if self.northeast.insert(boid):
            return True
        if self.southwest.insert(boid):
            return True
        if self.southeast.insert(boid):
            return True
        
        # If no insertion was successful, add to the current node
        self.boids.append(boid)
        return True

    def query(self, range_rect):
        found = []
        
        # Check for intersection with the search rectangle
        if not self.boundary.colliderect(range_rect):
            return found
        
        # Add boids from the current node
        for boid in self.boids:
            if range_rect.collidepoint(boid.position.x, boid.position.y):
                found.append(boid)
        
        # If the node is divided, search in the sub-quadrants
        if self.divided:
            found.extend(self.northwest.query(range_rect))
            found.extend(self.northeast.query(range_rect))
            found.extend(self.southwest.query(range_rect))
            found.extend(self.southeast.query(range_rect))
        
        return found

    def Draw(self):
        # Draw the quadtree
        pygame.draw.rect(SCREEN, GRAY, self.boundary, 1)
        if self.divided:
            self.northwest.Draw()
            self.northeast.Draw()
            self.southwest.Draw()
            self.southeast.Draw()
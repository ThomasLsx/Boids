import numpy as np
import pygame
import math
from config import WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN, WHITE, RED, GREEN, BLUE, VIOLET

class Flock:
    def __init__(self, num_boids):
        self.num_boids = num_boids
        
        # Initialize arrays for positions and velocities
        self.positions = np.random.rand(num_boids, 2) * [WINDOW_WIDTH, WINDOW_HEIGHT]
        self.velocities = (np.random.rand(num_boids, 2) - 0.5) * 4  # Random vel between -2 and 2
        
        # Constants
        self.size_boids = 10
        self.max_speed = 2
        self.min_speed = 1
        self.vision = 200
        self.vision_angle = 270
        self.vision_cos = math.cos(math.radians(self.vision_angle / 2))
        self.avoid_radius = self.size_boids * 2.5
        
        # Pre-allocate arrays for performance
        self.colors = np.full((num_boids, 3), WHITE, dtype=int)
        self.cohesion_centers = self.positions.copy()

    def update(self, cohesion_val, alignment_val, separation_val, max_speed_val):
        # Update max speed based on slider
        self.max_speed = max(0.1, max_speed_val)
        
        # Calculate squared distances between all pairs (N x N matrix)
        # Using broadcasting: (N, 1, 2) - (1, N, 2) -> (N, N, 2)
        diff_matrix = self.positions[:, np.newaxis, :] - self.positions[np.newaxis, :, :]
        dist_sq_matrix = np.sum(diff_matrix**2, axis=2)
        
        # Avoid self-interaction (set diagonal to infinity)
        np.fill_diagonal(dist_sq_matrix, np.inf)
        
        # Vision mask: check distance
        vision_mask = dist_sq_matrix < self.vision**2
        
        # Vision angle mask
        # Normalize velocities
        vel_norms = np.linalg.norm(self.velocities, axis=1, keepdims=True)
        vel_norms[vel_norms == 0] = 1 # Avoid division by zero
        normalized_vels = self.velocities / vel_norms
        
        # Normalize diff vectors
        dist_matrix = np.sqrt(dist_sq_matrix)
        dist_matrix[dist_matrix == 0] = 1 # Avoid division by zero
        normalized_diffs = diff_matrix / dist_matrix[:, :, np.newaxis]
        
        # Dot product for angle check
        # (N, 1, 2) * (N, N, 2) -> (N, N, 2) -> sum axis 2 -> (N, N)
        dot_products = np.sum(normalized_vels[:, np.newaxis, :] * normalized_diffs, axis=2)
        angle_mask = dot_products > self.vision_cos
        
        # Combined neighbor mask
        neighbor_mask = vision_mask & angle_mask
        
        # --- Cohesion ---
        if cohesion_val > 1:
            # Sum positions of neighbors
            # (N, N, 1) * (1, N, 2) -> (N, N, 2) -> sum axis 1 -> (N, 2)
            neighbor_counts = np.sum(neighbor_mask, axis=1, keepdims=True)
            neighbor_counts[neighbor_counts == 0] = 1 # Avoid div by zero
            
            center_mass = np.sum(self.positions[np.newaxis, :, :] * neighbor_mask[:, :, np.newaxis], axis=1) / neighbor_counts
            
            # Vector to center
            vec_to_center = center_mass - self.positions
            
            # Normalize and scale
            dist_to_center = np.linalg.norm(vec_to_center, axis=1, keepdims=True)
            dist_to_center[dist_to_center == 0] = 1
            
            desired_vel = (vec_to_center / dist_to_center) * self.max_speed
            cohesion_force = (desired_vel - self.velocities) * 0.01
            
            # Apply only if there are neighbors and distance < slider
            # Note: simplified logic compared to original loop, but vectorized
            # Original checked distance < cohesion_slider individually
            # Here we apply a global mask for cohesion range
            cohesion_range_mask = dist_sq_matrix < cohesion_val**2
            final_cohesion_mask = neighbor_mask & cohesion_range_mask
            
            # Re-calculate center mass with specific cohesion range
            cohesion_counts = np.sum(final_cohesion_mask, axis=1, keepdims=True)
            has_cohesion_neighbors = cohesion_counts > 0
            cohesion_counts[cohesion_counts == 0] = 1
            
            center_mass_c = np.sum(self.positions[np.newaxis, :, :] * final_cohesion_mask[:, :, np.newaxis], axis=1) / cohesion_counts
            
            # Store for visualization
            self.cohesion_centers = center_mass_c
            
            vec_to_center_c = center_mass_c - self.positions
            dist_to_center_c = np.linalg.norm(vec_to_center_c, axis=1, keepdims=True)
            dist_to_center_c[dist_to_center_c == 0] = 1
            desired_vel_c = (vec_to_center_c / dist_to_center_c) * self.max_speed
            cohesion_force = (desired_vel_c - self.velocities) * 0.01
            
            self.velocities += cohesion_force * has_cohesion_neighbors

        # --- Alignment ---
        if alignment_val > 1:
            alignment_range_mask = dist_sq_matrix < alignment_val**2
            final_alignment_mask = neighbor_mask & alignment_range_mask
            
            alignment_counts = np.sum(final_alignment_mask, axis=1, keepdims=True)
            has_alignment_neighbors = alignment_counts > 0
            alignment_counts[alignment_counts == 0] = 1
            
            avg_vel = np.sum(self.velocities[np.newaxis, :, :] * final_alignment_mask[:, :, np.newaxis], axis=1) / alignment_counts
            alignment_force = (avg_vel - self.velocities) * 0.03
            
            self.velocities += alignment_force * has_alignment_neighbors

        # --- Separation ---
        separation_range_mask = dist_sq_matrix < separation_val**2
        # Separation doesn't strictly need vision cone in some implementations, but let's keep it consistent
        # Actually original code checked vision cone first.
        # But separation usually overrides vision cone (360 degrees) for collision avoidance? 
        # Original code: "if self.in_vision_cone(other): ... if dist < separation_slider"
        # So it respects vision cone.
        final_separation_mask = neighbor_mask & separation_range_mask
        
        # Calculate repulsion vectors
        # diff_matrix is (self - other)
        # We want (self - other) / dist^2
        
        # Avoid division by zero (already handled by diagonal inf)
        # dist_sq_matrix has inf on diagonal
        
        repulsion = diff_matrix / (dist_sq_matrix[:, :, np.newaxis] + 1e-6) # Add epsilon
        
        # Sum repulsion vectors
        steer_separation = np.sum(repulsion * final_separation_mask[:, :, np.newaxis], axis=1)
        
        has_separation_neighbors = np.sum(final_separation_mask, axis=1, keepdims=True) > 0
        
        # Normalize and scale
        steer_len = np.linalg.norm(steer_separation, axis=1, keepdims=True)
        steer_len[steer_len == 0] = 1
        
        desired_separation = (steer_separation / steer_len) * self.max_speed
        separation_force = (desired_separation - self.velocities) * 0.05
        
        self.velocities += separation_force * has_separation_neighbors

        # --- Limit Speed ---
        speed = np.linalg.norm(self.velocities, axis=1, keepdims=True)
        over_speed = speed > self.max_speed
        self.velocities[over_speed[:, 0]] = (self.velocities[over_speed[:, 0]] / speed[over_speed[:, 0]]) * self.max_speed
        
        under_speed = (speed < self.min_speed) & (speed > 0)
        self.velocities[under_speed[:, 0]] = (self.velocities[under_speed[:, 0]] / speed[under_speed[:, 0]]) * self.min_speed

        # --- Update Positions ---
        self.positions += self.velocities
        
        # --- Wrap around screen ---
        self.positions[:, 0] %= WINDOW_WIDTH
        self.positions[:, 1] %= WINDOW_HEIGHT
        
        # --- Update Colors ---
        # Vectorized color logic is a bit complex to match exactly the if/elif/else structure
        # but we can do it with boolean indexing
        self.colors[:] = VIOLET
        
        # Conditions
        cond_green = (cohesion_val > alignment_val) & (cohesion_val > separation_val)
        cond_red = (alignment_val > cohesion_val) & (alignment_val > separation_val)
        cond_blue = (separation_val > cohesion_val) & (separation_val > alignment_val)
        
        # Apply global color (since sliders are global, all boids have same color logic usually)
        # Wait, the original code set color per boid based on sliders?
        # "if self.cohesion_slider > self.alignment_slider ..."
        # The sliders are global properties in the original code, but stored on boid?
        # "boid.cohesion_slider = boid.vision * slider.current_val / 100"
        # Yes, updated in main loop for all boids. So all boids have same color.
        
        if cond_green:
            self.colors[:] = GREEN
        elif cond_red:
            self.colors[:] = RED
        elif cond_blue:
            self.colors[:] = BLUE

    def draw(self, screen):
        # Draw all boids
        # Calculating vertices for N triangles
        
        # Normalized direction
        vel_norms = np.linalg.norm(self.velocities, axis=1, keepdims=True)
        vel_norms[vel_norms == 0] = 1
        directions = self.velocities / vel_norms
        
        # Rotate 135 degrees
        # Rotation matrix for +135 deg
        # [cos 135, -sin 135]
        # [sin 135,  cos 135]
        angle_left = np.radians(135)
        c_l, s_l = np.cos(angle_left), np.sin(angle_left)
        rot_left = np.array([[c_l, -s_l], [s_l, c_l]])
        
        angle_right = np.radians(-135)
        c_r, s_r = np.cos(angle_right), np.sin(angle_right)
        rot_right = np.array([[c_r, -s_r], [s_r, c_r]])
        
        # Front vertex: pos + dir * height
        height = self.size_boids * 1.5
        fronts = self.positions + directions * height
        
        # Left vertex: pos + rotate(dir, 135) * base
        base = self.size_boids
        # Apply rotation: (N, 2) dot (2, 2) -> (N, 2)
        left_dirs = np.dot(directions, rot_left.T)
        lefts = self.positions + left_dirs * base
        
        # Right vertex
        right_dirs = np.dot(directions, rot_right.T)
        rights = self.positions + right_dirs * base
        
        # Draw polygons
        # Pygame draw.polygon is not vectorized, so we must loop
        # But we can optimize by using fewer python object creations
        
        for i in range(self.num_boids):
            pygame.draw.polygon(screen, self.colors[i], [fronts[i], lefts[i], rights[i]])
            
    def add_boids(self, n):
        new_pos = np.random.rand(n, 2) * [WINDOW_WIDTH, WINDOW_HEIGHT]
        new_vel = (np.random.rand(n, 2) - 0.5) * 4
        self.positions = np.vstack((self.positions, new_pos))
        self.velocities = np.vstack((self.velocities, new_vel))
        self.colors = np.vstack((self.colors, np.full((n, 3), WHITE, dtype=int)))
        self.num_boids += n
        
    def remove_boids(self, n):
        if self.num_boids >= n:
            self.positions = self.positions[:-n]
            self.velocities = self.velocities[:-n]
            self.colors = self.colors[:-n]
            self.num_boids -= n

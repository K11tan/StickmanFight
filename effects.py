# effects.py - Particle effects and visual effects for the game

import pygame
import random
import math
from constants import *

class ParticleEffect:
    def __init__(self, x, y, color, count, size, speed, gravity):
        """
        Create a particle effect
        
        Args:
            x, y: Center position of the effect
            color: Base color of the particles
            count: Number of particles to create
            size: Maximum size of particles
            speed: Maximum speed of particles
            gravity: Gravity effect on particles
        """
        self.particles = []
        self.active = True
        
        # Create particles
        for i in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed_val = random.uniform(speed * 0.5, speed)
            
            particle = {
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed_val,
                "vy": math.sin(angle) * speed_val,
                "size": random.uniform(size * 0.5, size),
                "color": self.get_particle_color(color),
                "life": random.uniform(20, 40)  # Frames until particle disappears
            }
            
            self.particles.append(particle)
        
        self.gravity = gravity
    
    def get_particle_color(self, base_color):
        """Create a slightly varied color based on the base color"""
        r, g, b = base_color
        variation = 30
        
        r = max(0, min(255, r + random.randint(-variation, variation)))
        g = max(0, min(255, g + random.randint(-variation, variation)))
        b = max(0, min(255, b + random.randint(-variation, variation)))
        
        return (r, g, b)
    
    def update(self):
        """Update all particles in the effect"""
        # Check if any particles are still active
        if not self.particles:
            self.active = False
            return
        
        # Update each particle
        for particle in self.particles[:]:
            # Apply gravity
            particle["vy"] += self.gravity
            
            # Move particle
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            
            # Reduce life
            particle["life"] -= 1
            
            # Remove dead particles
            if particle["life"] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        """Draw all particles to the surface"""
        for particle in self.particles:
            # Calculate alpha based on remaining life
            alpha = int(255 * (particle["life"] / 40))
            
            # Create a surface for the particle with alpha
            particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
            
            # Get color with alpha
            r, g, b = particle["color"]
            color_alpha = (r, g, b, alpha)
            
            # Draw circle
            pygame.draw.circle(particle_surface, color_alpha, 
                              (particle["size"], particle["size"]), 
                              particle["size"])
            
            # Draw to main surface
            surface.blit(particle_surface, 
                        (particle["x"] - particle["size"], 
                         particle["y"] - particle["size"]))

class ExplosionEffect(ParticleEffect):
    def __init__(self, x, y):
        """Special explosion effect for special moves"""
        super().__init__(x, y, RED, 30, 15, 2.0, 0.05)
        
        # Add additional particles with different colors
        for i in range(15):
            angle = random.uniform(0, math.pi * 2)
            speed_val = random.uniform(1.0, 3.0)
            
            particle = {
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed_val,
                "vy": math.sin(angle) * speed_val,
                "size": random.uniform(5, 12),
                "color": self.get_particle_color(ORANGE),
                "life": random.uniform(30, 60)
            }
            
            self.particles.append(particle)
            
        for i in range(10):
            angle = random.uniform(0, math.pi * 2)
            speed_val = random.uniform(0.5, 2.0)
            
            particle = {
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed_val,
                "vy": math.sin(angle) * speed_val,
                "size": random.uniform(8, 20),
                "color": self.get_particle_color(YELLOW),
                "life": random.uniform(20, 50)
            }
            
            self.particles.append(particle)

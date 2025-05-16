# fighter.py - Fighter class and related functions

import pygame
import random
import math
from constants import *
from effects import ParticleEffect

class Fighter:
    def __init__(self, x, y, width, height, color, controls, is_player=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.is_player = is_player
        
        # Movement
        self.speed = FIGHTER_SPEED
        self.direction = "right" if x < SCREEN_WIDTH // 2 else "left"
        
        # Action state
        self.action = "idle"
        self.action_time = 0
        self.action_duration = 20  # frames
        
        # Combat stats
        self.health = 100
        self.energy = 100
        self.blocking = False
        
        # Special move
        self.special_ready = False
        self.special_meter = 0
        self.special_threshold = SPECIAL_THRESHOLD
        self.special_active = False
        
        # Combo system
        self.combo_counter = 0
        self.combo_timer = 0
        self.combo_timeout = COMBO_TIMEOUT
        
        # Controls (keyboard keys)
        self.controls = controls
        
        # Hit box
        self.hit_box = pygame.Rect(x - width // 2, y - height // 2, width, height)
        
        # Attack hitbox (for detecting hits)
        self.attack_box = pygame.Rect(0, 0, 0, 0)
        
        # CPU behavior
        self.cpu_decision_timer = 0
        self.cpu_action_duration = 0
        self.cpu_current_action = None
    
    def update(self, opponent):
        # Update hit box position
        self.hit_box.x = self.x - self.width // 2
        self.hit_box.y = self.y - self.height // 2
        
        # Handle action timer
        if self.action != "idle":
            self.action_time += 1
            if self.action_time >= self.action_duration:
                self.action = "idle"
                self.action_time = 0
                self.blocking = False
                self.special_active = False
        
        # Update combo timer
        if self.combo_counter > 0:
            self.combo_timer += 1
            if self.combo_timer >= self.combo_timeout:
                self.combo_counter = 0
                self.combo_timer = 0
        
        # Regenerate energy
        if self.energy < 100 and self.action == "idle":
            self.energy += 0.5
            if self.energy > 100:
                self.energy = 100
        
        # Check if special is ready
        if self.special_meter >= self.special_threshold:
            self.special_ready = True
        
        # Player controlled
        if self.is_player:
            self.handle_player_input()
        else:
            self.handle_cpu_ai(opponent)
        
        # Update attack hitbox based on action
        self.update_attack_box()
        
        # Check for hits on opponent
        self.check_hit(opponent)
    
    def update_attack_box(self):
        # Reset attack box
        self.attack_box.width = 0
        self.attack_box.height = 0
        
        # Only create attack box during attack animations
        if self.action == "punch":
            if self.direction == "right":
                self.attack_box.x = self.x + self.width // 2
                self.attack_box.y = self.y - self.height // 3
                self.attack_box.width = self.width // 2
                self.attack_box.height = self.height // 3
            else:
                self.attack_box.x = self.x - self.width
                self.attack_box.y = self.y - self.height // 3
                self.attack_box.width = self.width // 2
                self.attack_box.height = self.height // 3
                
        elif self.action == "kick":
            if self.direction == "right":
                self.attack_box.x = self.x + self.width // 2
                self.attack_box.y = self.y
                self.attack_box.width = self.width
                self.attack_box.height = self.height // 4
            else:
                self.attack_box.x = self.x - self.width
                self.attack_box.y = self.y
                self.attack_box.width = self.width
                self.attack_box.height = self.height // 4
                
        elif self.action == "special":
            # Special move has a larger attack area
            if self.direction == "right":
                self.attack_box.x = self.x + self.width // 3
                self.attack_box.y = self.y - self.height // 2
                self.attack_box.width = self.width
                self.attack_box.height = self.height
            else:
                self.attack_box.x = self.x - self.width
                self.attack_box.y = self.y - self.height // 2
                self.attack_box.width = self.width
                self.attack_box.height = self.height
    
    def check_hit(self, opponent):
        # Check if we're in the middle of an attack and it has reached the right frame
        if (self.action in ["punch", "kick", "special"] and 
            self.action_time == self.action_duration // 2):
            
            # Check if the attack box intersects with the opponent's hit box
            if self.attack_box.colliderect(opponent.hit_box):
                
                # Calculate damage based on attack type and combo
                damage = DAMAGE[self.action]
                
                # Apply combo bonus
                if self.combo_counter > 1:
                    damage += damage * COMBO_BONUS * (self.combo_counter - 1)
                
                # Check if opponent is blocking
                if opponent.blocking:
                    # Reduce damage if blocking
                    damage *= BLOCK_DAMAGE_REDUCTION
                    opponent.special_meter += damage  # Blocking builds special meter
                    
                    # Create particle effect for blocked attack
                    return [ParticleEffect(
                        opponent.x + (20 if opponent.direction == "right" else -20),
                        opponent.y - 30,
                        BLUE, 
                        5, 10, 0.2, 0.1
                    )]
                    
                else:
                    # Apply damage
                    opponent.health -= damage
                    
                    # Add to special meter
                    self.special_meter += damage * 2
                    
                    # Create particle effect for successful hit
                    particle_color = YELLOW if self.action == "punch" else ORANGE
                    if self.action == "special":
                        particle_color = RED
                        
                    hit_x = opponent.x + (10 if self.direction == "right" else -10)
                    
                    return [ParticleEffect(
                        hit_x,
                        opponent.y - self.height // 3,
                        particle_color,
                        10, 15, 0.5, 0.2
                    )]
            
        return []
    
    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        
        # Movement only if not in middle of action
        if self.action == "idle":
            # Move left
            if keys[self.controls["left"]]:
                self.x -= self.speed
                self.direction = "left"
                
                # Prevent moving off screen
                if self.x < self.width // 2:
                    self.x = self.width // 2
            
            # Move right
            if keys[self.controls["right"]]:
                self.x += self.speed
                self.direction = "right"
                
                # Prevent moving off screen
                if self.x > SCREEN_WIDTH - self.width // 2:
                    self.x = SCREEN_WIDTH - self.width // 2
            
            # Punch
            if keys[self.controls["punch"]] and self.energy >= ENERGY_COST["punch"]:
                self.action = "punch"
                self.action_time = 0
                self.energy -= ENERGY_COST["punch"]
                
                # Update combo
                self.combo_counter += 1
                self.combo_timer = 0
            
            # Kick
            if keys[self.controls["kick"]] and self.energy >= ENERGY_COST["kick"]:
                self.action = "kick"
                self.action_time = 0
                self.energy -= ENERGY_COST["kick"]
                
                # Update combo
                self.combo_counter += 1
                self.combo_timer = 0
            
            # Block
            if keys[self.controls["block"]] and self.energy >= ENERGY_COST["block"]:
                self.action = "block"
                self.action_time = 0
                self.energy -= ENERGY_COST["block"]
                self.blocking = True
            
            # Special
            if keys[self.controls["special"]] and self.special_ready and self.energy >= ENERGY_COST["special"]:
                self.action = "special"
                self.action_time = 0
                self.energy -= ENERGY_COST["special"]
                self.special_meter = 0
                self.special_ready = False
                self.special_active = True
                
                # Reset combo
                self.combo_counter = 0
                self.combo_timer = 0
    
    def handle_cpu_ai(self, opponent):
        # Simple AI behavior
        if self.action == "idle":
            # Update decision timer
            self.cpu_decision_timer += 1
            
            if self.cpu_decision_timer >= self.cpu_action_duration:
                # Make a new decision
                self.cpu_decision_timer = 0
                self.cpu_action_duration = random.randint(30, 90)  # Frames until next decision
                
                # Distance to opponent
                distance = abs(self.x - opponent.x)
                
                if distance > self.width * 2:
                    # Too far, move towards opponent
                    self.cpu_current_action = "move"
                    
                elif distance <= self.width * 1.2:
                    # In attack range
                    if opponent.action == "punch" or opponent.action == "kick" or opponent.action == "special":
                        # Opponent is attacking, try to block
                        if random.random() < 0.7 and self.energy >= ENERGY_COST["block"]:
                            self.action = "block"
                            self.action_time = 0
                            self.blocking = True
                            self.energy -= ENERGY_COST["block"]
                        else:
                            # Failed to block, try to attack back or move away
                            choice = random.choice(["punch", "kick", "move"])
                            self.cpu_current_action = choice
                    else:
                        # Opponent not attacking, choose an action
                        if self.special_ready and self.energy >= ENERGY_COST["special"] and random.random() < 0.3:
                            # Use special attack
                            self.action = "special"
                            self.action_time = 0
                            self.energy -= ENERGY_COST["special"]
                            self.special_meter = 0
                            self.special_ready = False
                            self.special_active = True
                        else:
                            # Regular attack
                            choice = random.choice(["punch", "kick", "block", "move"])
                            self.cpu_current_action = choice
                else:
                    # Medium distance, choose between moving and attacking
                    choice = random.choice(["punch", "kick", "move", "move"])
                    self.cpu_current_action = choice
            
            # Execute current action
            if self.cpu_current_action == "move":
                # Move towards opponent
                if self.x < opponent.x:
                    self.x += self.speed
                    self.direction = "right"
                else:
                    self.x -= self.speed
                    self.direction = "left"
                    
                # Prevent moving off screen
                if self.x < self.width // 2:
                    self.x = self.width // 2
                if self.x > SCREEN_WIDTH - self.width // 2:
                    self.x = SCREEN_WIDTH - self.width // 2
                    
            elif self.cpu_current_action == "punch" and self.energy >= ENERGY_COST["punch"]:
                self.action = "punch"
                self.action_time = 0
                self.energy -= ENERGY_COST["punch"]
                self.combo_counter += 1
                self.combo_timer = 0
                self.cpu_current_action = None
                
            elif self.cpu_current_action == "kick" and self.energy >= ENERGY_COST["kick"]:
                self.action = "kick"
                self.action_time = 0
                self.energy -= ENERGY_COST["kick"]
                self.combo_counter += 1
                self.combo_timer = 0
                self.cpu_current_action = None

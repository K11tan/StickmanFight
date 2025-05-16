# stickman.py - Stickman drawing functions

import pygame
import math
import random
from constants import *

def draw_stickman(surface, x, y, width, height, color, action, direction, special=False):
    """
    Draw a stickman figure with different poses based on action
    
    Args:
        surface: pygame surface to draw on
        x, y: position of the stickman
        width, height: dimensions of the stickman
        color: RGB color tuple for the stickman
        action: string indicating the action ("idle", "punch", "kick", "block", "special")
        direction: string indicating the direction ("left" or "right")
        special: boolean indicating if special effects should be shown
    """
    # Scale factors
    head_radius = int(height * 0.15)
    torso_length = int(height * 0.3)
    arm_length = int(height * 0.25)
    leg_length = int(height * 0.4)
    
    # Head position
    head_x = x
    head_y = y + head_radius
    
    # Base positions
    shoulder_y = head_y + head_radius
    hip_y = shoulder_y + torso_length
    
    # Draw different poses based on action
    if action == "idle":
        # Head
        pygame.draw.circle(surface, color, (head_x, head_y), head_radius)
        
        # Torso
        pygame.draw.line(surface, color, (head_x, shoulder_y), (head_x, hip_y), 3)
        
        # Arms
        arm_angle = 20 if direction == "right" else 160
        r_arm_x = head_x + int(arm_length * math.cos(math.radians(arm_angle)))
        r_arm_y = shoulder_y + int(arm_length * math.sin(math.radians(arm_angle)))
        
        l_arm_angle = 160 if direction == "right" else 20
        l_arm_x = head_x + int(arm_length * math.cos(math.radians(l_arm_angle)))
        l_arm_y = shoulder_y + int(arm_length * math.sin(math.radians(l_arm_angle)))
        
        pygame.draw.line(surface, color, (head_x, shoulder_y), (r_arm_x, r_arm_y), 2)
        pygame.draw.line(surface, color, (head_x, shoulder_y), (l_arm_x, l_arm_y), 2)
        
        # Legs
        r_leg_x = head_x + int(leg_length * 0.5 * math.cos(math.radians(120)))
        r_leg_y = hip_y + int(leg_length * 0.5 * math.sin(math.radians(120)))
        
        l_leg_x = head_x + int(leg_length * 0.5 * math.cos(math.radians(60)))
        l_leg_y = hip_y + int(leg_length * 0.5 * math.sin(math.radians(60)))
        
        pygame.draw.line(surface, color, (head_x, hip_y), (r_leg_x, r_leg_y), 2)
        pygame.draw.line(surface, color, (head_x, hip_y), (l_leg_x, l_leg_y), 2)
    
    elif action == "punch":
        # Head
        pygame.draw.circle(surface, color, (head_x, head_y), head_radius)
        
        # Torso - leaning slightly
        torso_lean = 5 if direction == "right" else -5
        pygame.draw.line(surface, color, (head_x, shoulder_y), 
                         (head_x + torso_lean, hip_y), 3)
        
        # Arms - one extended for punch
        if direction == "right":
            # Back arm
            l_arm_angle = 190
            l_arm_x = head_x + int(arm_length * 0.8 * math.cos(math.radians(l_arm_angle)))
            l_arm_y = shoulder_y + int(arm_length * 0.8 * math.sin(math.radians(l_arm_angle)))
            pygame.draw.line(surface, color, (head_x, shoulder_y), (l_arm_x, l_arm_y), 2)
            
            # Punching arm - extended
            r_arm_angle = 0
            r_arm_length = arm_length * 1.3  # Extended for punch
            r_arm_x = head_x + int(r_arm_length * math.cos(math.radians(r_arm_angle)))
            r_arm_y = shoulder_y + int(r_arm_length * math.sin(math.radians(r_arm_angle)))
            pygame.draw.line(surface, color, (head_x, shoulder_y), (r_arm_x, r_arm_y), 3)
            
            # Draw fist
            pygame.draw.circle(surface, color, (r_arm_x, r_arm_y), 5)
            
            # Show punch effect
            if special:
                for i in range(3):
                    offset = random.randint(5, 15)
                    pygame.draw.circle(surface, YELLOW, 
                                      (r_arm_x + offset, r_arm_y + random.randint(-5, 5)), 
                                      random.randint(3, 8))
        else:  # Left direction
            # Back arm
            r_arm_angle = -10
            r_arm_x = head_x + int(arm_length * 0.8 * math.cos(math.radians(r_arm_angle)))
            r_arm_y = shoulder_y + int(arm_length * 0.8 * math.sin(math.radians(r_arm_angle)))
            pygame.draw.line(surface, color, (head_x, shoulder_y), (r_arm_x, r_arm_y), 2)
            
            # Punching arm - extended
            l_arm_angle = 180
            l_arm_length = arm_length * 1.3  # Extended for punch
            l_arm_x = head_x + int(l_arm_length * math.cos(math.radians(l_arm_angle)))
            l_arm_y = shoulder_y + int(l_arm_length * math.sin(math.radians(l_arm_angle)))
            pygame.draw.line(surface, color, (head_x, shoulder_y), (l_arm_x, l_arm_y), 3)
            
            # Draw fist
            pygame.draw.circle(surface, color, (l_arm_x, l_arm_y), 5)
            
            # Show punch effect
            if special:
                for i in range(3):
                    offset = random.randint(5, 15)
                    pygame.draw.circle(surface, YELLOW, 
                                      (l_arm_x - offset, l_arm_y + random.randint(-5, 5)), 
                                      random.randint(3, 8))
        
        # Legs - slightly bent for stability
        r_leg_x = head_x + int(leg_length * 0.5 * math.cos(math.radians(110)))
        r_leg_y = hip_y + int(leg_length * 0.5 * math.sin(math.radians(110)))
        
        l_leg_x = head_x + int(leg_length * 0.5 * math.cos(math.radians(70)))
        l_leg_y = hip_y + int(leg_length * 0.5 * math.sin(math.radians(70)))
        
        pygame.draw.line(surface, color, (head_x + torso_lean, hip_y), (r_leg_x, r_leg_y), 2)
        pygame.draw.line(surface, color, (head_x + torso_lean, hip_y), (l_leg_x, l_leg_y), 2)
    
    elif action == "kick":
        # Head
        pygame.draw.circle(surface, color, (head_x, head_y), head_radius)
        
        # Torso - leaning for kick
        torso_lean = 10 if direction == "right" else -10
        pygame.draw.line(surface, color, (head_x, shoulder_y), 
                         (head_x + torso_lean, hip_y), 3)
        
        # Arms - balancing
        if direction == "right":
            # Back arm
            l_arm_angle = 150
            l_arm_x = head_x + int(arm_length * math.cos(math.radians(l_arm_angle)))
            l_arm_y = shoulder_y + int(arm_length * math.sin(math.radians(l_arm_angle)))
            pygame.draw.line(surface, color, (head_x, shoulder_y), (l_arm_x, l_arm_y), 2)
            
            # Front arm
            r_arm_angle = 45
            r_arm_x = head_x + int(arm_length * math.cos(math.radians(r_arm_angle)))
            r_arm_y = shoulder_y + int(arm_length * math.sin(math.radians(r_arm_angle)))
            pygame.draw.line(surface, color, (head_x, shoulder_y), (r_arm_x, r_arm_y), 2)
            
            # Kicking leg - extended
            r_leg_angle = 0
            r_leg_length = leg_length * 1.3
            r_leg_x = head_x + torso_lean + int(r_leg_length * math.cos(math.radians(r_leg_angle)))
            r_leg_y = hip_y + int(r_leg_length * math.sin(math.radians(r_leg_angle)))
            pygame.draw.line(surface, color, (head_x + torso_lean, hip_y), (r_leg_x, r_leg_y), 3)
            
            # Standing leg - bent for balance
            l_leg_angle = 100
            l_leg_x = head_x + torso_lean + int(leg_length * 0.8 * math.cos(math.radians(l_leg_angle)))
            l_leg_y = hip_y + int(leg_length * 0.8 * math.sin(math.radians(l_leg_angle)))
            pygame.draw.line(surface, color, (head_x + torso_lean, hip_y), (l_leg_x, l_leg_y), 2)
            
            # Show kick effect
            if special:
                for i in range(3):
                    offset = random.randint(5, 15)
                    pygame.draw.circle(surface, ORANGE, 
                                      (r_leg_x + offset, r_leg_y + random.randint(-5, 5)), 
                                      random.randint(3, 8))
        else:  # Left direction
            # Back arm
            r_arm_angle = 30
            r_arm_x = head_x + int(arm_length * math.cos(math.radians(r_arm_angle)))
            r_arm_y = shoulder_y + int(arm_length * math.sin(math.radians(r_arm_angle)))
            pygame.draw.line(surface, color, (head_x, shoulder_y), (r_arm_x, r_arm_y), 2)
            
            # Front arm
            l_arm_angle = 135
            l_arm_x = head_x + int(arm_length * math.cos(math.radians(l_arm_angle)))
            l_arm_y = shoulder_y + int(arm_length * math.sin(math.radians(l_arm_angle)))
            pygame.draw.line(surface, color, (head_x, shoulder_y), (l_arm_x, l_arm_y), 2)
            
            # Kicking leg - extended
            l_leg_angle = 180
            l_leg_length = leg_length * 1.3
            l_leg_x = head_x + torso_lean + int(l_leg_length * math.cos(math.radians(l_leg_angle)))
            l_leg_y = hip_y + int(l_leg_length * math.sin(math.radians(l_leg_angle)))
            pygame.draw.line(surface, color, (head_x + torso_lean, hip_y), (l_leg_x, l_leg_y), 3)
            
            # Standing leg - bent for balance
            r_leg_angle = 80
            r_leg_x = head_x + torso_lean + int(leg_length * 0.8 * math.cos(math.radians(r_leg_angle)))
            r_leg_y = hip_y + int(leg_length * 0.8 * math.sin(math.radians(r_leg_angle)))
            pygame.draw.line(surface, color, (head_x + torso_lean, hip_y), (r_leg_x, r_leg_y), 2)
            
            # Show kick effect
            if special:
                for i in range(3):
                    offset = random.randint(5, 15)
                    pygame.draw.circle(surface, ORANGE, 
                                      (l_leg_x - offset, l_leg_y + random.randint(-5, 5)), 
                                      random.randint(3, 8))
    
    elif action == "block":
        # Head
        pygame.draw.circle(surface, color, (head_x, head_y), head_radius)
        
        # Torso - slightly crouched
        torso_shrink = 0.9
        pygame.draw.line(surface, color, (head_x, shoulder_y), 
                         (head_x, hip_y * torso_shrink), 3)
        
        # Arms - crossed for blocking
        if direction == "right":
            # Arm positions for right-facing block
            r_arm_angle1 = 45
            r_arm_x1 = head_x + int(arm_length * 0.6 * math.cos(math.radians(r_arm_angle1)))
            r_arm_y1 = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(r_arm_angle1)))
            
            r_arm_angle2 = 100
            r_arm_x2 = r_arm_x1 + int(arm_length * 0.6 * math.cos(math.radians(r_arm_angle2)))
            r_arm_y2 = r_arm_y1 + int(arm_length * 0.6 * math.sin(math.radians(r_arm_angle2)))
            
            l_arm_angle1 = 135
            l_arm_x1 = head_x + int(arm_length * 0.6 * math.cos(math.radians(l_arm_angle1)))
            l_arm_y1 = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(l_arm_angle1)))
            
            l_arm_angle2 = 80
            l_arm_x2 = l_arm_x1 + int(arm_length * 0.6 * math.cos(math.radians(l_arm_angle2)))
            l_arm_y2 = l_arm_y1 + int(arm_length * 0.6 * math.sin(math.radians(l_arm_angle2)))
            
        else:  # Left direction
            # Arm positions for left-facing block
            l_arm_angle1 = 135
            l_arm_x1 = head_x + int(arm_length * 0.6 * math.cos(math.radians(l_arm_angle1)))
            l_arm_y1 = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(l_arm_angle1)))
            
            l_arm_angle2 = 80
            l_arm_x2 = l_arm_x1 + int(arm_length * 0.6 * math.cos(math.radians(l_arm_angle2)))
            l_arm_y2 = l_arm_y1 + int(arm_length * 0.6 * math.sin(math.radians(l_arm_angle2)))
            
            r_arm_angle1 = 45
            r_arm_x1 = head_x + int(arm_length * 0.6 * math.cos(math.radians(r_arm_angle1)))
            r_arm_y1 = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(r_arm_angle1)))
            
            r_arm_angle2 = 100
            r_arm_x2 = r_arm_x1 + int(arm_length * 0.6 * math.cos(math.radians(r_arm_angle2)))
            r_arm_y2 = r_arm_y1 + int(arm_length * 0.6 * math.sin(math.radians(r_arm_angle2)))
        
        # Draw arms with thicker lines for blocking
        pygame.draw.line(surface, color, (head_x, shoulder_y), (r_arm_x1, r_arm_y1), 2)
        pygame.draw.line(surface, color, (r_arm_x1, r_arm_y1), (r_arm_x2, r_arm_y2), 3)
        
        pygame.draw.line(surface, color, (head_x, shoulder_y), (l_arm_x1, l_arm_y1), 2)
        pygame.draw.line(surface, color, (l_arm_x1, l_arm_y1), (l_arm_x2, l_arm_y2), 3)
        
        # Show block effect
        if special:
            shield_x = head_x + (30 if direction == "right" else -30)
            pygame.draw.arc(surface, BLUE, 
                           (shield_x - 30, shoulder_y - 30, 60, 80),
                           math.radians(60), math.radians(300), 3)
        
        # Legs - slightly bent
        hip_y = hip_y * torso_shrink
        r_leg_x = head_x + int(leg_length * 0.5 * math.cos(math.radians(110)))
        r_leg_y = hip_y + int(leg_length * 0.5 * math.sin(math.radians(110)))
        
        l_leg_x = head_x + int(leg_length * 0.5 * math.cos(math.radians(70)))
        l_leg_y = hip_y + int(leg_length * 0.5 * math.sin(math.radians(70)))
        
        pygame.draw.line(surface, color, (head_x, hip_y), (r_leg_x, r_leg_y), 2)
        pygame.draw.line(surface, color, (head_x, hip_y), (l_leg_x, l_leg_y), 2)
    
    elif action == "special":
        # A dramatic special move pose
        # Head
        pygame.draw.circle(surface, color, (head_x, head_y), head_radius)
        
        # Draw flame-like effects around the stickman
        if special:
            for i in range(15):
                flame_x = head_x + random.randint(-30, 30)
                flame_y = head_y + random.randint(-40, 40)
                flame_size = random.randint(5, 15)
                
                # Create a gradient of colors for the flame effect
                color_value = random.randint(0, 2)
                if color_value == 0:
                    flame_color = RED
                elif color_value == 1:
                    flame_color = ORANGE
                else:
                    flame_color = YELLOW
                
                pygame.draw.circle(surface, flame_color, (flame_x, flame_y), flame_size)
        
        # Torso - slightly leaning back
        torso_lean = -5 if direction == "right" else 5
        pygame.draw.line(surface, color, (head_x, shoulder_y), 
                        (head_x + torso_lean, hip_y), 3)
        
        # Arms - both raised up in a power pose
        if direction == "right":
            r_arm_angle1 = 30
            r_arm_x1 = head_x + int(arm_length * 0.6 * math.cos(math.radians(r_arm_angle1)))
            r_arm_y1 = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(r_arm_angle1)))
            
            r_arm_angle2 = -30
            r_arm_x2 = r_arm_x1 + int(arm_length * 0.6 * math.cos(math.radians(r_arm_angle2)))
            r_arm_y2 = r_arm_y1 + int(arm_length * 0.6 * math.sin(math.radians(r_arm_angle2)))
            
            l_arm_angle1 = 150
            l_arm_x1 = head_x + int(arm_length * 0.6 * math.cos(math.radians(l_arm_angle1)))
            l_arm_y1 = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(l_arm_angle1)))
            
            l_arm_angle2 = 210
            l_arm_x2 = l_arm_x1 + int(arm_length * 0.6 * math.cos(math.radians(l_arm_angle2)))
            l_arm_y2 = l_arm_y1 + int(arm_length * 0.6 * math.sin(math.radians(l_arm_angle2)))
        else:
            l_arm_angle1 = 150
            l_arm_x1 = head_x + int(arm_length * 0.6 * math.cos(math.radians(l_arm_angle1)))
            l_arm_y1 = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(l_arm_angle1)))
            
            l_arm_angle2 = 210
            l_arm_x2 = l_arm_x1 + int(arm_length * 0.6 * math.cos(math.radians(l_arm_angle2)))
            l_arm_y2 = l_arm_y1 + int(arm_length * 0.6 * math.sin(math.radians(l_arm_angle2)))
            
            r_arm_angle1 = 30
            r_arm_x1 = head_x + int(arm_length * 0.6 * math.cos(math.radians(r_arm_angle1)))
            r_arm_y1 = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(r_arm_angle1)))
            
            r_arm_angle2 = -30
            r_arm_x2 = r_arm_x1 + int(arm_length * 0.6 * math.cos(math.radians(r_arm_angle2)))
            r_arm_y2 = r_arm_y1 + int(arm_length * 0.6 * math.sin(math.radians(r_arm_angle2)))
        
        # Draw arms
        pygame.draw.line(surface, color, (head_x, shoulder_y), (r_arm_x1, r_arm_y1), 2)
        pygame.draw.line(surface, color, (r_arm_x1, r_arm_y1), (r_arm_x2, r_arm_y2), 2)
        
        pygame.draw.line(surface, color, (head_x, shoulder_y), (l_arm_x1, l_arm_y1), 2)
        pygame.draw.line(surface, color, (l_arm_x1, l_arm_y1), (l_arm_x2, l_arm_y2), 2)
        
        # Legs - in an action stance
        r_leg_x = head_x + torso_lean + int(leg_length * 0.5 * math.cos(math.radians(120)))
        r_leg_y = hip_y + int(leg_length * 0.5 * math.sin(math.radians(120)))
        
        l_leg_x = head_x + torso_lean + int(leg_length * 0.5 * math.cos(math.radians(60)))
        l_leg_y = hip_y + int(leg_length * 0.5 * math.sin(math.radians(60)))
        
        pygame.draw.line(surface, color, (head_x + torso_lean, hip_y), (r_leg_x, r_leg_y), 2)
        pygame.draw.line(surface, color, (head_x + torso_lean, hip_y), (l_leg_x, l_leg_y), 2)
    
    # Draw eyes in the head
    eye_offset = 3
    left_eye_x = head_x - head_radius // 3
    right_eye_x = head_x + head_radius // 3
    eyes_y = head_y - head_radius // 5
    
    # Swap eyes based on direction
    if direction == "left":
        left_eye_x, right_eye_x = right_eye_x, left_eye_x
    
    # Draw eyes
    pygame.draw.circle(surface, BLACK, (left_eye_x, eyes_y), 2)
    pygame.draw.circle(surface, BLACK, (right_eye_x, eyes_y), 2)
    
    # Draw mouth
    mouth_y = head_y + head_radius // 3
    mouth_width = head_radius // 2
    
    if special:
        # Open mouth for special move
        pygame.draw.ellipse(surface, BLACK, 
                           (head_x - mouth_width // 2, mouth_y - 2, 
                            mouth_width, mouth_width // 2))
    else:
        # Normal mouth
        pygame.draw.line(surface, BLACK, 
                        (head_x - mouth_width // 2, mouth_y),
                        (head_x + mouth_width // 2, mouth_y), 1)

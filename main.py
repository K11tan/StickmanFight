# main.py - Main game file

import pygame
import sys
import random
import math
from pygame.locals import *

# Import game modules
from constants import *
from stickman import draw_stickman
from fighter import Fighter
from effects import ParticleEffect
from ui import draw_ui, draw_menu, draw_game_over, draw_mode_select

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stick Fighter")
clock = pygame.time.Clock()

# Initialize sounds
pygame.mixer.init()
try:
    hit_sound = pygame.mixer.Sound("hit.wav")
    block_sound = pygame.mixer.Sound("block.wav")
    special_sound = pygame.mixer.Sound("special.wav")
except:
    # Create placeholder sounds if files not found
    hit_sound = None
    block_sound = None
    special_sound = None

class Game:
    def __init__(self):
        self.running = True
        self.game_over = False
        self.winner = None
        self.game_state = "menu"  # "menu", "playing", "paused", "game_over", "mode_select"
        self.game_mode = "solo"  # "solo" or "versus"
        
        # Particle effects
        self.particles = []
        
        # Define player controls
        player1_controls = {
            "left": K_a,
            "right": K_d,
            "punch": K_r,
            "kick": K_t,
            "block": K_y,
            "special": K_f
        }
        
        player2_controls = {
            "left": K_LEFT,
            "right": K_RIGHT,
            "punch": K_COMMA,
            "kick": K_PERIOD,
            "block": K_m,
            "special": K_SLASH
        }
        
        # Create the fighters with correct control mode based on game mode
        self.player1 = Fighter(200, SCREEN_HEIGHT - 100, 60, 120, BLUE, player1_controls, True)
        self.player2 = Fighter(600, SCREEN_HEIGHT - 100, 60, 120, RED, player2_controls, self.game_mode == "versus")
        
        # Background elements
        self.create_background()
        
        # Font for text
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
    
    def create_background(self):
        # Create background elements (clouds, mountains, etc.)
        self.clouds = []
        for i in range(5):
            cloud = {
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(50, 150),
                "width": random.randint(60, 120),
                "height": random.randint(30, 50),
                "speed": random.uniform(0.2, 0.5)
            }
            self.clouds.append(cloud)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        self.game_state = "playing"
                    elif self.game_state == "menu" or self.game_state == "game_over":
                        self.running = False
                
                # Handle menu actions
                if self.game_state == "menu":
                    if event.key == pygame.K_RETURN:
                        self.game_state = "mode_select"
                
                # Handle mode selection
                elif self.game_state == "mode_select":
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        # Solo mode against CPU
                        self.game_mode = "solo"
                        self.reset_game()
                        self.game_state = "playing"
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        # Versus mode (2 players)
                        self.game_mode = "versus"
                        self.reset_game()
                        self.game_state = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                
                # Handle game over actions
                elif self.game_state == "game_over":
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.game_state = "playing"
                    elif event.key == pygame.K_m:
                        self.game_state = "menu"
                
                # Handle pause actions
                elif self.game_state == "paused":
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.game_state = "playing"
                    elif event.key == pygame.K_m:
                        self.game_state = "menu"
    
    def update(self):
        if self.game_state != "playing":
            return
            
        # Update players
        self.player1.update(self.player2)
        self.player2.update(self.player1)
        
        # Update cloud positions
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > SCREEN_WIDTH + 100:
                cloud["x"] = -cloud["width"]
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if not particle.active:
                self.particles.remove(particle)
        
        # Check for game over condition
        if self.player1.health <= 0 or self.player2.health <= 0:
            self.game_over = True
            self.game_state = "game_over"
            if self.player1.health <= 0:
                self.winner = "Player 2"
            else:
                self.winner = "Player 1"
    
    def draw(self):
        # Draw the background
        screen.fill(SKY_BLUE)
        
        # Draw mountains (static)
        for i in range(3):
            x1 = i * 300 - 100
            x2 = x1 + 150
            x3 = x1 + 300
            pygame.draw.polygon(screen, (100, 100, 100), [(x1, SCREEN_HEIGHT), (x2, 300), (x3, SCREEN_HEIGHT)])
        
        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.ellipse(screen, WHITE, (cloud["x"], cloud["y"], cloud["width"], cloud["height"]))
        
        # Draw ground
        pygame.draw.rect(screen, (139, 69, 19), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.line(screen, (100, 50, 0), (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 3)
        
        # Draw game elements based on game state
        if self.game_state == "menu":
            draw_menu(screen, self.big_font, self.font)
        
        elif self.game_state == "mode_select":
            draw_mode_select(screen, self.big_font, self.font)
        
        elif self.game_state == "playing" or self.game_state == "paused":
            # Display current mode
            mode_text = self.font.render(f"MODE: {'SOLO' if self.game_mode == 'solo' else 'VERSUS'}", True, WHITE)
            screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 10))
            
            # Draw fighters
            draw_stickman(screen, self.player1.x, self.player1.y, self.player1.width, self.player1.height, 
                       self.player1.color, self.player1.action, self.player1.direction, self.player1.special_active)
            
            draw_stickman(screen, self.player2.x, self.player2.y, self.player2.width, self.player2.height, 
                       self.player2.color, self.player2.action, self.player2.direction, self.player2.special_active)
            
            # Draw UI elements
            draw_ui(screen, self.player1, self.player2, self.font)
            
            # Draw particles
            for particle in self.particles:
                particle.draw(screen)
            
            # Draw pause overlay
            if self.game_state == "paused":
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                
                pause_text = self.big_font.render("PAUSED", True, WHITE)
                resume_text = self.font.render("Press ESC to resume", True, WHITE)
                restart_text = self.font.render("Press R to restart", True, WHITE)
                menu_text = self.font.render("Press M for menu", True, WHITE)
                
                screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 3))
                screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2))
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
                screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
        
        elif self.game_state == "game_over":
            # Display current mode
            mode_text = self.font.render(f"MODE: {'SOLO' if self.game_mode == 'solo' else 'VERSUS'}", True, WHITE)
            screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 10))
            
            # Draw final positions of fighters
            draw_stickman(screen, self.player1.x, self.player1.y, self.player1.width, self.player1.height, 
                       self.player1.color, self.player1.action, self.player1.direction, False)
            
            draw_stickman(screen, self.player2.x, self.player2.y, self.player2.width, self.player2.height, 
                       self.player2.color, self.player2.action, self.player2.direction, False)
            
            # Draw game over screen
            draw_game_over(screen, self.winner, self.big_font, self.font)
        
        pygame.display.flip()
    
    def reset_game(self):
        # Determine if player 2 is CPU based on game mode
        is_player2_human = self.game_mode == "versus"
        
        # Reset fighter positions and stats
        self.player1.x = 200
        self.player1.health = 100
        self.player1.energy = 100
        self.player1.special_meter = 0
        self.player1.special_ready = False
        self.player1.action = "idle"
        
        self.player2.x = 600
        self.player2.health = 100
        self.player2.energy = 100
        self.player2.special_meter = 0
        self.player2.special_ready = False
        self.player2.action = "idle"
        self.player2.is_player = is_player2_human
        
        # Reset game state
        self.game_over = False
        self.winner = None
        self.particles = []
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

# Run the game if this is the main file
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
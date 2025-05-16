# ui.py - UI drawing functions for the game

import pygame
from constants import *

def draw_health_bar(surface, x, y, width, height, value, max_value, border_color, fill_color, bg_color):
    """
    Draw a health/energy bar
    
    Args:
        surface: Surface to draw on
        x, y: Position of the bar
        width, height: Dimensions of the bar
        value: Current value
        max_value: Maximum value
        border_color: Color of the border
        fill_color: Color of the fill
        bg_color: Background color
    """
    # Draw background
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    
    # Draw fill
    fill_width = int(width * (value / max_value))
    if fill_width > 0:
        pygame.draw.rect(surface, fill_color, (x, y, fill_width, height))
    
    # Draw border
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2)

def draw_special_meter(surface, x, y, width, height, value, max_value):
    """Draw special meter with flashing effect when full"""
    # Draw background
    pygame.draw.rect(surface, GRAY, (x, y, width, height))
    
    # Draw fill
    fill_width = int(width * (value / max_value))
    if fill_width > 0:
        # Check if meter is full for flashing effect
        if value >= max_value:
            # Use pulsing color based on ticks
            ticks = pygame.time.get_ticks() // 100
            if ticks % 2 == 0:
                fill_color = YELLOW
            else:
                fill_color = ORANGE
        else:
            fill_color = PURPLE
            
        pygame.draw.rect(surface, fill_color, (x, y, fill_width, height))
    
    # Draw border
    pygame.draw.rect(surface, BLACK, (x, y, width, height), 2)

def draw_combo_indicator(surface, x, y, combo_count, font):
    """Draw combo counter if combo > 1"""
    if combo_count > 1:
        combo_text = font.render(f"{combo_count}x COMBO", True, YELLOW)
        surface.blit(combo_text, (x, y))

def draw_ui(surface, player1, player2, font):
    """Draw all UI elements for the game"""
    # Draw player 1 UI (left side)
    draw_health_bar(surface, 20, 20, 200, 20, player1.health, 100, WHITE, GREEN, RED)
    draw_health_bar(surface, 20, 50, 150, 10, player1.energy, 100, WHITE, BLUE, GRAY)
    draw_special_meter(surface, 20, 70, 150, 10, player1.special_meter, player1.special_threshold)
    
    # Draw player 1 name and combo
    p1_name = font.render("PLAYER 1", True, player1.color)
    surface.blit(p1_name, (20, 90))
    draw_combo_indicator(surface, 20, 120, player1.combo_counter, font)
    
    # Draw player 2 UI (right side)
    draw_health_bar(surface, SCREEN_WIDTH - 220, 20, 200, 20, player2.health, 100, WHITE, GREEN, RED)
    draw_health_bar(surface, SCREEN_WIDTH - 170, 50, 150, 10, player2.energy, 100, WHITE, BLUE, GRAY)
    draw_special_meter(surface, SCREEN_WIDTH - 170, 70, 150, 10, player2.special_meter, player2.special_threshold)
    
    # Draw player 2 name and combo
    p2_name = font.render("PLAYER 2", True, player2.color)
    text_width = p2_name.get_width()
    surface.blit(p2_name, (SCREEN_WIDTH - 20 - text_width, 90))
    
    combo_text = font.render(f"{player2.combo_counter}x COMBO", True, YELLOW)
    text_width = combo_text.get_width()
    if player2.combo_counter > 1:
        surface.blit(combo_text, (SCREEN_WIDTH - 20 - text_width, 120))

def draw_menu(surface, big_font, font):
    """Draw the main menu"""
    # Draw title
    title_text = big_font.render("STICK FIGHTER", True, WHITE)
    subtitle_text = font.render("2D Fighting Game", True, YELLOW)
    
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    surface.blit(subtitle_text, 
               (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 
                SCREEN_HEIGHT // 4 + title_text.get_height() + 10))
    
    # Draw instructions
    instruction_text = font.render("Press ENTER to start", True, WHITE)
    surface.blit(instruction_text, 
               (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 
                SCREEN_HEIGHT // 2))
    
    # Credits
    credits_text = font.render("Created with PyGame", True, GRAY)
    surface.blit(credits_text, 
               (SCREEN_WIDTH // 2 - credits_text.get_width() // 2, 
                SCREEN_HEIGHT - 50))

def draw_mode_select(surface, big_font, font):
    """Draw the game mode selection screen"""
    # Draw title
    title_text = big_font.render("SELECT MODE", True, WHITE)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    
    # Draw mode options
    options = [
        "1. SOLO MODE - Play against CPU",
        "2. VERSUS MODE - 2 Player Battle"
    ]
    
    y_offset = SCREEN_HEIGHT // 2
    for option in options:
        option_text = font.render(option, True, YELLOW)
        surface.blit(option_text, 
                   (SCREEN_WIDTH // 2 - option_text.get_width() // 2, y_offset))
        y_offset += 50
    
    # Draw controls info
    controls_p1 = [
        "Player 1 Controls:",
        "A/D - Move Left/Right",
        "R - Punch",
        "T - Kick",
        "Y - Block",
        "F - Special Move"
    ]
    
    controls_p2 = [
        "Player 2 Controls:",
        "←/→ - Move Left/Right",
        "Num 1 - Punch",
        "Num 2 - Kick",
        "Num 3 - Block",
        "Num 0 - Special Move"
    ]
    
    # Draw P1 controls
    y_offset = SCREEN_HEIGHT * 2 // 3 + 20
    for line in controls_p1:
        text = font.render(line, True, BLUE)
        surface.blit(text, (SCREEN_WIDTH // 4 - text.get_width() // 2, y_offset))
        y_offset += 30
    
    # Draw P2 controls
    y_offset = SCREEN_HEIGHT * 2 // 3 + 20
    for line in controls_p2:
        text = font.render(line, True, RED)
        surface.blit(text, (SCREEN_WIDTH * 3 // 4 - text.get_width() // 2, y_offset))
        y_offset += 30
    
    # Back instruction
    back_text = font.render("Press ESC to go back", True, WHITE)
    surface.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 50))

def draw_game_over(surface, winner, big_font, font):
    """Draw the game over screen"""
    # Darkened overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))
    
    # Draw game over text
    game_over_text = big_font.render("GAME OVER", True, WHITE)
    surface.blit(game_over_text, 
               (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                SCREEN_HEIGHT // 3))
    
    # Draw winner
    color = BLUE if winner == "Player 1" else RED
    winner_text = big_font.render(f"{winner} WINS!", True, color)
    surface.blit(winner_text, 
               (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, 
                SCREEN_HEIGHT // 2))
    
    # Draw instructions
    instructions = [
        "Press ENTER to play again",
        "Press M for main menu",
        "Press ESC to quit"
    ]
    
    y_offset = SCREEN_HEIGHT * 2 // 3
    for line in instructions:
        text = font.render(line, True, WHITE)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40
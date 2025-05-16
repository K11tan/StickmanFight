# constants.py - Game constants and settings

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (150, 150, 150)
PURPLE = (128, 0, 128)
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)

# Game settings
GRAVITY = 0.5
DAMAGE = {
    "punch": 5,
    "kick": 8,
    "special": 20
}

ENERGY_COST = {
    "punch": 10,
    "kick": 15,
    "block": 5,
    "special": 50
}

# Fighter stats
FIGHTER_WIDTH = 60
FIGHTER_HEIGHT = 120
FIGHTER_SPEED = 5
SPECIAL_THRESHOLD = 100

# Combat settings
BLOCK_DAMAGE_REDUCTION = 0.25  # Block reduces damage by 75%
COMBO_TIMEOUT = 60  # Frames before combo resets
COMBO_BONUS = 0.2   # 20% damage bonus per combo hit

# Sound settings
SOUND_VOLUME = 0.5

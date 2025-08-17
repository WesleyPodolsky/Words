"""All the game settings are defined here."""

# Screen dimensions
WIDTH = 1200
HEIGHT = 750

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)

# Landing Pads
NUMBER_OF_PADS = 3

# Obstacles
MIN_OBSTACLES = 5
MAX_OBSTACLES = 15

# Meteors
MIN_METEORS = 5
MAX_METEORS = 10

# Physics
GRAVITY = 0.1 / 30
AIR_RESISTANCE = 0.02 / 30

# Lander
LANDER_LIVES_START = 3
THRUST_COST = 5
START_FUEL = 500
SAFE_LANDING_SPEED = 1.0
# number of ticks for which the lander is immune to damage from collisions
NO_COLLISION_DURATION = 60
# Chance of a failure in every frame e.g. if set to 0.001 lander should fail once every 1000 frames (game runs @ 30fps)
FAILURE_CHANCE = 0.001
FAILURE_DURATION = 60  # frames

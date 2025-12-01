# settings.py

# --- Display Settings ---
WIDTH = 1080
HEIGHT = 720
FPS = 60

# --- Player Settings ---
PLAYER_SPEED = 200  # Adjust for feel — 200 = smooth glide, 300 = fast arcade

# --- Colors ---
BLACK = (0, 0, 0)
DARK_BLUE = (10, 10, 25)
CYAN = (0, 255, 200)
LIGHT_BLUE = (0, 180, 255)
# settings.py - placeholder


LEVEL_COLORS = [
    (133, 218, 235),
    (95, 201, 231),
    (95, 161, 231),
    (95, 110, 231),
    (76, 96, 170),
    (68, 71, 116),
    (50, 49, 59),
    (70, 60, 94),
    (93, 71, 118),
    (133, 83, 149),
    (171, 88, 168),
    (202, 96, 174),
    (243, 167, 135),
    (245, 218, 167),
    (141, 216, 148),
    (93, 193, 144),
    (74, 185, 163),
    (69, 147, 165),
    (94, 253, 247),
    (255, 93, 204),
    (253, 254, 137),
    (255, 255, 255),
]

CURRENT_LEVEL = 0
MAX_LEVELS = len(LEVEL_COLORS)

def get_level_color(index=None):
    if index is None:
        index = CURRENT_LEVEL
    return LEVEL_COLORS[index % MAX_LEVELS]
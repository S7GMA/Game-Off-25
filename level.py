from settings import LEVEL_COLORS

class Level:
    """Handles level progression, difficulty scaling, and color themes."""

    def __init__(self):
        self.index = 0
        self.max_levels = len(LEVEL_COLORS)
        self.duration = 30  # seconds per level
        self.spawn_rate = 2.0

    def next_level(self):
        """Advance to the next level and scale difficulty."""
        self.index = (self.index + 1) % self.max_levels
        self.spawn_rate = max(0.5, 2.0 - self.index * 0.2)

    def reset(self):
        """Reset progression for a new run."""
        self.index = 0
        self.spawn_rate = 2.0

    def get_color(self):
        """Return current level's color tint."""
        return LEVEL_COLORS[self.index]

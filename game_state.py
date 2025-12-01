class GameState:
    def __init__(self):
        # valid states:
        # "menu", "countdown", "game", "pause", "game_over"
        self.state = "menu"

    def set(self, new_state):
        self.state = new_state

    def is_state(self, name):
        return self.state == name

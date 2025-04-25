

class GameState():
    def __init__(self):
        self.current_screen = 'game' # menu game_over upgrades
        self.reset()

    def reset(self):
        self.score = 0
        self.player_health = 100
        
    def save_last_game_score(self):
        self.last_game_score = self.score


game_state = GameState()
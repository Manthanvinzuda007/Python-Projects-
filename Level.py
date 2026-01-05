class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.max_levels = 15

    def get_current_config(self):
        # Dynamically scale difficulty
        size = 4 if self.current_level < 4 else (5 if self.current_level < 8 else 6)
        moves = 10 - (self.current_level // 3)
        if moves < 5: moves = 5
        
        return {
            "size": size,
            "moves": moves,
            "difficulty": self.current_level
        }

    def next_level(self):
        if self.current_level < self.max_levels:
            self.current_level += 1
            return True
        return False

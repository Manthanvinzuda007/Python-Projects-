import random
import time

class GameEngine:
    def __init__(self, level_manager):
        self.level_manager = level_manager
        self.focus_level = 100.0
        self.is_focused = True
        self.reset_for_next_level()

    def reset_for_next_level(self):
        config = self.level_manager.get_current_config()
        self.grid_size = config['size']
        self.moves_left = config['moves']
        self.grid = self._generate_grid()
        self.target_sum = self._calculate_valid_target()
        self.current_sum = 0
        self.path = []
        self.start_time = time.time()

    def reset_current_level(self):
        self.moves_left = self.level_manager.get_current_config()['moves']
        self.current_sum = 0
        self.path = []

    def _generate_grid(self):
        return [[random.randint(1, 9) for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def _calculate_valid_target(self):
        # Ensure there is at least one valid path of reasonable length
        path_len = random.randint(3, self.grid_size + 1)
        r, c = 0, 0
        target = self.grid[r][c]
        visited = {(0,0)}
        
        for _ in range(path_len - 1):
            adj = []
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and (nr, nc) not in visited:
                    adj.append((nr, nc))
            if not adj: break
            r, c = random.choice(adj)
            target += self.grid[r][c]
            visited.add((r, c))
        return target

    def process_move(self, r, c):
        if (r, c) in self.path:
            return "ALREADY_VISITED"
        
        # Check adjacency if path started
        if self.path:
            pr, pc = self.path[-1]
            if abs(pr - r) + abs(pc - c) != 1:
                return "INVALID_MOVE"

        self.path.append((r, c))
        self.current_sum += self.grid[r][c]
        self.moves_left -= 1

        if self.current_sum == self.target_sum:
            return "WIN"
        if self.moves_left <= 0 or self.current_sum > self.target_sum:
            return "LOSE"
        
        return "CONTINUE"

    def get_grid(self): return self.grid
    def get_path(self): return self.path

    def handle_focus_loss(self):
        self.is_focused = False

    def handle_focus_gain(self):
        self.is_focused = True

    def tick(self):
        # Focus drains faster if window is inactive
        drain_rate = 0.5 if self.is_focused else 3.0
        # Difficulty multiplier
        multiplier = 1 + (self.level_manager.current_level * 0.1)
        self.focus_level -= (drain_rate * multiplier * 0.1)
        if self.focus_level > 100: self.focus_level = 100

    def calculate_round_score(self):
        base = 100 * self.level_manager.current_level
        time_bonus = max(0, 500 - int(time.time() - self.start_time))
        focus_bonus = int(self.focus_level * 2)
        return base + time_bonus + focus_bonus

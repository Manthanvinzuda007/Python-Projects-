import json
import os

class ScoreSystem:
    def __init__(self):
        self.total_score = 0
        self.high_score = 0
        self.file_path = "scores.json"
        self.load_high_score()

    def add_points(self, points):
        self.total_score += points
        if self.total_score > self.high_score:
            self.high_score = self.total_score
            self.save_high_score()

    def penalty(self, points):
        self.total_score = max(0, self.total_score - points)

    def load_high_score(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
            except:
                self.high_score = 0

    def save_high_score(self):
        with open(self.file_path, "w") as f:
            json.dump({"high_score": self.high_score}, f)

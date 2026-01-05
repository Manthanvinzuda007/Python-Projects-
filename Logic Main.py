import tkinter as tk
from tkinter import messagebox
import json
import time
from game_logic import GameEngine
from levels import LevelManager
from score import ScoreSystem

class MindStrikeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MindStrike – Logic & Focus")
        self.root.geometry("900x700")
        self.root.configure(bg="#121212")

        # Initialize Components
        self.score_system = ScoreSystem()
        self.level_manager = LevelManager()
        self.engine = GameEngine(self.level_manager)
        
        self.setup_ui()
        self.bind_events()
        self.start_game()

    def setup_ui(self):
        # Header Section
        self.header = tk.Frame(self.root, bg="#1a1a1a", pady=10)
        self.header.pack(fill="x")

        self.lvl_label = tk.Label(self.header, text="LEVEL: 1", fg="#00ffcc", bg="#1a1a1a", font=("Courier", 16, "bold"))
        self.lvl_label.pack(side="left", padx=20)

        self.score_label = tk.Label(self.header, text="SCORE: 0", fg="#ffffff", bg="#1a1a1a", font=("Courier", 16))
        self.score_label.pack(side="right", padx=20)

        # Game Info Panel
        self.info_panel = tk.Frame(self.root, bg="#121212", pady=20)
        self.info_panel.pack(fill="x")

        self.target_label = tk.Label(self.info_panel, text="TARGET: 0", fg="#ff3366", bg="#121212", font=("Courier", 24, "bold"))
        self.target_label.pack()

        self.status_label = tk.Label(self.info_panel, text="Current Sum: 0 | Moves: 0", fg="#aaaaaa", bg="#121212", font=("Courier", 12))
        self.status_label.pack()

        # Grid Container
        self.grid_frame = tk.Frame(self.root, bg="#333333", pading=2)
        self.grid_frame.pack(expand=True)

        # Focus Meter
        self.focus_frame = tk.Frame(self.root, bg="#121212", pady=10)
        self.focus_frame.pack(fill="x")
        self.focus_label = tk.Label(self.focus_frame, text="FOCUS METER", fg="#555555", bg="#121212", font=("Courier", 10))
        self.focus_label.pack()
        self.focus_bar = tk.Canvas(self.focus_frame, width=400, height=10, bg="#222", highlightthickness=0)
        self.focus_bar.pack()
        self.focus_rect = self.focus_bar.create_rectangle(0, 0, 400, 10, fill="#00ffcc")

    def bind_events(self):
        self.root.bind("<FocusOut>", lambda e: self.engine.handle_focus_loss())
        self.root.bind("<FocusIn>", lambda e: self.engine.handle_focus_gain())

    def start_game(self):
        self.update_grid()
        self.game_loop()

    def update_grid(self):
        # Clear current grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        grid_data = self.engine.get_grid()
        self.buttons = []
        
        for r in range(len(grid_data)):
            row_btns = []
            for c in range(len(grid_data[0])):
                val = grid_data[r][c]
                btn = tk.Button(
                    self.grid_frame, 
                    text=str(val), 
                    width=5, 
                    height=2, 
                    font=("Courier", 14, "bold"),
                    bg="#2a2a2a",
                    fg="#ffffff",
                    activebackground="#444444",
                    command=lambda r=r, c=c: self.make_move(r, c)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_btns.append(btn)
            self.buttons.append(row_btns)
        
        self.refresh_ui_labels()

    def make_move(self, r, c):
        result = self.engine.process_move(r, c)
        if result == "WIN":
            self.score_system.add_points(self.engine.calculate_round_score())
            if self.level_manager.next_level():
                messagebox.showinfo("Success", "Logic Level Cleared!")
                self.engine.reset_for_next_level()
                self.update_grid()
            else:
                messagebox.showinfo("MindStrike Master", "You have conquered all levels!")
                self.root.quit()
        elif result == "LOSE":
            messagebox.showerror("Failed", "Logic Error: Out of moves or invalid path.")
            self.engine.reset_current_level()
            self.update_grid()
        
        self.refresh_ui_labels()
        self.highlight_path()

    def highlight_path(self):
        path = self.engine.get_path()
        for r, c in path:
            self.buttons[r][c].config(bg="#00ffcc", fg="#000000")

    def refresh_ui_labels(self):
        self.lvl_label.config(text=f"LEVEL: {self.level_manager.current_level}")
        self.score_label.config(text=f"SCORE: {self.score_system.total_score}")
        self.target_label.config(text=f"TARGET: {self.engine.target_sum}")
        self.status_label.config(text=f"Current Sum: {self.engine.current_sum} | Moves Left: {self.engine.moves_left}")

    def game_loop(self):
        # Update Focus Bar
        focus_pct = self.engine.focus_level / 100
        self.focus_bar.coords(self.focus_rect, 0, 0, 400 * focus_pct, 10)
        
        # Color shift for focus
        if focus_pct < 0.3: color = "#ff3366"
        elif focus_pct < 0.6: color = "#ffcc00"
        else: color = "#00ffcc"
        self.focus_bar.itemconfig(self.focus_rect, fill=color)

        if self.engine.focus_level <= 0:
            messagebox.showwarning("DISTRACTED", "Focus Lost. Penalty Applied.")
            self.engine.focus_level = 50
            self.score_system.penalty(50)
            self.refresh_ui_labels()

        self.engine.tick()
        self.root.after(100, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = MindStrikeApp(root)
    root.mainloop()```

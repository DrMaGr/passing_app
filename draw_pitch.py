import tkinter as tk, asyncio
from player_icons import PlayerIconManager
from player_config import BALL_RADIUS, BALL_COLOR, BALL_START_POSITION
from game_ui import GameUI  # Import UI for button
from passing_lines import PassingLines  # Import passing lines

class HockeyPitch:
    def __init__(self, root):
        """
        Initializes the Hockey Pitch UI with a canvas, players, and the ball.
        """
        root.title("Hockey Pitch")
        root.geometry("1920x1080")
        root.resizable(False, False)

        # Create the canvas (pitch)
        self.canvas = tk.Canvas(root, bg="green", width=1720, height=1080)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ✅ Draw the pitch first
        self.draw_pitch()

        # ✅ Create players (so they appear below the ball)
        self.players = PlayerIconManager(self.canvas)

        # ✅ Create passing lines for Essendon players (excluding GK)
        self.passing_lines = PassingLines(self.canvas, self.players)  # ❌ Removed attach_to_players()

        # ✅ Draw the ball last (on top of everything)
        self.draw_ball()
        self.make_ball_draggable()

        # ✅ Initialize the UI after everything is set up
        self.ui = GameUI(root, self)

    def draw_pitch(self):
        """ Draws the hockey pitch with field markings. """
        self.canvas.delete("all")  # Clear the canvas

        # Pitch dimensions
        pitch_length = 914  # in pixels (91.4m)
        pitch_width = 550   # in pixels (55m)
        margin_top = 50     # Space around the pitch
        center_x = 860      # Centered horizontally in 1920px window

        # ✅ Draw pitch outline
        self.canvas.create_rectangle(
            center_x - pitch_width // 2, margin_top,
            center_x + pitch_width // 2, margin_top + pitch_length,
            outline="white", width=2
        )

        # ✅ Draw the center line
        self.canvas.create_line(
            center_x - pitch_width // 2, margin_top + pitch_length / 2,
            center_x + pitch_width // 2, margin_top + pitch_length / 2,
            fill="white", width=2
        )

        # ✅ Draw 25-yard lines
        self.canvas.create_line(
            center_x - pitch_width // 2, margin_top + pitch_length / 4,
            center_x + pitch_width // 2, margin_top + pitch_length / 4,
            fill="white", width=2
        )
        self.canvas.create_line(
            center_x - pitch_width // 2, margin_top + 3 * pitch_length / 4,
            center_x + pitch_width // 2, margin_top + 3 * pitch_length / 4,
            fill="white", width=2
        )

        # ✅ Draw goals
        goal_width = 37
        goal_depth = 8
        self.canvas.create_rectangle(
            center_x - goal_width // 2, margin_top - goal_depth,
            center_x + goal_width // 2, margin_top,
            outline="white", width=2
        )
        self.canvas.create_rectangle(
            center_x - goal_width // 2, margin_top + pitch_length,
            center_x + goal_width // 2, margin_top + pitch_length + goal_depth,
            outline="white", width=2
        )

        # ✅ Draw the "D" arcs (solid)
        d_radius = 146
        self.canvas.create_arc(
            center_x - d_radius, margin_top - d_radius,
            center_x + d_radius, margin_top + d_radius,
            start=0, extent=-180, outline="white", style=tk.ARC, width=2
        )
        self.canvas.create_arc(
            center_x - d_radius, margin_top + pitch_length - d_radius,
            center_x + d_radius, margin_top + pitch_length + d_radius,
            start=180, extent=-180, outline="white", style=tk.ARC, width=2
        )

        # ✅ Draw the dashed parallel arcs (50px larger)
        outer_d_radius = d_radius + 50
        self.canvas.create_arc(
            center_x - outer_d_radius, margin_top - outer_d_radius,
            center_x + outer_d_radius, margin_top + outer_d_radius,
            start=0, extent=-180, outline="white", style=tk.ARC, width=1.2, dash=(5, 5)
        )
        self.canvas.create_arc(
            center_x - outer_d_radius, margin_top + pitch_length - outer_d_radius,
            center_x + outer_d_radius, margin_top + pitch_length + outer_d_radius,
            start=180, extent=-180, outline="white", style=tk.ARC, width=1.2, dash=(5, 5)
        )

        # ✅ Draw penalty spots (64.7px from baseline, centered)
        penalty_spot_radius = 1.5  # Small circle size
        penalty_spot_offset = 64.7

        # Top D arc penalty spot
        self.canvas.create_oval(
            center_x - penalty_spot_radius, margin_top + penalty_spot_offset - penalty_spot_radius,
            center_x + penalty_spot_radius, margin_top + penalty_spot_offset + penalty_spot_radius,
            fill="white", outline="white"
        )

        # Bottom D arc penalty spot
        self.canvas.create_oval(
            center_x - penalty_spot_radius, margin_top + pitch_length - penalty_spot_offset - penalty_spot_radius,
            center_x + penalty_spot_radius, margin_top + pitch_length - penalty_spot_offset + penalty_spot_radius,
            fill="white", outline="white"
        )

    def draw_ball(self):
        """ Draws the ball on top of all other elements. """
        x, y = BALL_START_POSITION
        self.ball = self.canvas.create_oval(
            x - BALL_RADIUS, y - BALL_RADIUS,
            x + BALL_RADIUS, y + BALL_RADIUS,
            fill=BALL_COLOR, outline="", tags="ball"
        )

    def make_ball_draggable(self):
        """ Makes the ball draggable across the screen. """
        drag_data = {"x": None, "y": None}

        def on_press(event):
            """ Stores the initial position when the ball is clicked. """
            drag_data["x"], drag_data["y"] = event.x, event.y

        def on_drag(event):
            """ Moves the ball smoothly while dragging. """
            if drag_data["x"] is None or drag_data["y"] is None:
                return

            new_x, new_y = event.x, event.y
            self.canvas.coords(
                self.ball,
                new_x - BALL_RADIUS, new_y - BALL_RADIUS,
                new_x + BALL_RADIUS, new_y + BALL_RADIUS
            )
            drag_data["x"], drag_data["y"] = new_x, new_y

        def on_release(event):
            """ Clears drag data when the ball is released. """
            drag_data["x"], drag_data["y"] = None, None

        self.canvas.tag_bind(self.ball, "<ButtonPress-1>", on_press)
        self.canvas.tag_bind(self.ball, "<B1-Motion>", on_drag)
        self.canvas.tag_bind(self.ball, "<ButtonRelease-1>", on_release)

    def reset_all_positions(self):
        """ Resets the ball and all players to their original positions. """
        # ✅ Reset players
        self.players.reset_positions()

        # ✅ Reset ball to its original position
        x, y = BALL_START_POSITION
        self.canvas.coords(
            self.ball,
            x - BALL_RADIUS, y - BALL_RADIUS,
            x + BALL_RADIUS, y + BALL_RADIUS
        )


if __name__ == "__main__":
    root = tk.Tk()
    HockeyPitch(root)
    root.mainloop()

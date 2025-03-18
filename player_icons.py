import tkinter as tk
from player_config import PLAYER_RADIUS, PLAYER_FONT_SIZE, TEAM_COLORS, ALL_PLAYERS

class PlayerIcon:
    def __init__(self, canvas, x, y, label, team):
        """
        Represents a player icon on the canvas.

        Parameters:
            canvas (tk.Canvas): The canvas where the player is drawn.
            x (int): X-coordinate.
            y (int): Y-coordinate.
            label (str): Position label (e.g., "GK", "CF").
            team (str): Team name ("Essendon" or "Opponent").
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.label = label
        self.team = team

        # Retrieve team colors from config
        colors = TEAM_COLORS.get(team, TEAM_COLORS["Opponent"])
        self.fill_color = colors["fill"]
        self.outline_color = colors["outline"]
        self.font_color = colors["font"]

        # Draw player icon
        self.circle, self.label_text, self.coord_text = self.draw_icon()

        # Make draggable
        self.make_draggable()

    def draw_icon(self):
        """ Draws a player circle with a label and coordinates. """
        circle = self.canvas.create_oval(
            self.x - PLAYER_RADIUS, self.y - PLAYER_RADIUS,
            self.x + PLAYER_RADIUS, self.y + PLAYER_RADIUS,
            fill=self.fill_color, outline=self.outline_color, width=3, tags="players"
        )
        label_text = self.canvas.create_text(
            self.x, self.y, text=self.label, fill=self.font_color,
            font=("Arial", PLAYER_FONT_SIZE, "bold"), tags="players"
        )
        coord_text = self.canvas.create_text(
            self.x, self.y + 20, text=f"({self.x},{self.y})",
            fill="white", font=("Arial", PLAYER_FONT_SIZE), tags="players"
        )
        return circle, label_text, coord_text

    def update_position(self, new_x, new_y):
        """ Updates the player's position on the canvas and updates the coordinate text. """
        self.x, self.y = new_x, new_y
        self.canvas.coords(self.circle, new_x - PLAYER_RADIUS, new_y - PLAYER_RADIUS,
                           new_x + PLAYER_RADIUS, new_y + PLAYER_RADIUS)
        self.canvas.coords(self.label_text, new_x, new_y)
        self.canvas.coords(self.coord_text, new_x, new_y + 20)
        self.canvas.itemconfig(self.coord_text, text=f"({new_x},{new_y})")  # ✅ Update coordinate display

    def make_draggable(self):
        """ Enables dragging functionality for the player. """
        drag_data = {"x": None, "y": None}

        def on_press(event):
            drag_data["x"], drag_data["y"] = event.x, event.y
            self.canvas.itemconfig(self.circle, outline="blue", width=3)

        def on_drag(event):
            if drag_data["x"] is None or drag_data["y"] is None:
                return
            new_x, new_y = event.x, event.y
            self.update_position(new_x, new_y)  # ✅ Update position dynamically
            drag_data["x"], drag_data["y"] = new_x, new_y

        def on_release(event):
            self.canvas.itemconfig(self.circle, outline=self.outline_color, width=2)
            drag_data["x"], drag_data["y"] = None, None

        self.canvas.tag_bind(self.circle, "<ButtonPress-1>", on_press)
        self.canvas.tag_bind(self.circle, "<B1-Motion>", on_drag)
        self.canvas.tag_bind(self.circle, "<ButtonRelease-1>", on_release)


class PlayerIconManager:
    def __init__(self, canvas):
        """
        Manages all player icons (Essendon and Opponent).

        Parameters:
            canvas (tk.Canvas): The canvas where players are drawn.
        """
        self.canvas = canvas
        self.players = []

        # Create players from the config file
        for team, label, x, y in ALL_PLAYERS:
            player = PlayerIcon(canvas, x, y, label, team)
            self.players.append(player)

    def reset_positions(self):
        """ Resets all players to their original positions. """
        for player, (_, _, x, y) in zip(self.players, ALL_PLAYERS):
            player.update_position(x, y)

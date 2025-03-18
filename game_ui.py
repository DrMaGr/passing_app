import tkinter as tk

class GameUI:
    def __init__(self, root, hockey_pitch):
        """
        Creates UI buttons and sliders for game control.

        Parameters:
            root (tk.Tk): The main application window.
            hockey_pitch (HockeyPitch): The hockey pitch instance to control.
        """
        self.hockey_pitch = hockey_pitch

        # ✅ Create a frame for UI controls
        self.control_frame = tk.Frame(root, width=200, bg="gray")
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # ✅ Add the "Reset Ball and Positions" button
        self.reset_button = tk.Button(
            self.control_frame,
            text="Reset Ball and Positions",
            command=self.hockey_pitch.reset_all_positions,  # Calls reset function
            bg="black",
            fg="white"
        )
        self.reset_button.pack(pady=10)

        # ✅ Add the "Toggle Passing Lines" button
        self.toggle_lines_button = tk.Button(
            self.control_frame,
            text="Toggle Passing Lines On/Off",
            command=self.toggle_passing_lines,
            bg="black",
            fg="white"
        )
        self.toggle_lines_button.pack(pady=10)

        # ✅ Label for "Max Passing Length"
        self.passing_length_label = tk.Label(
            self.control_frame,
            text="Max Passing Length",
            bg="gray",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.passing_length_label.pack()

        # ✅ Subtext: "Distance (m)"
        self.distance_label = tk.Label(
            self.control_frame,
            text="Distance (m)",
            bg="gray",
            fg="white",
            font=("Arial", 9)
        )
        self.distance_label.pack()

        # ✅ Slider for max passing line length (displays value dynamically)
        self.line_length_slider = tk.Scale(
            self.control_frame,
            from_=50, to=400,  # ✅ Internally still in pixels
            orient=tk.HORIZONTAL,
            command=self.update_max_line_length,
            showvalue=False  # ✅ Hide default number
        )
        self.line_length_slider.set(300)  # Default to 30m (300px)
        self.line_length_slider.pack(pady=5)

        # ✅ Dynamic label for slider value (Max Passing Length)
        self.line_length_display = tk.Label(
            self.control_frame,
            text=f"{self.line_length_slider.get() // 10}m",
            bg="gray",
            fg="white",
            font=("Arial", 9),
            width=5  # ✅ Set initial width, but will adjust dynamically
        )
        self.line_length_display.pack()

        # ✅ Label for "Opponent Danger Zone"
        self.danger_zone_label = tk.Label(
            self.control_frame,
            text="Opponent Danger Zone",
            bg="gray",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.danger_zone_label.pack()

        # ✅ Subtext: "Threshold (m)"
        self.danger_zone_subtext = tk.Label(
            self.control_frame,
            text="Threshold (m)",
            bg="gray",
            fg="white",
            font=("Arial", 9)
        )
        self.danger_zone_subtext.pack()

        # ✅ Slider for controlling opponent danger zone (now in meters)
        self.danger_zone_slider = tk.Scale(
            self.control_frame,
            from_=1, to=10,  # ✅ Now ranges from 1m to 10m
            orient=tk.HORIZONTAL,
            command=self.update_danger_zone,
            showvalue=False  # ✅ Hide default number
        )
        self.danger_zone_slider.set(5)  # Default to 5m (50px)
        self.danger_zone_slider.pack(pady=5)

        # ✅ Dynamic label for slider value (Opponent Danger Zone)
        self.danger_zone_display = tk.Label(
            self.control_frame,
            text=f"{self.danger_zone_slider.get()}m",
            bg="gray",
            fg="white",
            font=("Arial", 9),
            width=5  # ✅ Set initial width, but will adjust dynamically
        )
        self.danger_zone_display.pack()

    def toggle_passing_lines(self):
        """ Toggles the visibility of passing lines. """
        self.hockey_pitch.passing_lines.toggle_passing_lines()

    def update_max_line_length(self, value):
        """ Updates the max passing line length based on slider value and adjusts the label width dynamically. """
        self.hockey_pitch.passing_lines.set_max_length(int(value))
        display_text = f"{int(value) // 10}m"  # ✅ Convert to meters
        self.line_length_display.config(text=display_text, width=len(display_text) + 2)  # ✅ Adjust width

    def update_danger_zone(self, value):
        """ Updates the opponent danger zone distance based on slider value (converts meters to pixels) and adjusts width. """
        self.hockey_pitch.passing_lines.set_danger_zone(int(value) * 10)
        display_text = f"{int(value)}m"
        self.danger_zone_display.config(text=display_text, width=len(display_text) + 2)  # ✅ Adjust width

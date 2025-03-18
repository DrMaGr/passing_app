class PassingLines:
    def __init__(self, canvas, players):
        """
        Initializes the passing lines for Essendon players.

        Parameters:
            canvas (tk.Canvas): The game canvas.
            players (list): List of player objects.
        """
        self.canvas = canvas
        self.players = players
        self.lines = {}  # Stores lines mapped between players
        self.lines_visible = True  # Tracks visibility state
        self.max_length = 300  # Default max line length, controlled by slider
        self.danger_zone = 50  # Default opponent proximity threshold, controlled by slider

        # ✅ Get all Essendon players except the GK
        essendon_players = [p for p in self.players.players if p.team == "Essendon" and p.label != "GK"]

        # ✅ Create connections for each player to multiple nearby teammates
        for player1 in essendon_players:
            for player2 in essendon_players:
                if player1 != player2:  # Avoid self-connection
                    line = self.canvas.create_line(
                        player1.x, player1.y, player2.x, player2.y,
                        fill="black", width=10, tags="passing_lines"
                    )
                    self.lines[(player1, player2)] = line

        # ✅ Ensure passing lines are drawn below player icons but above the pitch
        self.canvas.tag_lower("passing_lines", "players")

        # ✅ Attach to players so lines move when players move
        self.attach_to_players()

        # ✅ Attach opponents so they trigger passing line updates dynamically
        self.attach_to_opponents()

    def update_lines(self):
        """ Updates all passing lines dynamically based on player movement and proximity to opponents. """
        opponents = [p for p in self.players.players if p.team == "Opponent"]

        for (player1, player2), line in self.lines.items():
            # Calculate new line length
            length = ((player1.x - player2.x) ** 2 + (player1.y - player2.y) ** 2) ** 0.5

            # Hide line if it's too long or globally disabled
            if length >= self.max_length or not self.lines_visible:
                self.canvas.itemconfig(line, state="hidden")
            else:
                # Calculate dynamic thickness (10px at shortest, thinning out)
                thickness = max(2, 10 - (length / 30))  # Decreases gradually
                self.canvas.itemconfig(line, state="normal", width=thickness)

                # Determine if line should turn red based on proximity to an opponent
                line_color = "black"
                for opponent in opponents:
                    if self.is_near_line(player1, player2, opponent):
                        line_color = "red"
                        break  # Stop checking once red is confirmed

                # Update line color and position
                self.canvas.itemconfig(line, fill=line_color)
                self.canvas.coords(line, player1.x, player1.y, player2.x, player2.y)

    def is_near_line(self, player1, player2, opponent):
        """
        Checks if an opponent is within the current danger zone distance of a passing line.

        Parameters:
            player1 (PlayerIcon): First player in the passing line.
            player2 (PlayerIcon): Second player in the passing line.
            opponent (PlayerIcon): Opponent to check proximity.

        Returns:
            bool: True if opponent is within the danger zone distance of the line, else False.
        """
        x1, y1 = player1.x, player1.y
        x2, y2 = player2.x, player2.y
        ox, oy = opponent.x, opponent.y

        # Compute the distance from the opponent to the line segment
        if (x2 - x1) == 0:  # Vertical line case
            closest_x = x1
            closest_y = min(max(y1, oy), y2) if y1 < y2 else min(max(y2, oy), y1)
        else:
            m = (y2 - y1) / (x2 - x1)  # Line slope
            b = y1 - m * x1  # Line equation: y = mx + b
            closest_x = (ox + m * (oy - b)) / (m**2 + 1)
            closest_y = m * closest_x + b

        # Ensure closest point is within segment bounds
        closest_x = min(max(x1, closest_x), x2) if x1 < x2 else min(max(x2, closest_x), x1)
        closest_y = min(max(y1, closest_y), y2) if y1 < y2 else min(max(y2, closest_y), y1)

        # Compute the distance from the opponent to the closest point on the line
        distance = ((closest_x - ox) ** 2 + (closest_y - oy) ** 2) ** 0.5
        return distance <= self.danger_zone

    def attach_to_players(self):
        """ Ensures lines update dynamically when Essendon players move. """
        for player in self.players.players:
            if player.team == "Essendon" and player.label != "GK":
                player.update_position = self.wrap_update_position(player.update_position)

    def attach_to_opponents(self):
        """ Ensures lines update dynamically when opponent players move. """
        for opponent in self.players.players:
            if opponent.team == "Opponent":
                opponent.update_position = self.wrap_update_position(opponent.update_position)

    def wrap_update_position(self, original_update):
        """ Wraps the player's update_position to also update passing lines. """
        def new_update_position(new_x, new_y):
            original_update(new_x, new_y)  # Keep original movement
            self.update_lines()  # Update passing lines in real time
        return new_update_position

    def toggle_passing_lines(self):
        """ Toggles visibility of passing lines. """
        self.lines_visible = not self.lines_visible
        new_state = "normal" if self.lines_visible else "hidden"
        for line in self.lines.values():
            self.canvas.itemconfig(line, state=new_state)

    def set_max_length(self, value):
        """ Updates the max length of passing lines based on slider input. """
        self.max_length = int(value)
        self.update_lines()  # Recalculate line visibility with new length

    def set_danger_zone(self, value):
        """ Updates the opponent danger zone distance based on slider input. """
        self.danger_zone = int(value)
        self.update_lines()  # Recalculate line visibility with new danger zone

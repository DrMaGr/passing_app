# player_config.py

# Player display settings
PLAYER_RADIUS = 10
PLAYER_FONT_SIZE = 7

# Team colors
TEAM_COLORS = {
    "Essendon": {"fill": "black", "outline": "red", "font": "white"},
    "Opponent": {"fill": "white", "outline": "blue", "font": "blue"}
}

# player_config.py

# Player display settings
PLAYER_RADIUS = 10
PLAYER_FONT_SIZE = 8

# Team colors
TEAM_COLORS = {
    "Essendon": {"fill": "black", "outline": "red", "font": "white"},
    "Opponent": {"fill": "white", "outline": "blue", "font": "blue"}
}

# Ball settings
BALL_RADIUS = 4  # Ball size
BALL_COLOR = "yellow"  # Ball color
BALL_START_POSITION = (859, 503)  # Ball's initial position

# Player positions (with team assignments)
ALL_PLAYERS = [
    ("Opponent", "GK", 860, 89),
    ("Opponent", "LB", 796, 232),
    ("Opponent", "RB", 936, 232),
    ("Opponent", "LH", 624, 311),
    ("Opponent", "CH", 859, 311),
    ("Opponent", "RH", 1100, 311),
    ("Opponent", "LI", 997, 421),
    ("Opponent", "RI", 736, 421),
    ("Opponent", "LW", 1104, 476),
    ("Opponent", "RW", 610, 476),
    ("Opponent", "CF", 855, 459),

    ("Essendon", "GK", 859, 912),
    ("Essendon", "LB", 775, 782),
    ("Essendon", "RB", 931, 782),
    ("Essendon", "LH", 624, 696),
    ("Essendon", "CH", 863, 696),
    ("Essendon", "RH", 1101, 696),
    ("Essendon", "LI", 734, 591),
    ("Essendon", "RI", 1000, 591),
    ("Essendon", "LW", 607, 525),
    ("Essendon", "RW", 1104, 523),
    ("Essendon", "CF", 856, 521),
]

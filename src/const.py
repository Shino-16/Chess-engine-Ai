# Sidebar width
SIDEBAR_WIDTH = 400

# Screen dimensions
WIDTH = 800 + SIDEBAR_WIDTH  # 800 for board, 300 for right sidebar
HEIGHT = 800

# Board dimensions
ROWS = 8
COLS = 8

# Square size (board is always 800x800)
SQSIZE = 800 // ROWS

# Offsets to start drawing the board at the left edge
X_OFFSET = 0
Y_OFFSET = 0

# Player info box positions (now in the right sidebar)
PLAYER_BOX_WIDTH = 260
PLAYER_BOX_HEIGHT = 80

# Player 2 (Black) - top right
PLAYER2_BOX_X = 800 + (SIDEBAR_WIDTH - PLAYER_BOX_WIDTH) // 2
PLAYER2_BOX_Y = 40

# Player 1 (White) - bottom right
PLAYER1_BOX_X = 800 + (SIDEBAR_WIDTH - PLAYER_BOX_WIDTH) // 2
PLAYER1_BOX_Y = HEIGHT - PLAYER_BOX_HEIGHT - 40
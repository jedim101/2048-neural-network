import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

board = [ [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0] ]

def print_board():
  for row in board:
    colors = {
      0: "",
      2: "\033[104m",   # Bright Blue Background
      4: "\033[103m",   # Bright Yellow Background
      8: "\033[102m",   # Bright Green Background
      16: "\033[101m",  # Bright Red Background
      32: "\033[105m",  # Bright Magenta Background
      64: "\033[106m",  # Bright Cyan Background
      128: "\033[107m", # Bright White Background
      256: "\033[100m", # Bright Black/Grey Background
      512: "\033[44m",  # Blue Background
 
    }
    for tile in row:
      print(colors[tile] + str(tile) + (" " * (4 - len(str(tile)))), end="\033[0m ")
    print()

def get_empty_tiles():
  global board

  empty_tiles = []
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == 0:
        empty_tiles.append((i, j))
  return empty_tiles

def add_tile():
  empty_tiles = get_empty_tiles()
  if len(empty_tiles) > 0:
    random_tile = random.choice(empty_tiles)
    board[random_tile[0]][random_tile[1]] = 2 if random.random() < 0.9 else 4

def setup_game():
  board = add_tile()
  board = add_tile()

def move(direction):
  global board

  def transpose(board):
    return [list(row) for row in zip(*board)]
  
  def flip_x(board):
    return [row[::-1] for row in board]

  def flip_y(board):
    return board[::-1]

  def move_left(board):
    new_board = []
    for i in range(len(board)):
      row = [tile for tile in board[i] if tile != 0]
      j = 0
      while j < len(row) - 1:
        if row[j] == row[j + 1]:
          row[j] = row[j] * 2
          row.pop(j + 1)

        j += 1
      row = row + [0] * (len(board[i]) - len(row))
      new_board.append(row)
    return new_board

  if direction == LEFT:
    board = move_left(board)
  elif direction == RIGHT:
    board = flip_x(move_left(flip_x(board)))
  elif direction == UP:
    board = transpose(move_left(transpose(board)))
  elif direction == DOWN:
    board = flip_y(transpose(move_left(transpose(flip_y(board)))))

  add_tile()

def play_game():
  setup_game()
  print_board()

  while True:
    direction = input("")
    if direction == "w":
      move(UP)
    elif direction == "s":
      move(DOWN)
    elif direction == "a":
      move(LEFT)
    elif direction == "d":
      move(RIGHT)

    print()
    print_board()
    print()

play_game()
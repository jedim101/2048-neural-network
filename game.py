import math
import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

board = []

score = 0

def print_board():
  for row in board:
    colors = {
      0: "",
      1: "\033[104m",   # Bright Blue Background
      2: "\033[103m",   # Bright Yellow Background
      3: "\033[102m",   # Bright Green Background
      4: "\033[101m",  # Bright Red Background
      5: "\033[105m",  # Bright Magenta Background
      6: "\033[106m",  # Bright Cyan Background
      7: "\033[107m", # Bright White Background
      8: "\033[100m", # Bright Black/Grey Background
      9: "\033[44m",  # Blue Background
      10: "\033[42m", # Green Background
      11: "\033[41m", # Red Background
      12: "\033[43m", # Yellow Background
      13: "\033[45m", # Magenta Background
      14: "\033[46m", # Cyan Background
    }
    for tile in row:
      number_string = "--" if tile == 0 else str(int(math.pow(2, tile)))
      print(colors[tile] + (" " * int(math.floor(3 - len(number_string) / 2))) + number_string + (" " * int(math.ceil(3 - len(number_string) / 2))), end="\033[0m")
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
    board[random_tile[0]][random_tile[1]] = 1 if random.random() < 0.9 else 2

def setup_game():
  global board, score
  score = 0
  board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
  add_tile()
  add_tile()

def move(direction):
  global board

  def transpose(board):
    return [list(row) for row in zip(*board)]
  
  def flip_x(board):
    return [row[::-1] for row in board]

  def flip_y(board):
    return board[::-1]

  def move_left(board):
    global score

    new_board = []
    for i in range(len(board)):
      row = [tile for tile in board[i] if tile != 0]
      j = 0
      while j < len(row) - 1:
        if row[j] == row[j + 1]:
          score += math.pow(2, row[j] + 1)

          row[j] = row[j] + 1
          row.pop(j + 1)


        j += 1
      row = row + [0] * (len(board[i]) - len(row))
      new_board.append(row)
    return new_board

  if direction == LEFT:
    new_board = move_left(board)
  elif direction == RIGHT:
    new_board = flip_x(move_left(flip_x(board)))
  elif direction == UP:
    new_board = transpose(move_left(transpose(board)))
  elif direction == DOWN:
    new_board = flip_y(transpose(move_left(transpose(flip_y(board)))))

  if new_board == board:
    return False
  else:
    board = new_board
    return True

def is_game_over():
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == 0:
        return False
      if i < len(board) - 1 and board[i][j] == board[i + 1][j]:
        return False
      if j < len(board[i]) - 1 and board[i][j] == board[i][j + 1]:
        return False
      if i > 0 and board[i][j] == board[i - 1][j]:
        return False
      if j > 0 and board[i][j] == board[i][j - 1]:
        return False
  return True

def get_score():
  # score = 0
  # for i in range(len(board)):
  #   for j in range(len(board[i])):
  #     score += math.pow(2, board[i][j]) if board[i][j] != 0 else 0
  return score

def get_board_as_player_input():
  output = []
  for i in range(len(board)):
    output += board[i]
  return output

def play_game():
  setup_game()
  print_board()

  while True:
    key_pressed = input("")
    direction = None
    if key_pressed == "w":
      direction = UP
    elif key_pressed == "s":
      direction = DOWN
    elif key_pressed == "a":
      direction = LEFT
    elif key_pressed == "d":
      direction = RIGHT
    else:
      continue

    if move(direction) is False:
      continue

    print()
    print_board()
    print("Score: ", get_score())
    print()

    if is_game_over():
      print("Game Over")
      print("Score: ", get_score())
      break

def get_log_score():
  score = 0
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == 0:
        continue
      score += board[i][j]
  return score

def is_legal_move(direction):
  global board, score
  board_copy = [row[:] for row in board]
  score_copy = score

  legal = move(direction)

  board = board_copy
  score = score_copy
  return legal

def get_legal_moves():
  legal_moves = []
  for direction in [UP, RIGHT, DOWN, LEFT]:
    if is_legal_move(direction):
      legal_moves.append(direction)
  return legal_moves

# play_game()
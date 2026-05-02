import game
import json

with open("game_log.json", "r") as f:
  game_log = json.load(f)

for state in game_log:
  game.board = state["board"]
  game.print_board()
  print("Score: ", state["score"])
  print()
  input()

print("Moves count: ", len(game_log))
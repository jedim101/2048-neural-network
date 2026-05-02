import agent
import game
import time
import copy
import json

start_time = time.time()

iterations = 5000

agent.random_weights_and_biases()
# with open("network_params.json", "r") as f:
#   agent.network_params = json.load(f)

agent.save_network()

round_start_time = time.time()

score_history = []

high_score = 0
high_score_game_log = []

i = 0

# for i in range(iterations):
while True:
  i += 1
  iteration_start_time = time.time()
  total_reward = 0

  game_log = []

  # for _ in range(100):
  #   print()

  moves_count = 0

  reward = 0

  agent.reset_variables()

  game.setup_game()
  # game.print_board()

  game_log.append({
    "board": copy.deepcopy(game.board),
    "score": game.score,
  })

  while not game.is_game_over():
    moves_count += 1

    state = game.get_board_as_player_input()

    initial_score = game.score
    # print("Initial score:", initial_score)

    legal_moves = game.get_legal_moves()
    move = agent.make_move(state, reward, legal_moves)

    total_reward += reward

    game.move(move)

    reward = game.score - initial_score

    game_log.append({
      "board": copy.deepcopy(game.board),
      "score": game.score,
    })

    # print()
    # print()
    # print()

    # print("Move:", "UP" if move == 0 else "RIGHT" if move == 1 else "DOWN" if move == 2 else "LEFT")
    # print()
    # print("move #:", moves_count)
    # game.print_board()
    # print("Score:", game.score)
    # print("Initial score:", initial_score)
    # print()
    # print("Reward:", reward)
    # print()
    # print()
    # print()

  agent.make_move(None, reward, game.get_legal_moves())

  agent.decay_epsilon()

  agent.save_network()

  score_history.append(int(game.score))

  if game.score > high_score:
    high_score = game.score
    with open("game_log.json", "w") as f:
      json.dump(game_log, f)

  with open("score_history.json", "r") as f:
    score_history = json.load(f)
    score_history.append(game.score)
  with open("score_history.json", "w") as f:
    json.dump(score_history, f)
  with open("network_params.json", "w") as f:
    json.dump(agent.network_params, f)

  print()
  game.print_board()
  print("Iteration:", i + 1)
  print("Moves count: ", moves_count)
  print("Score: ", game.score)
  print("Log Tile Count: ", game.get_log_score())
  print("Epsilon: ", agent.epsilon)
  print("Total reward: ", total_reward)
  print("Iteration time: ", time.time() - iteration_start_time)
  # print("█" * int(i / iterations * 100) + "-" * (100 - int(i / iterations * 100)))
  print()



# ------------------------------------------------------------

for i in range(10):
  print()
print("Iterations: ", iterations)
print("Time taken: ", time.time() - round_start_time, "seconds")
print("High score: ", high_score)

print()

print("Total time taken: ", time.time() - start_time)

# print("High score game log: ", high_score_game_log)

with open("game_log.json", "w") as f:
  json.dump(high_score_game_log, f)

with open("score_history.json", "a") as f:
  json.dump(score_history, f)

with open("network_params.json", "w") as f:
  json.dump(agent.network_params, f)
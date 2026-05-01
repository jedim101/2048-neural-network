from turtle import screensize
import agent
import game
import time

start_time = time.time()

iterations = 10000

agent.random_weights_and_biases()
agent.save_network()

round_start_time = time.time()

score_history = []
invalid_move_history = []
invalid_move_percentage_history = []
total_reward_history = []

for i in range(iterations):
  iteration_start_time = time.time()
  total_reward = 0

  # for _ in range(100):
  #   print()

  moves_count = 0

  invalid_move_count = 0

  reward = 0

  agent.reset_variables()

  game.setup_game()
  # game.print_board()

  while not game.is_game_over():
    moves_count += 1

    state = game.get_board_as_player_input()

    initial_score = game.get_score()

    move = agent.make_move(state, reward)

    reward = 0

    legal_move = game.move(move)

    if not legal_move:
      invalid_move_count += 1
      reward = -100

    new__score = game.get_score()

    reward += (new__score - initial_score)
    total_reward += reward

    if legal_move:
      game.add_tile()

    # print()
    # print()
    # print()
    
    # print("Move:", "UP" if move == 0 else "RIGHT" if move == 1 else "DOWN" if move == 2 else "LEFT")
    # print()
    # print("move #:", moves_count)
    # game.print_board()
    # print("Score:", game.get_score())
    # print()
    # print("Reward:", reward)

  agent.make_move(None, reward)

  agent.decay_epsilon()

  agent.save_network()

  score_history.append(str(int(game.get_score())))
  invalid_move_history.append(str(invalid_move_count))
  invalid_move_percentage_history.append(str(invalid_move_count / moves_count))
  total_reward_history.append(str(total_reward))

  print()
  game.print_board()
  print("Iteration:", i + 1)
  print("Moves count: ", moves_count)
  print("Score: ", game.get_score())
  print("Log score: ", game.get_log_score())
  print("Invalid move count: ", invalid_move_count)
  print("Epsilon: ", agent.epsilon)
  print("Total reward: ", total_reward)
  print("Iteration time: ", time.time() - iteration_start_time)
  print()


for i in range(10):
  print()
print("Iterations: ", iterations)
print("Time taken: ", time.time() - round_start_time, "seconds")
print()

print("Total time taken: ", time.time() - start_time)

print()
print("Score history:\n", "\n".join(score_history))
print()
print("Invalid move history:\n", "\n".join(invalid_move_history))
print()
print("Invalid move percentage history:\n", "\n".join(invalid_move_percentage_history))
print()
print("Total reward history:\n", "\n".join(total_reward_history))
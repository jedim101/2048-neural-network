import agent
import game
import random
import time

start_time = time.time()

iterations = 100000

round_data = []

agent.random_weights_and_biases()

round_start_time = time.time()

total_invalid_move_count = 0
total_score = 0


for i in range(iterations):

  invalid_move_count = 0
  reward = 0

  game.setup_game()

  while not game.is_game_over():

    state = game.get_board_as_player_input()
    initial_log_score = game.get_log_score()

    move = agent.make_move(state, reward)

    new_log_score = game.get_log_score()
    reward = new_log_score - initial_log_score

    if not game.move(move):
      invalid_move_count += 1
      reward -= 100
      while not game.move(random.randint(0, 3)):
        pass

    game.print_board()
    print("Iteration:", i + 1)
    print("Move: ", move)
    print("Log score: ", new_log_score)
    print("Reward: ", reward)
    print("Score:", game.get_score())
    print("Invalid move count:", invalid_move_count)
    print("Average Score:", total_score / (i + 1), "Average Invalid move count:", total_invalid_move_count / (i + 1))
    print()

  
  total_invalid_move_count += invalid_move_count
  total_score += game.get_score()

  print()
  # game.print_board()
  # print("Invalid move count: ", invalid_move_count)
  # print("Score: ", game.get_score())
  print("Iteration:", i + 1, "Score:", game.get_score(), "Invalid move count:", invalid_move_count, "Average Score:", total_score / (i + 1), "Average Invalid move count:", total_invalid_move_count / (i + 1))


for i in range(100):
  print()
print("Iterations: ", iterations)
print("Time taken: ", time.time() - round_start_time, "seconds")
print("Total invalid move count: ", total_invalid_move_count)
print("Total score: ", total_score)
print("Average invalid move count: ", total_invalid_move_count / iterations)
print("Average score: ", total_score / iterations)

round_data.append({
  "average_invalid_move_count": total_invalid_move_count / iterations,
  "average_score": total_score / iterations,
  "time_taken": time.time() - round_start_time,
})

print("--------------------------------")
print("Round data:")
for i in range(len(round_data)):
  print("Round: ", i + 1)
  print("Average invalid move count: ", round_data[i]["average_invalid_move_count"])
  print("Average score: ", round_data[i]["average_score"])
  print("Time taken: ", round_data[i]["time_taken"])
  print()

print("Total time taken: ", time.time() - start_time)
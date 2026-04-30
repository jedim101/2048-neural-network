import player
import game
import teacher
import random
import time

start_time = time.time()

iterations = 1000
rounds = 100

round_data = []

teacher.randomize_networks(iterations)

for round in range(rounds):
  round_start_time = time.time()

  total_invalid_move_count = 0
  total_score = 0

  for network_index, network in enumerate(teacher.networks):
    invalid_move_count = 0

    player.set_network(network)

    game.setup_game()

    invalid_move_count = 0

    while not game.is_game_over():

      move = player.make_move(game.get_board_as_player_input())

      if not game.move(move):
        invalid_move_count += 1
        while not game.move(random.randint(0, 3)):
          pass

    
    total_invalid_move_count += invalid_move_count
    total_score += game.get_score()

    teacher.all_games.append({
      "invalid_move_count": invalid_move_count,
      "score": game.get_score(),
      "network": player.network.copy(),
    })

    print()
    # game.print_board()
    # print("Invalid move count: ", invalid_move_count)
    # print("Score: ", game.get_score())
    print("Round:", round + 1, " Game:", network_index + 1, "Average Round Score:", total_score / (network_index + 1))


  for i in range(100):
    print()
  print("Round: ", round + 1)
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

  teacher.evolve_networks(int(iterations / 100), iterations)

print("--------------------------------")
print("Round data:")
for i in range(len(round_data)):
  print("Round: ", i + 1)
  print("Average invalid move count: ", round_data[i]["average_invalid_move_count"])
  print("Average score: ", round_data[i]["average_score"])
  print("Time taken: ", round_data[i]["time_taken"])
  print()

print("Total time taken: ", time.time() - start_time)
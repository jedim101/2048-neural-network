import player
import game
import random
import time

start_time = time.time()

total_invalid_move_count = 0
total_score = 0

iterations = 1000
for i in range(iterations):
  invalid_move_count = 0

  player.random_weights_and_biases()

  game.setup_game()
  game.print_board()

  invalid_move_count = 0

  while not game.is_game_over():
    # input()

    move = player.make_move(game.get_board_as_player_input())
    print(move)

    if not game.move(move):
      print("Invalid move, randomizing...")
      invalid_move_count += 1
      while not game.move(random.randint(0, 3)):
        pass
    
    print()
    game.print_board()
    print()

  print("Invalid move count: ", invalid_move_count)
  print("Score: ", game.get_score())

  total_invalid_move_count += invalid_move_count
  total_score += game.get_score()

print()
print("Iterations: ", iterations)
print("Time taken: ", time.time() - start_time, "seconds")
print("Total invalid move count: ", total_invalid_move_count)
print("Total score: ", total_score)
print("Average invalid move count: ", total_invalid_move_count / iterations)
print("Average score: ", total_score / iterations)
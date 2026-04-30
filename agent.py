import random

GAMMA = 0.8
MAX_EPSILON = 0.9
MIN_EPSILON = 0.1

epsilon = MAX_EPSILON

network_params = [
  {
    "weights": [[0 for _ in range(16)] for _ in range(16)],
    "biases": [0 for _ in range(16)]
  },
  {
    "weights": [[0 for _ in range(16)] for _ in range(16)],
    "biases": [0 for _ in range(16)]
  },
  {
    "weights": [[0 for _ in range(16)] for _ in range(4)],
    "biases": [0 for _ in range(4)]
  }
]

neuron_values = []
new_neuron_values = []

chosen_action = [0, 0.0]

def set_network(net):
  global network_params
  network_params = net

def random_weights_and_biases():
  for layer in network_params:
    layer["weights"] = [[random.random() for _ in range(len(layer["weights"][0]))] for _ in range(len(layer["weights"]))]
    layer["biases"] = [random.random() for _ in range(len(layer["biases"]))]

def run_network(input_layer):
  current_layer = input_layer
  new_neuron_values.append(current_layer)

  for layer in network_params:
    previous_layer = current_layer
    current_layer = []
    for neuron_index in range(len(layer["weights"])):
      neuron_value = 0
      for weight_index in range(len(layer["weights"][neuron_index])):
        neuron_value += layer["weights"][neuron_index][weight_index] * previous_layer[weight_index]
      neuron_value += layer["biases"][neuron_index]
      current_layer.append(neuron_value)
    neuron_values.append(current_layer)

  return current_layer

def backpropagate(expected_return):
    global chosen_action, network_params, neuron_values

    error = expected_return - chosen_action[1]
    
    pass

def make_move(state, reward):
  global chosen_action

  action_returns = run_network(state)

  actual_previous_return = reward + GAMMA * max(action_returns)
  backpropagate(actual_previous_return)

  if random.random() < epsilon:
    chosen_action_index = random.randint(0, 3) 
  else:
    chosen_action_index = action_returns.index(max(action_returns))

  chosen_action = [chosen_action_index, action_returns[chosen_action_index]]
  return chosen_action[0]


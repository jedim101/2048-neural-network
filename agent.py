import random
import math
import copy

GAMMA = 0.5
MAX_EPSILON = 0.9
MIN_EPSILON = 0.05

epsilon = MAX_EPSILON

EPSILON_DECAY_FACTOR = 0.0001

LEARNING_RATE = 0.01

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

saved_network_params = []

neuron_values = []

previous_state = None
previous_action_index = 0

def reset_variables():
  global neuron_values, previous_state, previous_action_index
  neuron_values = []
  previous_state = None
  previous_action_index = 0

def set_network(net):
  global network_params
  network_params = net

def save_network():
  global saved_network_params

  saved_network_params = copy.deepcopy(network_params)

def random_weights_and_biases():
  for layer in network_params:
    layer["weights"] = [[random.random() for _ in range(len(layer["weights"][0]))] for _ in range(len(layer["weights"]))]
    layer["biases"] = [random.random() for _ in range(len(layer["biases"]))]

def run_network(params, input_layer, save_neuron_values = False):
  global neuron_values

  if save_neuron_values:
    neuron_values = []
    neuron_values.append(input_layer)
  else:
    neuron_values = []

  current_layer = input_layer

  for (layer_index, layer) in enumerate(params):
    previous_layer = current_layer
    current_layer = []
    for neuron_index in range(len(layer["weights"])):
      neuron_value = 0
      for weight_index in range(len(layer["weights"][neuron_index])):
        neuron_value += layer["weights"][neuron_index][weight_index] * previous_layer[weight_index]
      neuron_value += layer["biases"][neuron_index]
      if layer_index != len(params) - 1:
        neuron_value = max(0, neuron_value)
      current_layer.append(neuron_value)
    if save_neuron_values:
      neuron_values.append(current_layer)

  return current_layer

def backprop(expected_return, action_index):
  global neuron_values, network_params

  output = neuron_values[-1]

  # 1. initialize gradient at output layer
  dL_da = [0 for _ in range(len(output))]
  dL_da[action_index] = 2 * (output[action_index] - expected_return)

  # 2. backprop through layers
  for layer_index in reversed(range(len(network_params))):
    layer = network_params[layer_index]

    activations = neuron_values[layer_index + 1]  # current layer output
    prev_activations = neuron_values[layer_index]

    dL_dz = [0 for _ in range(len(activations))]

    # ReLU derivative (applied using activation > 0 mask)
    if layer_index == len(network_params) - 1:
      dL_dz = dL_da
    else:
      for i in range(len(activations)):
        if activations[i] > 0:
          dL_dz[i] = dL_da[i]
        else:
          dL_dz[i] = 0

    # compute gradient to propagate to previous layer (USE CURRENT WEIGHTS BEFORE UPDATING)
    new_dL_da = [0 for _ in range(len(prev_activations))]

    for j in range(len(prev_activations)):
      total = 0
      for i in range(len(layer["weights"])):
        total += dL_dz[i] * layer["weights"][i][j]
      new_dL_da[j] = total

    # update weights + biases
    for i in range(len(layer["weights"])):
      for j in range(len(layer["weights"][i])):
        grad = dL_dz[i] * prev_activations[j]
        layer["weights"][i][j] -= LEARNING_RATE * grad

      layer["biases"][i] -= LEARNING_RATE * dL_dz[i]

    dL_da = new_dL_da

def make_move(state, reward):
  global previous_state, previous_action_index, epsilon

  if state is None and previous_state is not None:
    target = reward

    run_network(network_params, previous_state, True)

    backprop(target, previous_action_index)
    return

  if previous_state is not None:
    saved_output = run_network(saved_network_params, state, False)
    target = reward + GAMMA * max(saved_output)

    run_network(network_params, previous_state, True)

    backprop(target, previous_action_index)

  network_output = run_network(network_params, state, False)

  previous_state = state
  if random.random() < epsilon:
    previous_action_index = random.randint(0, 3) 
  else:
    previous_action_index = network_output.index(max(network_output))

  return previous_action_index

def decay_epsilon():
  global epsilon
  epsilon = max(MIN_EPSILON, epsilon - EPSILON_DECAY_FACTOR)
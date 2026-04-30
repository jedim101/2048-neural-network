import random

all_games = []
networks = []

DEFAULT_NETWORK = [
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

def random_network():
  network = DEFAULT_NETWORK.copy()
  for layer in network:
    layer["weights"] = [[random.random() for _ in range(len(layer["weights"][0]))] for _ in range(len(layer["weights"]))]
    layer["biases"] = [random.random() for _ in range(len(layer["biases"]))]
  return network

def randomize_networks(count):
  global networks
  networks = []
  for _ in range(count):
    networks.append(random_network())
  return networks

def evolve_networks(top_to_save, count):
  all_games.sort(key=lambda x: x["score"], reverse=True)
  top_games = all_games[:top_to_save]
  
  top_networks = list(map(lambda x: x["network"], top_games))

  new_networks = []
  new_networks.append(top_networks)

  for network in top_networks:
    for _ in range(int(count / top_to_save)):
      new_network = []

      for layer in network:
        new_weights = []
        new_biases = []

        for node_weights in layer["weights"]:
          new_node_weights = []
          for weight in node_weights:
            new_node_weights.append(weight * (random.random() * .2 + .9))
          new_weights.append(new_node_weights)
        for bias in layer["biases"]:
          new_biases.append(bias * (random.random() * .2 + .9))
        
          new_network.append({
            "weights": new_weights,
            "biases": new_biases
          })

    new_networks.append(new_network)
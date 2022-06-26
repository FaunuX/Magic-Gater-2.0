import neural_network as n_n
import random as rand
import copy


class Evolver():
  def __init__(self, expectation, shape, inputs):
    self.EXPECTATION = expectation
    self.shape = shape
    self.inputs = inputs

    self.model = n_n.neural_network(shape)


    self.best_cost = 1
    
  def mutate(self, iteration):
    self.networks = []

    for i in range(999):
      self.networks.append(copy.deepcopy(self.model))
      
    for network in self.networks:
      for changing_row in network.network[1:]:
        for changing_neuron in changing_row:
          if rand.randint(0, 1) == 0:
            changing_weight = rand.randint(0, len(changing_neuron.weights) - 1)
            changing_neuron_index = network.network[network.network.index(changing_row)].index(changing_neuron)
            network.network[network.network.index(changing_row)][changing_neuron_index].weights[changing_weight] += (rand.random() - 0.5) / (iteration + 1 / 1)
          else:
            changing_neuron.bias += rand.random() * rand.randint(-1, 1)
  
  def average_cost(self, network):
    distribution = [sum(network.cost(input, self.EXPECTATION[self.inputs.index(input)])) for input in self.inputs][:-1]
    numerator = sum([distribution[i] * (distribution.index(i) / 2) for i in range(len(distribution))])
    denominator = sum(range(len(distribution))) / 2
    return round(numerator / denominator * 2, 3) 

    

  def select(self):
    for network in self.networks:
      current_cost = self.average_cost(network)
      if current_cost < self.best_cost:
        self.best_cost = current_cost
        self.model = copy.deepcopy(network)


  def evolve(self, repeat=9):
    for i in range(repeat):
      #print(round(i / 9.99), self.best_cost)
      
      self.mutate(i)
      self.select()

  def add_data(self, output_data, input_data):
    self.EXPECTATION += output_data
    self.inputs += input_data
    self.evolve()

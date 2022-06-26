from math import e
import random as rand


class neuron:
  def __init__(self, weights, bias):
    self.weights = weights
    self.bias = bias
    self.value = 0
   
  def find_value(self, inputs):
    weighted_inputs = []
    for input in inputs:
      weight = self.weights[inputs.index(input)]
      weighted_inputs.append(weight * input)
      value = sum(weighted_inputs) - self.bias
      value = 1 / (1 + (e**-value))
    return value

class neural_network:
  def __init__(self, shape):
    self.shape = shape
    self.network = [[]] * len(self.shape)
    for i in range(len(self.shape) - 1):
      self.network[i + 1] = ([neuron(([0.5] * (self.shape[i])), 2)] * self.shape[i + 1])

  def run(self, inputs):
    self.network[0] = inputs
    layer_list = inputs
    for i in range(len(self.shape) - 1):
      new_layer_list = []
      for neuron in self.network[i + 1]:
        new_layer_list.append(neuron.find_value(layer_list))
      layer_list = new_layer_list
    return new_layer_list

  def cost(self, inputs, expectation):
    outputs = self.run(inputs)
    cost = [None] * len(outputs)
    for i in range(len(outputs)):
      sub_cost = (expectation[i] - outputs[i]) ** 2
      cost[i] = sub_cost
    return cost

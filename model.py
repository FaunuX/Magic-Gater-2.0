import json
import random
import math
import evolve


def sigmoid(x):
  if x >= 0:
    z = math.exp(-x)
    sig = 1 / (1 + z)
    return sig
  else:
    z = math.exp(x)
    sig = z / (1 + z)
    return sig

commanders_list = json.loads(open('commanders.json').read())

unranked_commanders = []


def random_commander():
	random.shuffle(commanders_list)
	return commanders_list[:50]

class recommendationEngine:
  def __init__(self, color_preferences, type_preferences):
    self.model = evolve.Evolver([], [17, 8, 4, 1], [])
    self.color_preferences = color_preferences
    self.type_preferences = type_preferences


  def generate_commander_input(self, commander_data):
      data_input = [0] * 17
      layout_values = {'normal': 0, 'flip': 1, 'transform': 2, 'modal_dfc': 3, 'meld': 4, 'leveler': 5, 'reversible_card': 6}
      color_values = {'W': 10, 'U': 11, 'B': 12, 'R': 13, 'G': 14}
      data_input[layout_values[commander_data['layout']]] = 1
      data_input[7] = sigmoid(float(commander_data['cmc']))
      if 'creature' in commander_data['type_line'].split():
        if commander_data['power'] != '*':
          data_input[8] = sigmoid(float(commander_data['power']))
        if commander_data['toughness'] != '*':
          data_input[9] = sigmoid(float(commander_data['toughness']))
      if 'planeswalker' in commander_data['type_line'].split():
        if type(commander_data['loyalty']) == 'int':
          data_input[8] = sigmoid(float(commander_data['loyalty']))
          data_input[9] = sigmoid(float(commander_data['loyalty']))
        else:
          data_input[8] = 0
          data_input[9] = 0
      if len(commander_data['color_identity']) != 0:
        for color in commander_data['color_identity']:
          data_input[color_values[color]] = 1
        try:
          data_input[15] = sigmoid(float(commander_data['prices']['usd']))
        except:
          data_input[15] = sigmoid(float(commander_data['prices']['usd_foil']))
        if 'edhrec_rank' in commander_data:
          data_input[16] = 1 - sigmoid(commander_data['edhrec_rank'] / 2000)
        elif 'penny_rank' in commander_data:
          data_input[16] = 1 - sigmoid(commander_data['penny_rank'] / 2000)
      return data_input

  def generate_commander_score(self, commander_data):
    return self.model.model.run(self.generate_commander_input(commander_data))

  def cooked_data(self, commander_raw_data):
    commander_data = commander_raw_data
    bad_layouts = ['transform', 'reversible_card', 'modal_dfc']
    if commander_data['layout'] in bad_layouts:
      bad_attributes = ['prices', 'edhrec_rank', 'layout', 'color_identity', 'cmc']
      if 'edhrec_rank' in commander_data:
        bad_attributes.append('edhrec_rank')
      if 'penny_rank' in commander_data:
        bad_attributes.append('penny_rank')
      commander_data = commander_raw_data['card_faces'][0]
      for attribute in bad_attributes:
        commander_data[attribute] = commander_raw_data[attribute]
    return commander_data
          
    
    
  def compare_commanders(self, commanders):
    commander_values = []
    for commander in commanders:
      commander_values.append(self.generate_commander_score(self.cooked_data(commander)))
      return commanders[commander_values.index(max(commander_values))]
  
  def suggest_commander(self):
    cmdrs = random_commander()
    return self.compare_commanders(cmdrs)
      
  def commander_page(self, i):
    page_list = []
    while len(page_list) < i:
      next_card = self.suggest_commander()
      if not(next_card in page_list):
        page_list.append(next_card)
    return page_list
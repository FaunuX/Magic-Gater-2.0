import json
import random
import ast

commanders_list = json.loads(open('commanders.json').read())



def random_commander():
	random.shuffle(commanders_list)
	return commanders_list[0]





def generate_commander_score(color_preferences, commander_id, type_preferences, commander_creature_type):
  commander_type = commander_creature_type
  color_preferences = json.loads(color_preferences)
  total_colors = color_preferences['W'] + color_preferences['U'] + color_preferences['B'] + color_preferences['R'] + color_preferences['G']
  score = 0
  if len(commander_id) == 1:
    score = color_preferences[commander_id[0]] / (total_colors * 1.25)
  if len(commander_id) == 2:
    score = (color_preferences[commander_id[0]] + color_preferences[commander_id[1]]) / (total_colors * 1.5)
  if len(commander_id) == 3:
    score = (color_preferences[commander_id[0]] + color_preferences[commander_id[1]] + color_preferences[commander_id[2]]) / (total_colors * 1.75)
  if len(commander_id) == 4:
    score = (color_preferences[commander_id[0]] + color_preferences[commander_id[1]] + color_preferences[commander_id[2]] + color_preferences[commander_id[3]]) / (total_colors * 2.0)
  if len(commander_id) == 5:
    score = 4/9
  for type in type_preferences:
    if commander_type.find(type) != -1:
      score += 0.15
  return score




def compare_commanders(commander_1_data, commander_2_data, color_preferences, type_preferences):
  if generate_commander_score(color_preferences, commander_1_data['color_identity'], type_preferences, commander_1_data['type_line']) > generate_commander_score(color_preferences, commander_2_data['color_identity'], type_preferences, commander_2_data['type_line']):
    return commander_1_data
  else:
    return commander_2_data


def suggest_commander(color_preferences, type_preferences):
	return compare_commanders(
			compare_commanders(
				compare_commanders(
					random_commander(), 			
					random_commander(), 
					color_preferences,
          type_preferences),
				compare_commanders(
					random_commander(), 
					random_commander(), 
					color_preferences, 
          type_preferences),
				color_preferences, 
        type_preferences),
			compare_commanders(
				compare_commanders(
					random_commander(), 	
					random_commander(), 
					color_preferences, 
          type_preferences), 
				compare_commanders(
					random_commander(), 
					random_commander(), 
					color_preferences,
          type_preferences), 
				color_preferences, 
        type_preferences),
			color_preferences,
      type_preferences
		)



def commander_page(color_preferences, type_preferences):
  page_list = []
  while len(page_list) < 10:
	  next_card = suggest_commander(color_preferences, type_preferences)
	  if not(next_card in page_list):
		  page_list.append(next_card)
  return page_list
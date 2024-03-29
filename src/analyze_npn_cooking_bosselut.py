# analyze_npn_cooking_bosselut.py

import argparse
import glob
import json
import numpy as np
import os
import pandas as pd

from collections import defaultdict
from datetime import datetime


"""
Objective:

analyze 121K npn cooking files (json)

Currently, I want to analyze 'verb' value for number of FD-events
'ingredients' value for number of entities in each utt
'text' to get length of each file 

Common Keys:
1) 'split' - which dataset split the recipe belongs to
2) 'id' - a unique identifier for each recipe
3) 'verb' - a dictionary where each key is a step number in the recipe (e.g., '0' is the first step). The value is the list of verbs that occur in this step. If no verbs occur, there should be a "<NO_CHANGE>" included
4) 'ingredient_list' - a list of plain text words for each ingredient_name
5) 'ingredients' - a dictionary where each key is a step number in the recipe. Steps without ingredients don't have a key. The value is a list indices for the ingredients that occur in that step (the indices correspond to their location in ingredient_list)
6) 'events' - a dictionary where each key is a step number in the recipe. Steps without an event don't have a key. The value for each key is another dictionary. In this 2nd dictionary, each key is a state change type (i.e., composition, cookedness, etc.). The values in the second dictionary are the end states for each state change type. if a state change type does not exist in this step, the second dictionary does not have a key for it.
7) 'text' - a dictionary where each key is a step number in the recipe. Each value is a list of tokens for this step.

For "train" recipes, two additional keys are as follows (if needed):
1) 'ing_type' - a dictionary where each key is a step number in the recipe. The value is a number corresponding to what type of annotation the ingredients are ( 1 = mention annotation, 2 = coref annotation, 3 = no ingredients to be selected)
2) 'ingredients_nocoref' - the ingredients at each step without the coref rules to augment training data


"""

"""
Sample command line:

python3 analyze_npn_cooking_bosselut.py \
--recipes_path '/nfs/research/regan/src/data/cooking_dataset/recipes/'

"""


def analyze_recipes(path):

	cnt_files = 0
	
	all_cnt_utts = []
	all_cnt_tokens = []
	
	length_coref_chains_per_file = {}

	all_recipes_noun_counts = []
	all_vocab_verbs_fd_events = []


	os.chdir(path)

	for file in glob.glob("*.json"):

		length_utts = 0
		cnt_utts = 0

		# used as proxy for fd-entities
		cnt_vocab_nouns_from_ingredients = defaultdict(int)
		cnt_vocab_verbs_from_verbs = defaultdict(int)	

		with open(file, 'r') as f:

			cnt_files += 1

			data = json.load(f)

			# process length of all utts in 'text'
			text = data['text']

			for step, utt in text.items():

				length_utts += len(utt)
				cnt_utts += 1

			all_cnt_tokens.append(length_utts)
			all_cnt_utts.append(cnt_utts)


			ingredients = data['ingredients']

			for step, arr in ingredients.items():

				for ingred in arr:
					cnt_vocab_nouns_from_ingredients[ingred] += 1

			all_recipes_noun_counts.append(cnt_vocab_nouns_from_ingredients)


	print("Number of recipe files:", cnt_files)
	print("Mean number of tokens per file:", np.mean(all_cnt_tokens))
	print("Mean number of utts per file:", np.mean(all_cnt_utts))


	length_coref_all_fd_entities = []
	cnt_number_unique_fd_entities_per_recipe = []

	cnt_number_total_fd_entities_per_recipe = []

	for recipe_noun_count in all_recipes_noun_counts:

		cnt_number_unique_fd_entities_per_recipe.append(len(recipe_noun_count))


		
		# each recipe is a defaultdict count the number of entities and their frequencies

		this_recipe_coref = []
		total_count_fd_entities = 0
		for ingred, count in recipe_noun_count.items():
			this_recipe_coref.append(count)

			total_count_fd_entities += count

		cnt_number_total_fd_entities_per_recipe.append(total_count_fd_entities)

		if len(this_recipe_coref) > 0:
			length_coref_all_fd_entities.append(np.mean(this_recipe_coref))


	print("Mean number of unique fd-entities per file:", np.mean(cnt_number_unique_fd_entities_per_recipe))
	print("Mean number of total fd-entities per file:", np.mean(cnt_number_total_fd_entities_per_recipe))
	print("Mean length coref chain per file:", np.mean(length_coref_all_fd_entities))


	# print("Number of total verbs:", len(all_verbs))
	# print("Number of total nouns:", len(all_nouns))

	
	
	# print("Mean count of all entities per file:", np.mean(cnt_all_entities_per_file))
	

	





def main():

	parser = argparse.ArgumentParser(description='analysis of NPN recipes dataset')
	parser.add_argument('--recipes_path', required=True, type=os.path.abspath,
						help='path to directory of json files') 
	# parser.add_argument('--write_path', required=True, type=os.path.abspath,
	# 					help='path to write next version of propara data (currently v6)') 

	opt = parser.parse_args()
	print()
	print(opt)
	print()

	d = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
	print(d)
	print()
	print("Analysing NPN recipes dataset (121K json files)")
	print()

	analyze_recipes(opt.recipes_path)




		






if __name__ == '__main__':
	main()


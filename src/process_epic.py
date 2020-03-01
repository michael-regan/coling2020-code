# process_epic.py

import argparse
import csv
import numpy as np
import os
import pandas as pd

from collections import defaultdict
from datetime import datetime


"""
Objective:

columns in epic_narration.csv
participant_id,video_id,start_timestamp,stop_timestamp,narration

columns in epic_train_action_labels.csv
uid,participant_id,video_id,narration,start_timestamp,stop_timestamp,start_frame,stop_frame,verb,verb_class,noun,noun_class,all_nouns,all_noun_classes


"""

"""
Sample command line:

python3 process_epic.py \
--epic_narration_path '../data/epic_train_action_labels.csv'

"""


def read_epics(path):

	df = pd.read_csv(path)

	all_video_ids = []
	all_verbs = []
	all_nouns = []

	all_narration_lengths = []

	# grouping by narration so to count number coref chains
	coref_grouped_by_narration = {}

	length_files = defaultdict(int)

	for idx, row in df.iterrows():

		video_id = row.video_id
		verb = row.verb
		noun = row.noun
		narration = row.narration

		all_narration_lengths.append(len(narration.split()))

		if video_id not in coref_grouped_by_narration:
			coref_grouped_by_narration[video_id] = defaultdict(int)

		length_files[video_id] += 1

		all_video_ids.append(video_id)
		all_verbs.append(verb)
		all_nouns.append(noun)

		coref_grouped_by_narration[video_id][noun] += 1



	all_video_ids = list(set(all_video_ids))
	all_verbs = list(set(all_verbs))
	all_nouns = list(set(all_nouns))

	print("Number of video files:", len(all_video_ids))
	print("Number of total verbs:", len(all_verbs))
	print("Number of total nouns:", len(all_nouns))

	length_coref = []

	num_entities_per_file = []

	for k, v in coref_grouped_by_narration.items():
		for key, num_coref in v.items():
			length_coref.append(num_coref)
		num_entities_per_file.append(len(v))

	print("Mean length coref chain per file:", np.mean(length_coref))
	print("Mean number of entities per file:", np.mean(num_entities_per_file))
	print("Mean number of tokens per file:", np.mean(all_narration_lengths))


	all_lengths_files = []

	for k, v in length_files.items():
		all_lengths_files.append(v)

	print("Mean number of utts per file:", np.mean(all_lengths_files))





def main():

	parser = argparse.ArgumentParser(description='analysis of EPIC recipes data')
	parser.add_argument('--epic_narration_path', required=True, type=os.path.abspath,
						help='path to json file of corrected dependency trees') 
	# parser.add_argument('--write_path', required=True, type=os.path.abspath,
	# 					help='path to write next version of propara data (currently v6)') 

	opt = parser.parse_args()
	print()
	print(opt)
	print()

	d = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
	print(d)
	print()
	print("Analysing EPICs Recipes data (counting entities and actions)")
	print()

	read_epics(opt.epic_narration_path)




		






if __name__ == '__main__':
	main()


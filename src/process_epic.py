# process_epic.py

import argparse
import csv
import os
import pandas as pd

from collections import defaultdict
from datetime import datetime
from stanfordcorenlp import StanfordCoreNLP



"""
Objective:

columns in epic_narration.csv
participant_id,video_id,start_timestamp,stop_timestamp,narration


"""

"""
Sample command line:

python3 process_epic.py \
--epic_narration_path '../data/epic_training.csv'

"""


class StanfordNLP:

	def __init__(self, host='http://localhost', port=8888):
		self.nlp = StanfordCoreNLP(host, port=port, timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
		self.props = {
			'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
			'pipelineLanguage': 'en',
			'outputFormat': 'json'
			}

	def word_tokenize(self, sentence):
		return self.nlp.word_tokenize(sentence)
		
	def pos(self, sentence):
		return self.nlp.pos_tag(sentence)

	def ner(self, sentence):
		return self.nlp.ner(sentence)

	def parse(self, sentence):
		return self.nlp.parse(sentence)

	def dependency_parse(self, sentence):
		return self.nlp.dependency_parse(sentence)

	def annotate(self, sentence):
		return json.loads(self.nlp.annotate(sentence, properties=self.props))
	
	@staticmethod
	def tokens_to_dict(_tokens):
		tokens = defaultdict(dict)
		for token in _tokens:
			tokens[int(token['index'])] = {
				'word': token['word'],
				'lemma': token['lemma'],
				'pos': token['pos'],
				'ner': token['ner']
				}
		return tokens




def read_epics(path):

	df = pd.read_csv(path)

	all_video_ids = []

	for idx, row in df.iterrows():

		video_id = row.video_id
		narr = row.narration

		if video_id not in all_video_ids:
			all_video_ids.append(video_id)

	print("Number of video files:", len(all_video_ids))




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


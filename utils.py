import json
from nltk.tokenize import word_tokenize
import pandas as pd

def makeVocab():
	fpr = open("/home/sayali/CS726/Project/train.txt", 'r')
	vocab = {}
	ivocab = {}
	count = 1
	for line in fpr:
		qas = line.split('\t')
		for j in range(2):
			q_words = qas[j].split(' ')
			print q_words
			for i in range(len(q_words)):
				if q_words[i] not in vocab.keys():
					vocab[q_words[i]] = count
					ivocab[count] = q_words[i]
					count = count + 1

		# print "vocab"
		# for k,v in vocab.items():
		# 	print str(k)+"--"+str(v)

		# print "ivocab"
		# for k,v in ivocab.items():
		# 	print str(k)+"--"+str(v)	

	df = pd.DataFrame(vocab.items())
	print df
	df.to_pickle('vocab.pkl')

	df1 = pd.DataFrame(ivocab.items())
	print df1
	df1.to_pickle('ivocab.pkl')
		
makeVocab()
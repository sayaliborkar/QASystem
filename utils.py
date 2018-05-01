import json
from nltk.tokenize import word_tokenize
import pandas as pd
import torch

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

def vocabToEmbed():
	#gloveDF = pd.read_csv("/home/sayali/CS726/Project/data/glove.840B.300d.txt", sep=" ")
	#print gloveDF
	#gloveDF.to_pickle('/data/glove.pkl')
	df = pd.read_pickle('/home/sayali/CS726/Project/data/vocab.pkl')
	df.columns = ['word','id']
	#print df

	#emb = torch.FloatTensor(df.shape[0]+1,300)
	#print emb
	#torch.save(emb,'embedding')
	emb = torch.load('embedding')
	c = 0
	fp = open("/home/sayali/CS726/Project/data/glove.840B.300d.txt",'r')
	fw = open("/home/sayali/CS726/Project/data/error.txt",'w')
	for line in fp:
		vec = line.split(' ')
		try:
			df1 = df[df['word'].str.match(vec[0]+"$")]
		except:
			fw.write(line)
			continue

		print df1
		print vec[0]
		if not df1.empty :
			
			for i in range(1,301):
				try:
					emb[int(df1['id'])][i-1] = float(vec[i])
				except:
					fw.write(line)
					break		
		
	print emb
	torch.save(emb,'embedding')

def buildData():
	fp = open("/home/sayali/CS726/Project/data/train.txt",'r')
	df = pd.read_pickle('/home/sayali/CS726/Project/data/vocab.pkl')
	df.columns = ['word','id']
	df1 = df.set_index('word')

	count = 0
	data = pd.DataFrame(columns=['context','question','answer'])
	for line in fp:
		qas = line.split('\t')

		words = qas[0].split(' ')
		c = torch.IntTensor(len(words))
		for i in range(len(words)):
			#print df1.get_value(words[i], 'id')
			c[i] = int(df1.get_value(words[i], 'id'))
		#print c

		words = qas[1].split(' ')
		q = torch.IntTensor(len(words))
		for i in range(len(words)):
			#print df1.get_value(words[i], 'id')
			q[i] = int(df1.get_value(words[i], 'id'))
		#print q

		pos = qas[2].split(' ')
		p = torch.IntTensor(len(pos)+1)
		for i in range(len(pos)):
			#print df1.get_value(words[i], 'id')
			p[i] = int(pos[i])
		p[len(pos)] = int(len(c)+1)
		print p

		data = data.append({'context':c,'question':q,'answer':p},ignore_index=True)
		# print data.loc[0]
		# count = count + 1
		# if count==3:
		# 	break
	data.to_pickle('data.pkl')

#makeVocab()
#vocabToEmbed()
buildData()
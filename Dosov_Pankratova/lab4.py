import pandas as pd
import numpy as np
import nltk
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

file = open('C:\\Users\\sanjar\\Desktop\\mycorpus.txt', 'r', errors = 'ignore') # загрузка данных
raw=file.read()
raw=raw.lower() 
#nltk.download('punkt')
#nltk.download('wordnet') 
sent_tokens = nltk.sent_tokenize(raw) 
word_tokens = nltk.word_tokenize(raw) 
lemmer = nltk.stem.WordNetLemmatizer()

def LenTokens(tokens):
	return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
	return LenTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
	
GREETING_INPUTS = ("PMIdor15",)
GREETING_RESPONSES = ["Hello topus - octopus"]	

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
	robo_response = ''
	sent_tokens.append(user_response)
	TFidfVec = TfidfVectorizer(tokenizer = LemNormalize, stop_words = 'english')
	tfidf = TFidfVec.fit_transform(sent_tokens)
	vals = cosine_similarity(tfidf[-1], tfidf)
	idx = vals.argsort()[0][-2]
	flat = vals.flatten()
	flat.sort()
	req_tfidf = flat[-2]
	if(req_tfidf == 0):
		robo_response = robo_response + 'ПРОСТИТЕ. НО я ГЛУПИЙ ЧТОБЫ ПОНЯТЬ ЧТО ВЫ НАПИСАЛИ! плак-плак-плак'
		return robo_response
	else:
		robo_response = robo_response + sent_tokens[idx]
		return robo_response
	
flag = True
print("Введите то, что хотите найти.\n")
while(flag == True):
	user_response = input("Вы: ")
	user_response = user_response.lower()
	if(user_response!='bye'):
		if(user_response == 'thanks' or user_response == 'thank you'):
			flag=False
			print("You are welcome... Bye")
		else:
			if(greeting(user_response) != None):
				print("\n" + greeting(user_response))
			else:
				print("\n", end="")
				print(response(user_response))
				sent_tokens.remove(user_response)
	else:
		flag = False
		print("Bye")
	

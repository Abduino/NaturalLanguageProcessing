import sys
import nltk
from nltk.corpus import stopwords
import unicodedata
from nltk import word_tokenize,sent_tokenize, pos_tag
import re
import codecs
import gensim
import numpy as np

from gensim import models, matutils, similarities
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.parsing.preprocessing import remove_stopwords
from gensim.similarities.docsim import MatrixSimilarity
#Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
#%matplotlib inline
import os
## Setup mallet environment change it according to your drive
os.environ.update({'MALLET_HOME':r'C:/mallet-2.0.8'})
## Setup mallet path change it according to your drive
mallet_path = 'C:/mallet-2.0.8/bin/mallet'
#mallet_path = 'mallet-2.0.8/bin/mallet'

stop_word = "stop_words_amharic.txt"
stop_words = codecs.open(stop_word,"r","utf-8").read()
stop_words=re.sub(u'[\r\n]', '',stop_words)
stop_words_amharic = re.split(u'[ ]', stop_words)

def clean_doc(text):
    print("********** Preprocess the document ************")
    documents = re.split(u'[።]', text)
    #documents = [s for s in nltk.tokenize.sent_tokenize(text)]
    #tokenized_list = [simple_preprocess(doc) for doc in documents]
    #print(tokenized_list)
    tokens= [[word for word in simple_preprocess(str(doc)) if word not in stop_words_amharic] for doc in documents]
    print("len of doc is = ", len(documents))
    return tokens

def create_corpus_normal(tokens):
    print("******** Create normal lda corpus ************")
    id2word =corpora.Dictionary(tokens)
    mycorpus= [id2word.doc2bow(doc,allow_update=True) for doc in tokens]
    print("len of doc is = ", len(mycorpus))
    print("len of word is = ", len(id2word))
    return id2word,mycorpus

def create_corpus_tfidf(tokens):
    print("******** Create tf-idf corpus ************")
    id2word =corpora.Dictionary(tokens)
    mytfidf_corpus=[id2word.doc2bow(doc,allow_update=True) for doc in tokens]
    tfidf_model=models.TfidfModel(mytfidf_corpus)
    corpus_tfidf=tfidf_model[mytfidf_corpus]
    return id2word,corpus_tfidf
    


file_name = "2.txt"
text = codecs.open(file_name,"r","utf-8").read()
text=re.sub(u'[\n\r()!?፣]', '',text)
stop_words=re.sub(u'[\r\n]', '',stop_words)
tokens = clean_doc(text)

id2word, corpus = create_corpus_normal(tokens)

model_list, perplex_values, cv = compute_coherence_values_PL(dictionary=id2word, corpus=corpus, texts=tokens, start=2, limit=40, step=1)


#ldamodel = gensim.models.ldamodel.LdaModel.load('models/LDA_N_10topics')
#print(ldamodel.get_document_topics(id2word))
#from gensim.summarization import summarize, keywords
#from pprint import pprint
#d="Data/bbc/politics/009.txt"
#text = " ".join((line for line in smart_open('d', encoding='utf-8')))

# Summarize the paragraph

#pprint(summarize(text,ratio=0.5))
#> ('the PLA Rocket Force national defense science and technology experts panel, '
#>  'according to a report published by the')

# Important keywords from the paragraph
#print(keywords(text))
#> force zhang technology experts pla rocket


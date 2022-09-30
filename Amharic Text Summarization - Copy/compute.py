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
PUNCT_TRANSLATE_UNICODE = dict.fromkeys((i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith("P")),"",)


stop_word = "stop_words_amharic.txt"
stop_words = codecs.open(stop_word,"r","utf-8").read()
stop_words=re.sub(u'[\r\n]', '',stop_words)
stop_words_amharic = re.split(u'[ ]', stop_words)
def clean_doc(text):
    print("********** Preprocess the document ************")
    documents = re.split(u'[።]', text)
    tokens= [[word for word in simple_preprocess(str(doc)) if word not in stop_words_amharic] for doc in documents]
    print("len of doc is = ", len(documents))
    
    return tokens,documents

def create_corpus_normal(tokens):
    print("******** Create normal lda corpus ************")
    id2word =corpora.Dictionary(tokens)
    mycorpus= [id2word.doc2bow(doc,allow_update=True) for doc in tokens]
    print("len of doc is = ", len(mycorpus))
    print("len of word is = ", len(id2word))
    return id2word,mycorpus
    


file_name = "2.txt"
text = codecs.open(file_name,"r","utf-8").read()
text=re.sub(u'[\n\r()!?፣]', '',text)
stop_words=re.sub(u'[\r\n]', '',stop_words)

tokens = clean_doc(text)
id2word, corpus = create_corpus_normal(tokens)



ldamodel = gensim.models.ldamodel.LdaModel.load('models/lda_normal/LDA_N_10topics')
topics=ldamodel.get_topic_terms(0)
print(topics)
for i in topics:
    print


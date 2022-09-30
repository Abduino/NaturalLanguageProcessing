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
    print(documents)
    tokens= [[word for word in simple_preprocess(str(doc)) if word not in stop_words_amharic] for doc in documents]
    print("len of doc is = ", len(documents))
    tokens.remove(tokens[27])
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
    
def compute_coherence_values_PL(dictionary, corpus, texts, limit, start=2, step=1):
    coherence_values = []
    perplex_values = []
    ##
    model_list = []
    for num_topics in range(start, limit, step):
        #ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=num_topics,random_state=100,passes=10)
        model_list.append(lda_model)
        coherencemodel = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='u_mass', topn=20)
        coherence_values.append(coherencemodel.get_coherence())
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()
    for m, cv in zip(x, coherence_values):
        print("Num Topics =", m, " has Coherence Value of", round(cv, 4))
    return model_list,perplex_values, coherence_values
def compute_coherence_values_NL(dictionary, corpus, texts, limit, start=2, step=1):
    coherence_values = []
    perplex_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        lda_model_tfidf = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=num_topics,random_state=100,passes=10)
        model_list.append(lda_model_tfidf)

        coherencemodel = CoherenceModel(model=lda_model_tfidf, texts=texts, dictionary=dictionary, coherence='u_mass')
        coherence_values.append(coherencemodel.get_coherence())
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()


    return model_list,perplex_values#, coherence_values

#cv_score = 'file_score/file_data.txt'
file_name = "TEST_Doc1.txt"
text = codecs.open(file_name,"r","utf-8").read()
print(text)
text=re.sub(u'[\n\r()!?፣]', '',text)
print(text)
tokens = clean_doc(text)
print(tokens)

id2word, corpus = create_corpus_normal(tokens)
model_list, perplex_values, cv = compute_coherence_values_PL(dictionary=id2word, corpus=corpus, texts=tokens, start=2, limit=20, step=1)

id2word, corpus = create_corpus_tfidf(tokens)
model_list, perplex_values, cv = compute_coherence_values_NL(dictionary=id2word, corpus=corpus, texts=tokens, start=2, limit=20, step=1)
'''
#ldamodel.save('LDA_NYT')
##
## Train LDA with mallet
#ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=8, id2word=id2word)
#coherence_model_lda = gensim.models.CoherenceModel(model=ldamallet, texts=tokens, dictionary=id2word, coherence='u_mass')
#coherence_lda = coherence_model_lda.get_coherence()
#print('\nCoherence Score: ', coherence_lda)

#print(ldamodel.get_document_topics(corpus_new))

#optimal_model = model_list[3]
#model_topics = optimal_model.show_topics(formatted=False)
#pprint(optimal_model.print_topics(num_words=10))
##for i in cv:
##    print(i)


NUM_TOPICS = 8

ldamodel.save('LDA_NYT')
# Loading trained model
ldamodel = gensim.models.ldamodel.LdaModel.load('LDA_NYT')
## Print time taken to train the model
print("--- %s seconds ---" % (time.time() - start_time))

'''

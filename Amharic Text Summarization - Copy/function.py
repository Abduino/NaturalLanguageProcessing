import sys
import nltk
from nltk.corpus import stopwords
import unicodedata
from nltk import word_tokenize,sent_tokenize, pos_tag
# Sklearn
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from pprint import pprint
#from ginsim import corpora
import codecs
import numpy as np
import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
from gensim import models, matutils, similarities
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.parsing.preprocessing import remove_stopwords
from gensim.similarities.docsim import MatrixSimilarity
#Plotting tools
import re
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
#%matplotlib inline

mallet_path = 'mallet-2.0.8/bin/mallet'
PUNCT_TRANSLATE_UNICODE = dict.fromkeys((i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith("P")),"",)
en_stop = stopwords.words('english')
keywords=10
stop_word = "stop_words_amharic.txt"
stop_words = codecs.open(stop_word,"r","utf-8").read()
stop_words=re.sub(u'[\r\n]', '',stop_words)
stop_words_amharic = re.split(u'[ ]', stop_words)
def clean_doc(text):
    print("********** Preprocess the document ************")
    documents = re.split(u'[።]', text)
    tokens= [[word for word in simple_preprocess(str(doc)) if word not in stop_words_amharic] for doc in documents]
    tokens.remove(tokens[27])
    return tokens,documents

def create_corpus_normal(tokens):
    print("******** Create normal lda corpus ************")
    id2word =corpora.Dictionary(tokens)
    mycorpus= [id2word.doc2bow(doc,allow_update=True) for doc in tokens]
    return id2word,mycorpus



def create_corpus_tfidf(tokens):
    print("******** Create tf-idf corpus ************")
    id2word =corpora.Dictionary(tokens)
    mytfidf_corpus=[id2word.doc2bow(doc,allow_update=True) for doc in tokens]
    tfidf_model=models.TfidfModel(mytfidf_corpus)
    corpus_tfidf=tfidf_model[mytfidf_corpus]
    return id2word,corpus_tfidf
    



#===========================BASED ON KEYWORD AND TOPICS
def prepare__topic_keywords_matrix(lda_model,id2word):
    topic_keyword_by_num = pd.DataFrame()
    topic_keyword_by_probdis = pd.DataFrame()
    topic_keyword_by_word = pd.DataFrame()
    for i in range(len(lda_model.print_topics())):
        topicid = i
        topic = lda_model.get_topics()[topicid]
        topic = topic / topic.sum()
        topn = 10
        bestn = matutils.argsort(topic, topn, reverse=True)
        
        top = [(idx, topic[idx]) for idx in bestn]

        list1 =[]
        list2 =[]
        list3 =[]
        for i in range(0,topn):
            list1.append(bestn[i])
            list2.append(top[i][1])
            list3.append(id2word[bestn[i]])
        topic_keyword_by_num = topic_keyword_by_num.append(pd.Series(list1), ignore_index=True)
        topic_keyword_by_word = topic_keyword_by_word.append(pd.Series(list3), ignore_index=True)
        topic_keyword_by_probdis = topic_keyword_by_probdis.append(pd.Series(list2), ignore_index=True)
        topic_keyword_by_num = topic_keyword_by_num.astype('int64')
    return topic_keyword_by_num,topic_keyword_by_word,topic_keyword_by_probdis

def get_keyword_count(topic_keyword_by_num,id2word):
    list6=np.unique(topic_keyword_by_num, return_counts=True)
    topic_keyword_by_num8 = pd.DataFrame(data=list6)
    topic_keyword_by_num8= topic_keyword_by_num8.T
    topic_keyword_by_num8.columns = ['uniqs','counts']
    topic_keyword_by_num8=topic_keyword_by_num8.sort_values('counts',ascending=[0])
    term_id = topic_keyword_by_num8.iloc[:keywords,0:0].index
    word = []
    for i in range(len(term_id)):
        word.append(id2word[term_id[i]])
    return word
def get_keyword_colrow_wise(topic_keyword_by_word,lda_model):
    array_topic_keyword_num = np.array(topic_keyword_by_word)
    keytop = int(keywords/len(lda_model.print_topics()))
    term1=[]
    for i in range(0,9):
        for j in range(0,3):
            unique1, countd = np.unique(term1, return_counts=True)
            if len(unique1) == keywords:
                break
            else:
                term1.append(array_topic_keyword_num[i][j])
    term2=[]
    for i in range(0,9):
        for j in range(0,3):
            
            unique2, countd = np.unique(term2, return_counts=True)
            if len(unique2) == keywords:
                break
            else:
                term2.append(array_topic_keyword_num[j][i])
                
    return unique1,unique2
       
def get_keywords_dominant(topic_keyword_by_probdis,id2word):
    array_topic_keyword_num = np.array(topic_keyword_by_probdis)
    term40=[]
    for i in range(len(id2word)):
        result = np.where(array_topic_keyword_num == np.amax(array_topic_keyword_num))
        listOfCordinates = list(zip(result[0], result[1]))
        for cord in listOfCordinates:
            term40.append(cord[1])
        array_topic_keyword_num[result]=0
        unique2, countd = np.unique(term40, return_counts=True)
        if len(unique2) == keywords:
            break

    list_keyword_1=[]
    for i in range(len(unique2)):
        list_keyword_1.append(id2word[unique2[i]])

    return list_keyword_1


def get_keywords_app4(lda_model,id2word):
    #************************APP 4
    list2=[]
    for i in range(len(id2word)):
        wor=lda_model.get_term_topics(i, minimum_probability=0)
        list1=[]
        for j in wor:
            list1.append(j[1])
        list2.append(list1)
    sent_topics_dfarray = pd.DataFrame(data=list2)
    sent_topics_dfarray_Rsum = pd.DataFrame()
    sent_topics_dfarray_Rsum = sent_topics_dfarray.T
    sent = pd.DataFrame(data=list2)
    sent_topics_dfarray.loc[:,'C_sum'] = sent_topics_dfarray.sum(numeric_only = True,axis=1)
    sorted_sent_topics_dfarray = pd.DataFrame()
    sorted_sent_topics_dfarray = sent_topics_dfarray.sort_values('C_sum',ascending=[0])
    term_id = sorted_sent_topics_dfarray.iloc[:keywords,0:0].index
    list_keyword_1=[]
    for i in range(len(term_id)):
        list_keyword_1.append(id2word[term_id[i]])

 
    sent_topics_dfarray_Rsum.loc[:,'C_sum'] = sent_topics_dfarray_Rsum.sum(numeric_only = True,axis=1)
    sorted_sent_topics_dfarray_Rsum = pd.DataFrame()
    sorted_sent_topics_dfarray_Rsum = sent_topics_dfarray_Rsum.sort_values('C_sum',ascending=[0])
    dom_topic_list = sorted_sent_topics_dfarray_Rsum[0].index
    dom_topic = dom_topic_list[0]

    last=len(id2word)
    term_id2= sorted_sent_topics_dfarray_Rsum.iloc[0:1,0:last]
    term_id2 = term_id2.T
    term_id2.columns=['Key0']
    term_id2 = term_id2.sort_values('Key0',ascending=[0])
    term_id3 = term_id2.iloc[:keywords,0:0].index
    list_keyword_2 = []
    for i in range(len(term_id3)):
        list_keyword_2.append(id2word[term_id3[i]])

    return dom_topic_list,dom_topic,list_keyword_1,list_keyword_2


def get_topic_keywords(lda_model,id2word,topic_id):

    topic = lda_model.get_topics()[topic_id]
    topn = 10
    bestn = matutils.argsort(topic, topn, reverse=True)
    top = [(idx, topic[idx]) for idx in bestn]
    list3 =[]
    for i in range(0,topn):
        list3.append(id2word[bestn[i]])

    return list3




def get_dominant_topics(doc_topic_distribution):
    num_topics = 10
    list2=[]
    for i in doc_topic_distribution:
        list1=[]
        for j in range(len(i)):
            list1.append(i[j][1])
        list2.append(list1)
        
    sent_by_topic = pd.DataFrame(data=list2)
    sentence_by_topic_matrix = pd.DataFrame(data=list2)

    topic_by_sent = pd.DataFrame()
    topic_by_sent = sent_by_topic.T
    column_sum_of_weights = np.sum(topic_by_sent, axis=1)
    dom_topic = sent_by_topic.idxmax(axis=1)


    sorted_weight_indices = np.argsort(column_sum_of_weights)
    idx = np.arange(num_topics-num_topics, num_topics)
    dominant_topic_ids = sorted_weight_indices[idx]
    dominant_topic_ids = dominant_topic_ids[::-1]
    dom_topic_bysum=dominant_topic_ids.tolist()
    num1 = dom_topic_bysum[0]

    topic_counts = dom_topic.value_counts()
    dom_topic_by_count = topic_counts.index.tolist()
    num2 = dom_topic_by_count[0]

    return dom_topic_bysum,num1,dom_topic_by_count,num2,sentence_by_topic_matrix

def get_dominant_sentence_idx(sentences,sent_by_topic,num):
    num_sent=sentences
    sorted_sentences = sent_by_topic[num]
    sorted_sentences = np.argsort(sorted_sentences)
    sent_idx = np.arange(num_sent-num_sent, num_sent)
    dominant_sentence_ids = sorted_sentences[sent_idx]
    dominant_sentence_ids = dominant_sentence_ids[::-1]
    dominant_sentence=dominant_sentence_ids.tolist()
    return dominant_sentence

def get_dominant_sentence_fromall_topics(sentences,sent_by_topic):
    num_sent=sentences -1
    array_topic_keyword_num = np.array(sent_by_topic)
    dominant_sent_from_alltopics=[]
    for i in range(0,num_sent):
        result = np.where(array_topic_keyword_num == np.amax(array_topic_keyword_num))
        listOfCordinates = list(zip(result[0], result[1]))
        for cord in listOfCordinates:
            dominant_sent_from_alltopics.append(cord[0])
        array_topic_keyword_num[result]=0
    return dominant_sent_from_alltopics

def get_dominant_sentence_from_topicsSum(corpus, lda,num_sent):
    inference = lda.inference(corpus)
    inference = inference[0] # the inference is a tuple, need the first term
    num_topics = num_sent
    column_sum_of_weights = np.sum(inference, axis=1)
    sorted_weight_indices = np.argsort(column_sum_of_weights)
    idx = np.arange(num_topics - num_topics, num_topics)
    dominant_topic_ids = sorted_weight_indices[idx]
    dominant_topic_ids = dominant_topic_ids[::-1]
    return dominant_topic_ids.tolist()


#=========================================SUMMARIZATION SCORE

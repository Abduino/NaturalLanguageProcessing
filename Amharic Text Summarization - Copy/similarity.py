import gensim
import jieba
import nltk
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from gensim import corpora, models, similarities

from nltk.tokenize import word_tokenize, sent_tokenize

def get_similarity(dictionary,corpus,tokenized_sentences,sent):
    len_sent=len(tokenized_sentences)
    def similar(tokens_a, tokens_b):
        ratio = len(set(tokens_a).intersection(tokens_b))/ float(len(set(tokens_a).union(tokens_b)))
        return ratio


    scores_1 = []
    for sentence in tokenized_sentences :
        score = 0;
        score += similar(sentence,sent)
        scores_1.append(score)

    scores_2 = []
    for sentence in tokenized_sentences :
        reference = [sentence]
        candidate = sent
        score = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0))
        scores_2.append(score)
        
    feature_cnt = len(dictionary.token2id)
    tfidf = models.TfidfModel(corpus)
    kw_vector = dictionary.doc2bow(sent)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
    scores_3 = index[tfidf[kw_vector]]


    scores_4 = []
    for sentence in tokenized_sentences :
        X_set = set(sentence) 
        Y_set = set(sent)
        rvector = X_set.union(Y_set)  
        l1=[]
        l2=[]
        for w in rvector: 
            if w in X_set: l1.append(1) # create a vector 
            else: l1.append(0) 
            if w in Y_set: l2.append(1) 
            else: l2.append(0) 
        c = 2
        for i in range(len(rvector)): 

                c+= l1[i]*l2[i] 

        cosine = c / float((sum(l1)*sum(l2))**0.5)
        scores_4.append(cosine)
    all_scores = []
    all_scores.append(scores_1)
    all_scores.append(scores_2)
    all_scores.append(scores_3)
    all_scores.append(scores_4)
    def get_sorted_sentences(topic_by_sent):
        column_sum_of_weights = np.sum(topic_by_sent, axis=0)
        sorted_weight_indices = np.argsort(column_sum_of_weights)
        idx = np.arange(len_sent-len_sent, len_sent)
        dominant_topic_ids = sorted_weight_indices[idx]
        dominant_topic_ids = dominant_topic_ids[::-1]
        dom_topic_bysum=dominant_topic_ids.tolist()
        return dom_topic_bysum
    
    topic_by_sent = pd.DataFrame(data=scores_1)
    soretd_sentences = get_sorted_sentences(topic_by_sent)
    '''
    def get_sorted_sentences(topic_by_sent):
        column_sum_of_weights = np.sum(topic_by_sent, axis=0)
        sorted_weight_indices = np.argsort(column_sum_of_weights)
        idx = np.arange(len_sent-len_sent, len_sent)
        dominant_topic_ids = sorted_weight_indices[idx]
        dominant_topic_ids = dominant_topic_ids[::-1]
        dom_topic_bysum=dominant_topic_ids.tolist()
        return dom_topic_bysum
    
    topic_by_sent = pd.DataFrame(data=all_scores)
    soretd_sentences = get_sorted_sentences(topic_by_sent)
    '''
    return topic_by_sent,soretd_sentences

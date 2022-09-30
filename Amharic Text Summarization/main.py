import codecs
import re
import pandas as pd
import function as fun
import similarity as sim
#import roguetest as rg
import gensim
import numpy as np
from gensim import models, matutils, similarities
from gensim.models import CoherenceModel
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)



file_name = "TEST_Doc1.txt"
text = codecs.open(file_name,"r","utf-8").read()
text=re.sub(u'[\n\r()!?፣]','',text)

tokens,tokenized_list = fun.clean_doc(text)
id2word, corpus = fun.create_corpus_normal(tokens)
num_topics = 10
len_sentences=len(tokenized_list)-1



lda_model_normal = gensim.models.ldamodel.LdaModel.load('models/lda_normal/LDA_N_10topics')


#lda_model_normal = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=id2word,num_topics=num_topics,iterations=0)

doc_topic_distribution = lda_model_normal.get_document_topics(corpus, minimum_probability=0, minimum_phi_value=None, per_word_topics=False)
dom_topic_bysum,num1,dom_topic_by_count,num2,sentence_by_topic_matrix = fun.get_dominant_topics(doc_topic_distribution)



topic_keyword_by_num,topic_keyword_by_word,topic_keyword_by_probdis = fun.prepare__topic_keywords_matrix(lda_model_normal,id2word)

keywords_0 = fun.get_keyword_count(topic_keyword_by_num,id2word)
keywords_1,keywords_2 = fun.get_keyword_colrow_wise(topic_keyword_by_word,lda_model_normal)
keywords_3 = fun.get_keywords_dominant(topic_keyword_by_probdis,id2word)
dom_topic_list,dom_topic,keywords_4,keywords_5 = fun.get_keywords_app4(lda_model_normal,id2word)




print("DOMINANT TOPIC <DTSA_1 > ",dom_topic_list,"=>",dom_topic)
print("DOMINANT TOPIC <DTSA_2 > ",dom_topic_bysum,"=>",num1)
print("DOMINANT TOPIC <DTSA_3 > ",dom_topic_by_count,"=>",num2)
print("=======================================================================")



dominant_sent_from_alltopics = fun.get_dominant_sentence_fromall_topics(len_sentences,sentence_by_topic_matrix)
dominant_sentence_topicSum = fun.get_dominant_sentence_from_topicsSum(corpus,lda_model_normal,len_sentences)




#==============================based on coherance value

topn = lda_model_normal.top_topics(corpus=corpus, texts=tokens, dictionary=id2word, window_size=None,coherence='u_mass', topn=10, processes=-1)

print("££££££££££££££££££££££££££££££££££££££££££££££££££")
topic_keywords_cv = topn[1][0]
keywords_6=[]
for i in range(0,10):
    keywords_6.append(topic_keywords_cv[i][1])
print(keywords_6)

topic = lda_model_normal.show_topics()
str_topics = []
str_topics_only_id = []
for i in topic:
    str_topics.append(i)
    str_topics_only_id.append(i[0])
cm = CoherenceModel(model=lda_model_normal, corpus=corpus, texts=tokens, dictionary=id2word,window_size=None, coherence='u_mass', topn=10,processes=-1)
coherence_scores = cm.get_coherence_per_topic()
scored_topics = zip(str_topics, coherence_scores)
sorted_topics_cv = sorted(scored_topics, key=lambda tup: tup[1], reverse=True)
scored_topics_only_id = zip(str_topics_only_id, coherence_scores)
sorted_topics_cv_only_id = sorted(scored_topics_only_id, key=lambda tup: tup[1], reverse=True)
top_list=[]
for i in sorted_topics_cv_only_id:
    top_list.append(i[0])
    

num3=top_list[0]
#rg.make_rouge(sentences)




#================ KEYWORDS SELECTION ================================
print("================= KEYWORDS APPROACH ===============")
print("ABKS_1 KEYWORDS = " ,keywords_0)
print("ABKS_2_A KEYWORDS = " ,keywords_1)
print("ABKS_2_B KEYWORDS = " ,keywords_2)
print("ABKS_3 KEYWORDS = " ,keywords_3)
print("ABKS_4 KEYWORDS = " ,keywords_4)
print("ABKS_5 KEYWORDS = " ,keywords_5)
print("ABKS_6 KEYWORDS = " ,keywords_6) #from dominant topic
print("=======================================================================")


all_sentence_scores_ABKS_1,soretd_sentences1 = sim.get_similarity(id2word,corpus,tokens,keywords_0)

all_sentence_scores_ABKS_2A,soretd_sentences2A = sim.get_similarity(id2word,corpus,tokens,keywords_1)
all_sentence_scores_ABKS_2B,soretd_sentences2B = sim.get_similarity(id2word,corpus,tokens,keywords_2)
all_sentence_scores_ABKS_3,soretd_sentences3 = sim.get_similarity(id2word,corpus,tokens,keywords_3)
all_sentence_scores_ABKS_4,soretd_sentences4 = sim.get_similarity(id2word,corpus,tokens,keywords_4)
all_sentence_scores_ABKS_5,soretd_sentences5 = sim.get_similarity(id2word,corpus,tokens,keywords_5)
all_sentence_scores_ABKS_6,soretd_sentences6 = sim.get_similarity(id2word,corpus,tokens,keywords_6)

#all_sentence_scores_ABKS_1 = pd.concat(all_sentence_scores_ABKS_2A,ignore_index=True)
all_sentence_scores_ABKS_1 = pd.concat([all_sentence_scores_ABKS_1, all_sentence_scores_ABKS_2A,all_sentence_scores_ABKS_2B,all_sentence_scores_ABKS_3,all_sentence_scores_ABKS_4,all_sentence_scores_ABKS_5,all_sentence_scores_ABKS_6], axis=0,ignore_index=True)

export_csv = all_sentence_scores_ABKS_1.to_csv ('scores/similarity.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path

sorted_sentences_BO_keywords = []
sorted_sentences_BO_keywords.append(soretd_sentences1)
#,soretd_sentences2B,soretd_sentences3,soretd_sentences4,soretd_sentences4,soretd_sentences5,soretd_sentences6)
sorted_sentences_BO_keywords.append(soretd_sentences2A)
sorted_sentences_BO_keywords.append(soretd_sentences2B)
sorted_sentences_BO_keywords.append(soretd_sentences3)
sorted_sentences_BO_keywords.append(soretd_sentences4)
sorted_sentences_BO_keywords.append(soretd_sentences5)
sorted_sentences_BO_keywords.append(soretd_sentences6)
print(sorted_sentences_BO_keywords)
topic_by = pd.DataFrame(data=sorted_sentences_BO_keywords)

dom_sent_by_keywordsum = fun.get_dominant_sentence_idx(len_sentences,sentence_by_topic_matrix,dom_topic)
dom_sent_by_topicsum = fun.get_dominant_sentence_idx(len_sentences,sentence_by_topic_matrix,num1)
dom_sent_by_topiccount = fun.get_dominant_sentence_idx(len_sentences,sentence_by_topic_matrix,num2)
dom_sent_by_topic_cv = fun.get_dominant_sentence_idx(len_sentences,sentence_by_topic_matrix,num3)
print("=======================================================================")
print("DTSA1 ",dom_sent_by_keywordsum)
print("DTSA2 ",dom_sent_by_topicsum)
print("DTSA3 ",dom_sent_by_topiccount)
print("DTSA4 ",dom_sent_by_topic_cv)
print("=======================================================================")



print("==========================================================")
print("DSSA6 ",dominant_sent_from_alltopics)
print("DSSA6 ",dominant_sentence_topicSum)
print("==========================================================")

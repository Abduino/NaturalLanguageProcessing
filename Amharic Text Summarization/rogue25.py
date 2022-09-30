import numpy as np
import pandas as pd
import nltk
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
from nltk.metrics.scores import precision,recall,f_measure
from nltk.translate.bleu_score import sentence_bleu
stop_word = "stop_words_amharic.txt"
stop_words = codecs.open(stop_word,"r","utf-8").read()
stop_words=re.sub(u'[\r\n]', '',stop_words)
stop_words_amharic = re.split(u'[ ]', stop_words)
def get_scores(can,ref):
    can= re.sub('።፤','', can)
    can= re.sub('  ',' ', can)
    ref= re.sub(u'[።፤]','', ref)
    ref= re.sub('  ',' ', ref)
    ref = re.split(u'[ ]', ref)
    can= re.split(u'[ ]', can)
    reference = set(ref)
    candidate = set(can)
    list1=[]
    p=precision(reference, candidate)
    r=recall(reference, candidate)
    #f1=f_measure(reference, candidate, alpha=0.1))
    f1=f_measure(reference, candidate, alpha=0.9)
    list1.append(p)
    list1.append(r)
    list1.append(f1)
    return list1
    
    
def clean_doc(text):
    print("********** Preprocess the document ************")
    documents = re.split(u'[።]', text)

    tokens= [[word for word in simple_preprocess(str(doc)) if word not in stop_words_amharic] for doc in documents]
    print("len of doc is = ", len(documents))
    return tokens,documents

file_name = "TEST_Doc1.txt"
text = codecs.open(file_name,"r","utf-8").read()
text=re.sub(u'[\n\r()!?፣]', '',text)
print(text)
tokens,sentence = clean_doc(text)
arr1=[0, 3, 1, 2, 21, 10, 17, 23, 5, 11, 6, 8, 26, 18, 15, 20, 12, 4, 9, 24, 7, 14, 19, 25, 22, 13, 16]
arr2=[13, 4, 24, 19, 10, 16, 1, 23, 14, 18, 5, 8, 11, 7, 17, 6, 26, 22, 25, 3, 21, 12, 20, 9, 15, 2, 0]
arr3=[8, 24, 14, 13, 10, 23, 18, 16, 15, 17, 26, 22, 19, 3, 12, 20, 9, 4, 7, 25, 21, 1, 5, 11, 6, 2, 0]
arr4=[0, 14, 1, 23, 5, 11, 6, 8, 26, 18, 15, 3, 20, 10, 2, 4, 12, 24, 9, 7, 17, 21, 19, 25, 22, 13, 16]
arr5=[3, 10, 21, 17, 5, 13, 6, 0, 16, 19, 23, 1, 8, 4, 11, 7, 26, 2, 12, 20, 14, 24, 9, 22, 25, 18, 15]
arr6=[3, 19, 10, 21, 0, 9, 4, 17, 20, 1, 5, 18, 11, 6, 26, 2, 13, 16, 24, 7, 25, 23, 8, 15, 12, 14, 22]
arr7=[6, 5, 1, 9, 11, 21, 4, 7, 19, 25, 13, 23, 16, 8, 26, 18, 15, 3, 10, 20, 2, 12, 24, 14, 17, 0, 22]
candidate1 =""
candidate2 =""
candidate3 =""
candidate4 =""
candidate5 =""
candidate6 =""
candidate7 =""
for i in range(0,5):
    candidate1 = candidate1 + sentence[arr1[i]]
    candidate2 = candidate2 + sentence[arr2[i]]
    candidate3 = candidate3 + sentence[arr3[i]]
    candidate4 = candidate4 + sentence[arr4[i]]
    candidate5 = candidate5 + sentence[arr5[i]]
    candidate6 = candidate6 + sentence[arr6[i]]
    candidate7 = candidate7 + sentence[arr7[i]]


ideal_summary_1 = "\ufeffበገበያ ላይ በተደጋጋሚ እጥረትና የዋጋ ንረት ከሚታይባቸው መሰረታዊ የፍጆታ ዕቃዎች ሌላ፣ ለተለያዩ ግንባታዎች አገልግሎት ላይ የሚውሉ ምርቶች ላይም ተመሣሣይ የሆነ ችግር ሲታይባቸው ቆይቷል።  በአሁኑ ወቅት የሲሚንቶ እጥረት ብቻ ሣይሆን የዋጋ ንረቱ ለኮንትራክተሮችም ሆነ ለቤት አስገንቢዎች ራስ ምታት እየሆነ ከመጣ ሰነባብቷል።  የሲሚንቶ እጥረትና የዋጋ ንረት ለብዙ ሠራተኞችም ሠርቶ ለማደር ሥጋት እየሆነ መምጣቱን እየተመለከትን ነው።  የሲሚንቶ እጥረትና ዋጋ ንረት በየአቅጣጫው ምን ያህል ቤት እንደሚያንኳኳና ለስንቶች ሰቀቀን እንደሚሆን ሲታሰብ ጉዳዩ እንዲሁ በቀላሉ የሚታይ አለመሆኑንም ያመላክታል።  ካለው የገበያ ፍላጎት አንጻር ሲሚንቶ ለማምረት ቅድመ ዝግጅት ላይ ያሉም ሆኑ ግንባታ ሥራ ውስጥ የገቡ የሲሚንቶ ፋብሪካዎች፣ ምርቶቻቸውን ለገበያ ለማቅረብ አመታት የሚጠብቁ መሆናቸውን ስንመለከት ደግሞ ነገሩ የበለጠ ያሳስባል"
ideal_summary_2 = "\ufeffበገበያ ላይ በተደጋጋሚ እጥረትና የዋጋ ንረት ከሚታይባቸው መሰረታዊ የፍጆታ ዕቃዎች ሌላ፣ ለተለያዩ ግንባታዎች አገልግሎት ላይ የሚውሉ ምርቶች ላይም ተመሣሣይ የሆነ ችግር ሲታይባቸው ቆይቷል።  በአሁኑ ወቅት የሲሚንቶ እጥረት ብቻ ሣይሆን የዋጋ ንረቱ ለኮንትራክተሮችም ሆነ ለቤት አስገንቢዎች ራስ ምታት እየሆነ ከመጣ ሰነባብቷል።  የሲሚንቶ እጥረትና የዋጋ ንረት ለብዙ ሠራተኞችም ሠርቶ ለማደር ሥጋት እየሆነ መምጣቱን እየተመለከትን ነው።  በዚህ ምክንያት ከወራት በፊት ዋጋው ተረጋጋ የተባለ የአንድ ኩንታል ሲሚንቶ ዋጋ፣ ከጥቂት ሣምንታት ወዲህ በአማካይ ወደ አራት መቶ ብር ሊደርስ ችሏል።  . ለማንኛውም የሲሚንቶ እጥረትና የዋጋ ንረት ሊያስከትል የሚችለውን ሁለንተናዊ ጉዳት ሲጤን፣ አገሪቱ ለራስዋ የሚበቃ ሲሚንቶ እስከምታገኝ ድረስ አሁንም ብቸኛ የሆነው አማራጭ ምርቱን ከውጭ ማስገባት ነው"
ideal_summary_3 = "\ufeffበአሁኑ ወቅት የሲሚንቶ እጥረት ብቻ ሣይሆን የዋጋ ንረቱ ለኮንትራክተሮችም ሆነ ለቤት አስገንቢዎች ራስ ምታት እየሆነ ከመጣ ሰነባብቷል። የሲሚንቶ እጥረትና የዋጋ ንረት ለብዙ ሠራተኞችም ሠርቶ ለማደር ሥጋት እየሆነ መምጣቱን እየተመለከትን ነው።በአገሪቱ ውስጥ ያሉት የሲሚንቶ ፋብሪካዎች እያደገ የመጣውን የሲሚንቶ ፍላጎት ማሟላት ባለመቻላቸው፤ ሲሚንቶ ከውጭ እስከማምጣት የተደረሰ ቢሆንም፣ አሁን ያለውን ፍላጎት ማሟላት አልተቻለም።  ከሲሚንቶ እጥረትና ዋጋ ንረት ጋር በተያያዘ አንዳንድ የኮንስትራክሽን ግንባታዎች ማለቅ ከሚገባቸው ጊዜ በላይ እየወሰዱም ነው።  በአሁኑ ወቅት የሚካሄዱ ግንባታዎች ብዛት አንፃር ችግሩ ነገም፣ ተነገ ወዲያም ሊቀጥል ይችላል"


can1_id1=get_scores(candidate1,ideal_summary_1)
can1_id2=get_scores(candidate1,ideal_summary_2)
can1_id3=get_scores(candidate1,ideal_summary_3)
all_id =[]
all_id.append(can1_id1)
all_id.append(can1_id2)
all_id.append(can1_id3)
print(all_id)
topic_by_sent = pd.DataFrame(data=all_id)
print(topic_by_sent)
export_csv = topic_by_sent.to_csv ('scores/25%/ABKS1.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path



can1_id1=get_scores(candidate2,ideal_summary_1)
can1_id2=get_scores(candidate2,ideal_summary_2)
can1_id3=get_scores(candidate2,ideal_summary_3)
all_id =[]
all_id.append(can1_id1)
all_id.append(can1_id2)
all_id.append(can1_id3)
print(all_id)
topic_by_sent = pd.DataFrame(data=all_id)
print(topic_by_sent)
export_csv = topic_by_sent.to_csv ('scores/25%/ABKS2.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path




can1_id1=get_scores(candidate3,ideal_summary_1)
can1_id2=get_scores(candidate3,ideal_summary_2)
can1_id3=get_scores(candidate3,ideal_summary_3)
all_id =[]
all_id.append(can1_id1)
all_id.append(can1_id2)
all_id.append(can1_id3)
print(all_id)
topic_by_sent = pd.DataFrame(data=all_id)
print(topic_by_sent)
export_csv = topic_by_sent.to_csv ('scores/25%/ABKS3.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path


can1_id1=get_scores(candidate4,ideal_summary_1)
can1_id2=get_scores(candidate4,ideal_summary_2)
can1_id3=get_scores(candidate4,ideal_summary_3)
all_id =[]
all_id.append(can1_id1)
all_id.append(can1_id2)
all_id.append(can1_id3)
print(all_id)
topic_by_sent = pd.DataFrame(data=all_id)
print(topic_by_sent)
export_csv = topic_by_sent.to_csv ('scores/25%/ABKS4.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path


can1_id1=get_scores(candidate5,ideal_summary_1)
can1_id2=get_scores(candidate5,ideal_summary_2)
can1_id3=get_scores(candidate5,ideal_summary_3)
all_id =[]
all_id.append(can1_id1)
all_id.append(can1_id2)
all_id.append(can1_id3)
print(all_id)
topic_by_sent = pd.DataFrame(data=all_id)
print(topic_by_sent)
export_csv = topic_by_sent.to_csv ('scores/25%/ABKS5.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path

can1_id1=get_scores(candidate6,ideal_summary_1)
can1_id2=get_scores(candidate6,ideal_summary_2)
can1_id3=get_scores(candidate6,ideal_summary_3)
all_id =[]
all_id.append(can1_id1)
all_id.append(can1_id2)
all_id.append(can1_id3)
print(all_id)
topic_by_sent = pd.DataFrame(data=all_id)
print(topic_by_sent)
export_csv = topic_by_sent.to_csv ('scores/25%/ABKS6.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path

can1_id1=get_scores(candidate7,ideal_summary_1)
can1_id2=get_scores(candidate7,ideal_summary_2)
can1_id3=get_scores(candidate7,ideal_summary_3)
all_id =[]
all_id.append(can1_id1)
all_id.append(can1_id2)
all_id.append(can1_id3)
print(all_id)
topic_by_sent = pd.DataFrame(data=all_id)
print(topic_by_sent)
export_csv = topic_by_sent.to_csv ('scores/25%/ABKS7.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path




















'''
candidate = "﻿በገበያ ላይ በተደጋጋሚ እጥረትና የዋጋ ንረት ከሚታይባቸው መሰረታዊ የፍጆታ ዕቃዎች ሌላ ለተለያዩ ግንባታዎች አገልግሎት ላይየሚውሉ ምርቶች ላይም ተመሣሣይ የሆነ ችግር ሲታይባቸው ቆይቷል። የሲሚንቶ እጥረትና የዋጋ ንረት ለብዙ ሠራተኞችም ሠርቶ ለማደር ሥጋት እየሆነ መምጣቱን እየተመለከትን ነው። ለዚህም ሲሚንቶ ጥሩ ምሳሌ ሊሆን ይችላል። በአሁኑ ወቅትየሲሚንቶ እጥረት ብቻ ሣይሆን የዋጋ ንረቱ ለኮንትራክተሮችም ሆነ ለቤት አስገንቢዎች ራስ ምታት እየሆነ ከመጣ ሰነባብቷል። ለማንኛውም የሲሚንቶ እጥረትና የዋጋ ንረት ሊያስከትል የሚችለውን ሁለንተናዊ ጉዳት ሲጤን አገሪቱ ለራስዋ የሚበቃ ሲሚንቶ እስከምታገኝ ድረስ አሁንም ብቸኛ የሆነው አማራጭ ምርቱን ከውጭ ማስገባት ነው። ከሲሚንቶ እጥረትና ዋጋ ንረት ጋር በተያያዘ አንዳንድ የኮንስትራክሽን ግንባታዎች ማለቅ ከሚገባቸው ጊዜ በላይ እየወሰዱም ነው። የሲሚንቶ እጥረትና ዋጋ ንረት በየአቅጣጫው ምን ያህል ቤት እንደሚያንኳኳና ለስንቶች ሰቀቀን እንደሚሆን ሲታሰብ ጉዳዩ እንዲሁ በቀላሉ የሚታይ አለመሆኑንም ያመላክታል።"

ideal_summary_1 = "\ufeffበገበያ ላይ በተደጋጋሚ እጥረትና የዋጋ ንረት ከሚታይባቸው መሰረታዊ የፍጆታ ዕቃዎች ሌላ፣ ለተለያዩ ግንባታዎች አገልግሎት ላይ የሚውሉ ምርቶች ላይም ተመሣሣይ የሆነ ችግር ሲታይባቸው ቆይቷል።  በአሁኑ ወቅት የሲሚንቶ እጥረት ብቻ ሣይሆን የዋጋ ንረቱ ለኮንትራክተሮችም ሆነ ለቤት አስገንቢዎች ራስ ምታት እየሆነ ከመጣ ሰነባብቷል።  የሲሚንቶ እጥረትና የዋጋ ንረት ለብዙ ሠራተኞችም ሠርቶ ለማደር ሥጋት እየሆነ መምጣቱን እየተመለከትን ነው።  የሲሚንቶ እጥረትና ዋጋ ንረት በየአቅጣጫው ምን ያህል ቤት እንደሚያንኳኳና ለስንቶች ሰቀቀን እንደሚሆን ሲታሰብ ጉዳዩ እንዲሁ በቀላሉ የሚታይ አለመሆኑንም ያመላክታል።  ካለው የገበያ ፍላጎት አንጻር ሲሚንቶ ለማምረት ቅድመ ዝግጅት ላይ ያሉም ሆኑ ግንባታ ሥራ ውስጥ የገቡ የሲሚንቶ ፋብሪካዎች፣ ምርቶቻቸውን ለገበያ ለማቅረብ አመታት የሚጠብቁ መሆናቸውን ስንመለከት ደግሞ ነገሩ የበለጠ ያሳስባል።  ለማንኛውም የሲሚንቶ እጥረትና የዋጋ ንረት ሊያስከትል የሚችለውን ሁለንተናዊ ጉዳት ሲጤን፣ አገሪቱ ለራስዋ የሚበቃ ሲሚንቶ እስከምታገኝ ድረስ አሁንም ብቸኛ የሆነው አማራጭ ምርቱን ከውጭ ማስገባት ነው።  ይህ እንዲሆንም መንግሥት ቅድሚያ ሃላፊነት ያለበትና ጉዳዩ በቀጥታ የሚመለከታቸው ኮንትራክተሮችና የንግዱ ህብረተሰብ ምርቱን በማስገባት ለራሳቸው የሚጠቀሙበትና እንዲሁም በአግባቡ ለተጠቃሚዎች ሊያደርሱ የሚችሉበት ጊዜያዊ መመሪያ ተቀርጾ ሥራ ላይ መዋል ይገባዋል።"
ideal_summary_2 = "\ufeffበገበያ ላይ በተደጋጋሚ እጥረትና የዋጋ ንረት ከሚታይባቸው መሰረታዊ የፍጆታ ዕቃዎች ሌላ፣ ለተለያዩ ግንባታዎች አገልግሎት ላይ የሚውሉ ምርቶች ላይም ተመሣሣይ የሆነ ችግር ሲታይባቸው ቆይቷል።  በአሁኑ ወቅት የሲሚንቶ እጥረት ብቻ ሣይሆን የዋጋ ንረቱ ለኮንትራክተሮችም ሆነ ለቤት አስገንቢዎች ራስ ምታት እየሆነ ከመጣ ሰነባብቷል።  የሲሚንቶ እጥረትና የዋጋ ንረት ለብዙ ሠራተኞችም ሠርቶ ለማደር ሥጋት እየሆነ መምጣቱን እየተመለከትን ነው።  በዚህ ምክንያት ከወራት በፊት ዋጋው ተረጋጋ የተባለ የአንድ ኩንታል ሲሚንቶ ዋጋ፣ ከጥቂት ሣምንታት ወዲህ በአማካይ ወደ አራት መቶ ብር ሊደርስ ችሏል።  . ለማንኛውም የሲሚንቶ እጥረትና የዋጋ ንረት ሊያስከትል የሚችለውን ሁለንተናዊ ጉዳት ሲጤን፣ አገሪቱ ለራስዋ የሚበቃ ሲሚንቶ እስከምታገኝ ድረስ አሁንም ብቸኛ የሆነው አማራጭ ምርቱን ከውጭ ማስገባት ነው።  ይህ እንዲሆንም መንግሥት ቅድሚያ ሃላፊነት ያለበትና ጉዳዩ በቀጥታ የሚመለከታቸው ኮንትራክተሮችና የንግዱ ህብረተሰብ ምርቱን በማስገባት ለራሳቸው የሚጠቀሙበትና እንዲሁም በአግባቡ ለተጠቃሚዎች ሊያደርሱ የሚችሉበት ጊዜያዊ መመሪያ ተቀርጾ ሥራ ላይ መዋል ይገባዋል።  ችግሩ አገር አቀፍ በመሆኑም መንግሥት እንዲገባ የሚፈቅደው የሲሚንቶ ምርት በትክክል ለሚገነቡ አካላት ስለመድረሱ የሚያረጋግጥ ቁጥጥር ማድረግም ይጠበቅበታል።"
ideal_summary_3 = "በአሁኑ ወቅት የሲሚንቶ እጥረት ብቻ ሣይሆን የዋጋ ንረቱ ለኮንትራክተሮችም ሆነ ለቤት አስገንቢዎች ራስ ምታት እየሆነ ከመጣ ሰነባብቷል። የሲሚንቶ እጥረትና የዋጋ ንረት ለብዙ ሠራተኞችም ሠርቶ ለማደር ሥጋት እየሆነ መምጣቱን እየተመለከትን ነው።በአገሪቱ ውስጥ ያሉት የሲሚንቶ ፋብሪካዎች እያደገ የመጣውን የሲሚንቶ ፍላጎት ማሟላት ባለመቻላቸው፤ ሲሚንቶ ከውጭ እስከማምጣት የተደረሰ ቢሆንም፣ አሁን ያለውን ፍላጎት ማሟላት አልተቻለም።  ከሲሚንቶ እጥረትና ዋጋ ንረት ጋር በተያያዘ አንዳንድ የኮንስትራክሽን ግንባታዎች ማለቅ ከሚገባቸው ጊዜ በላይ እየወሰዱም ነው።  በአሁኑ ወቅት የሚካሄዱ ግንባታዎች ብዛት አንፃር ችግሩ ነገም፣ ተነገ ወዲያም ሊቀጥል ይችላል።  ለማንኛውም የሲሚንቶ እጥረትና የዋጋ ንረት ሊያስከትል የሚችለውን ሁለንተናዊ ጉዳት ሲጤን፣ አገሪቱ ለራስዋ የሚበቃ ሲሚንቶ እስከምታገኝ ድረስ አሁንም ብቸኛ የሆነው አማራጭ ምርቱን ከውጭ ማስገባት ነው።ይህ እንዲሆንም መንግሥት ቅድሚያ ሃላፊነት ያለበትና ጉዳዩ በቀጥታ የሚመለከታቸው ኮንትራክተሮችና የንግዱ ህብረተሰብ ምርቱን በማስገባት ለራሳቸው የሚጠቀሙበትና እንዲሁም በአግባቡ ለተጠቃሚዎች ሊያደርሱ የሚችሉበት ጊዜያዊ መመሪያ ተቀርጾ ሥራ ላይ መዋል ይገባዋል።"






can= re.sub('።፤','', candidate)
ref= re.sub(u'[።፤]','', ideal_summary_3)
ref = re.split(u'[ ]', ref)
can= re.split(u'[ ]', can)
print(ref)
print(can)
reference = set(ref)
candidate = set(can)
print(precision(reference, candidate))
print(recall(reference, candidate))
print(f_measure(reference, candidate, alpha=0.1))
print(f_measure(reference, candidate, alpha=0.9))
#for i in range(0,)

precision_score=[]
recall_score=[]
f_mes=[]
all_scores=[]
for i in range(0,7):
    ref= re.split(u'[ ]', ideal_summary_1[i])
    can=tokens[arr1[i]]
    reference = set(ref)
    candidate = set(can)

    precision_score.append(precision(reference, candidate))
    recall_score.append(recall(reference, candidate))
    f_mes.append(f_measure(reference, candidate, alpha=0.9))
all_scores.append(precision_score)
all_scores.append(recall_score)
all_scores.append(f_mes)

'''

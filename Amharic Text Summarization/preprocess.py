import nltk
from nltk.tokenize import RegexpTokenizer

from nltk.tokenize import word_tokenize, sent_tokenize
import codecs
import re

# function: open different files

                
file_name = "2.txt"
text = codecs.open(file_name,"r","utf-8").read()
text=re.sub('\n', '',text)
print(text)
stop_word = "stop_words_amharic.txt"
stop_words = codecs.open(stop_word,"r","utf-8").read()
print(stop_words)
stop_words=re.sub(u'[\r\n]', '',stop_words)
words = re.split(u'[ ]', stop_words)

print(words)
'''
sents = re.split(u'[!?፨፠\r\t።] ', text)
for i in sents:
        print("===============================")
        print(i)
print(len(sents))
for sent in sents:
        sent = re.sub(u'(^[.፡ ]+|[.፡ ]+$)', '', sent)
        print("____________________________________")
        print(sent)


#sentences= return_sent(text)
'''


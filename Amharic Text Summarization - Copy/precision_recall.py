import numpy as np
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


reference = set()
candidate = set(candidate)

print("P = ",precision(reference, candidate))
print("R = ",recall(reference, candidate))
print("F1 = ",f_measure(reference, candidate, alpha=0.1))

print("F1 = ",f_measure(reference, candidate, alpha=0.5))




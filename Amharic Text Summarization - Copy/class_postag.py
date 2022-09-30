# -*- coding: utf-8 -*-

import numpy
import pandas
import codecs
import re
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import scale


def opening(file_name):
	f = codecs.open(file_name, 'r', 'utf-8')
	array = [line.strip() for line in f]
	f.close()
	return array
def open_dict():
	dict = codecs.open('used_files/cleaned_dictionary.txt', 'r', 'utf-8')
	dictionary = {}
	for line in dict:
		split_line = line.split('\t')
		if len(split_line) == 2:
			dictionary[split_line[1]] = split_line[0]
		else:
			i = 1
			while i != 8:
				try:
					dictionary[split_line[i]] = split_line[0]
				except:
					pass
				i += 1
	dict.close()
	return dictionary

def get_feu(word):
        print("=>",word)
        dictionary = open_dict()
        consonants = opening('used_files/consonants.txt')
        vowel_o = opening('used_files/vowel_o.txt')
        vowel_u = opening('used_files/vowel_u.txt')
        vowel_e = opening('used_files/vowel_e.txt')
        vowel_i = opening('used_files/vowel_i.txt')
        vowel_a = opening('used_files/vowel_a.txt')
        vowel_ae = opening('used_files/vowel_ae.txt')
        pronouns = opening('used_files/pronouns.txt')
        numerals = opening('used_files/numerals.txt')
        verbs = opening('used_files/verbs.txt')
        conjunctions = opening('used_files/conjunctions.txt')
        adpositions = opening('used_files/adpositions.txt')
        particles = opening('used_files/particles.txt')
        demonstratives = opening('used_files/demonstratives.txt')
        quest_pronouns = opening('used_files/quest_pronouns.txt')
        personal_pronouns = opening('used_files/pers_pronouns.txt')
        
        word = re.sub(u'<.+?>', '', word)
        print("=>2",word)
        punctl = re.findall(u'^[-_:;\'\"\#*«»)(\]\[^$@}{‘’><.,?!%፠፡፣፤፥፧።፨፦]', word)
        punctr = re.findall(u'[-_:;\'\"\#*«»)(\]\[^$@}{‘’><.,?!%፠፡፣፤፥፧።፨፦]$', word)
        word = re.sub(u'(^[-_:;\'\"\#*«»)(\]\[^$@}{‘’><.,?!%፠፡፣፤፥፧።፨፦]|[-_:;\'\"\#*«»)(\]\[^$@}{‘’><.,?!%፠፡፣፤፥፧።፨፦]$)', '', word)
        print("=>3",word)
        if word in dictionary:
                print("yes")
                if dictionary[word] == 'n':
                        print("n")

                if dictionary[word] == 'adj':
                        print(word, 'ADJ')
                if dictionary[word] == 'pron':
                        print(word , 'PRON')

                if dictionary[word] == 'v':
                        print(word,'V')
                
                if dictionary[word] == 'adv':
                        print(w,'ADV')
          
                if dictionary[word] == 'prep':
                        print(w,'ADL')
         
                if dictionary[word] == 'conj':
                        print(word,'CONJ')

                if dictionary[word] == 'num':
                        print(word,'NUM')
     
                if dictionary[word] == 'part':
                        print(word,'PART')

        elif word in verbs:
                print("V" , w, 'V')
        elif word in conjunctions:
                tags.append(2)
                string = for_yield('CONJ')
                yield string
        elif word in pronouns:
                tags.append(5)
                string = for_yield('PRON')
                yield string
        elif word in adpositions:
                tags.append(3)
                string = for_yield('ADL')
                yield string
        elif re.search('[0-9]', word):
                tags.append(4)
                string = for_yield('NUM')
                yield string
        elif word in particles:
                tags.append(8)
                string = for_yield('PART')
                yield string
        elif word in numerals:
                tags.append(4)
                string = for_yield('NUM')
                yield string
        elif len(word) >= 3 and (word[:2] == u'የዚ' or word[:2] == u'በዚ' or word[:2] == u'ከዚ') and word[2:] in demonstratives:

        elif len(word) >= 3 and (word[:2] == u'የዚ' or word[:2] == u'በዚ' or word[:2] == u'ከዚ') and u'ይ' + word[2:] in demonstratives:
                tags.append(5)
                string = for_yield('PRON')
                yield string
        elif len(word) >= 2 and (word[0] == u'የ' or word[0] == u'ለ' or word[0] == u'በ') and word[1:] in personal_pronouns:
                tags.append(5)
                string = for_yield('PRON')
                yield string
        elif len(word) >= 3 and word[:2] == u'ስለ' and word[2:] in personal_pronouns:
                tags.append(5)
                string = for_yield('PRON')
                yield string
        elif len(word) >= 3 and ((word[-2] == u'ኛ' and (word[-1] == u'ው' or word[-1] == u'ዋ' or word[-1] in vowel_u)) or (word[-1] == u'ም' and (word[-2] == u'ው' or word[-2] == u'ዋ' or word[-2] in vowel_u))) and word[:-2] in quest_pronouns:
                tags.append(5)
                string = for_yield('PRON')
                yield string
        elif word in hash_dict:
                tags.append(str(hash_dict[word]))
                tag = str(hash_dict[word])
                if tag == 0:
                        string = for_yield('V')
                        yield string
                if tag == 1:
                        string = for_yield('ADJ')
                        yield string
                if tag == 2:
                        string = for_yield('ADV')
                        yield string
                if tag == 3:
                        string = for_yield('N')
                        yield string
        else:
                pred = perc.predict(features)
                tag =  int(re.sub('[\[\]]', '', str(pred)))
                tags.append(tag)
                if tag == 0:
                        string = for_yield('V')
                        yield string
                if tag == 1:
                        string = for_yield('ADJ')
                        yield string
                if tag == 2:
                        string = for_yield('ADV')
                        yield string
                if tag == 3:
                        string = for_yield('N')
                        yield string

        count += 1

val_tags = validate_with_mappings(tags, target, features)

print 'Accuracy ', accuracy_score(target, val_tags)
#print 'Precision ', precision_score(target, val_tags)
#print 'Recall ', recall_score(target, val_tags)
print 'F1 ', f1_score(target, val_tags)

'''

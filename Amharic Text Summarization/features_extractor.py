# coding:utf-8

import codecs
import re

# function: open different files
def opening(file_name):
	f = codecs.open(file_name, 'r', 'utf-8')
	array = [line.strip() for line in f]
	f.close()
	return array

# fucnction: opend dictionary
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

# function: get sentences

def feat_extract(name, text):
	# crate file for writing
	f_name = name.replace('.txt', '')
	feat_name = 'features_' + f_name + '.csv'
	w = codecs.open(feat_name, 'w', 'utf-8')

	# open needed files
	dictionary = open_dict()
	consonants = opening('.\\used_files\\consonants.txt')
	vowel_o = opening('.\\used_files\\vowel_o.txt')
	vowel_u = opening('.\\used_files\\vowel_u.txt')
	vowel_e = opening('.\\used_files\\vowel_e.txt')
	vowel_i = opening('.\\used_files\\vowel_i.txt')
	vowel_a = opening('.\\used_files\\vowel_a.txt')
	vowel_ae = opening('.\\used_files\\vowel_ae.txt')
	pronouns = opening('.\\used_files\\pronouns.txt')
	numerals = opening('.\\used_files\\numerals.txt')
	verbs = opening('.\\used_files\\verbs.txt')
	conjunctions = opening('.\\used_files\\conjunctions.txt')
	adpositions = opening('.\\used_files\\adpositions.txt')
	particles = opening('.\\used_files\\particles.txt')
	demonstratives = opening('.\\used_files\\demonstratives.txt')
	quest_pronouns = opening('.\\used_files\\quest_pronouns.txt')
	personal_pronouns = opening('.\\used_files\\pers_pronouns.txt')

	object_suffixes = [u'ኝ', u'ህ', u'ሽ', u'ው', u'ን']
	middle_tongue_a = [u'ቻ', u'ጃ', u'ጫ', u'ኻ', u'ዣ', u'ኛ', u'ያ']
	middle_tongue = [u'ች', u'ኝ', u'ዥ', u'ጭ', u'ጅ', u'ኽ', u'ይ']
	front_tongue_i = [u'ቲ', u'ዲ', u'ጢ', u'ሲ', u'ዚ', u'ኪ', u'ሊ']

	freq_dictionary ={}

	# function: create frequency dictionary
	def freq_dict(word, freq_dictionary = freq_dictionary):
		if word in freq_dictionary:
			freq_dictionary[word] += 1
		else:
			freq_dictionary[word] = 1

	words_out = []
	threshold = 0

	# get features and write in the file
	for sent in return_sent(text):
		words = re.split(u'[፡ ]+', sent)
		numb_word = 1
		for word in words:
			# outcomment when clastering
			if threshold == 11500:
				break
			# add or word in freq_dictionary when clastering
			if word == '':
				continue
			if word[-1] in u'፣፤፥':
				punct = 1
			else:
				punct = 0

			word = re.sub(u'[-_:;\'\"\#*«»)(\]\[^$@}{‘’><.,?!%፠፡፣፤፥፧።፨፦]', '', word)
			if word == '':
				continue

			'''
			if word in verbs:
				continue
			if word in conjunctions:
				continue
			if word in pronouns:
				continue
			if word in adpositions:
				continue
			if re.search('[0-9]', word):
				continue
			if word in particles:
				continue
			if word in numerals:
				continue

			if len(word) >= 3 and (word[:2] == u'የዚ' or word[:2] == u'በዚ' or word[:2] == u'ከዚ'):
				try_word = word[2:]
				if try_word in demonstratives:
					continue
				else:
					try_word = u'ይ' + word[2:]
					if try_word in demonstratives:
						continue
			if len(word) >= 2 and (word[0] == u'የ' or word[0] == u'ለ' or word[0] == u'በ'):
				try_word = word[1:]
				if try_word in personal_pronouns:
					continue
				elif len(word) >= 3 and word[:2] == u'ስለ':
					try_word = word[2:]
					if try_word in personal_pronouns:
						continue
			if len(word) >= 2 and (word[-1] == u'ኛ' or word[-1] == u'ም'):
				change = [u'ህ', u'ቶ', u'ና', u'ያ', u'ባ', u'ሳ', u'ራ', u'ር', u'ኝ', u'ት', u'ድ']
				for i in change:
					try_word = word[:-2] + i
					if try_word in numerals:
						continue
			if len(word) >= 3 and ((word[-2] == u'ኛ' and (word[-1] == u'ው' or word[-1] == u'ዋ' or word[-1] in vowel_u)) or (word[-1] == u'ም' and (word[-2] == u'ው' or word[-2] == u'ዋ' or word[-2] in vowel_u))):
				try_word = word[:-2]
				if try_word in quest_pronouns:
					continue

			'''

			w.write(word + ';')
			freq_dict(word)
			words_out.append(word)

			# check punct
			if punct == 1:
				w.write('1;')
			else:
				w.write('0;')

			# check word length
			#w.write(str(len(word)) + ';')

			# check first word
			if numb_word == 1:
				w.write('1;')
			else:
				w.write('0;')

			# check last word
			if numb_word == len(words):
				w.write('1;')
			else:
				w.write('0;')

			### unambiguous

			# ---VERY SIGNIFICANT---
			v = 0
			v_wh = 0
			adj = 0
			adj_wh = 0
			prep = 0
			prep_wh = 0
			conj = 0
			conj_wh = 0
			num = 0
			num_wh = 0
			adv = 0
			adv_wh = 0
			pron = 0
			pron_wh = 0
			n = 0
			n_wh = 0
			part = 0
			part_wh = 0

			def check_in(group, count, amount, word = word):
				if word in group:
					count += 1
					amount += 1
				else:
					amount += 1

			'''
			# check numerals
			if re.search('[0-9]', word):
				num += 1
				numb_word += 1
			else:
				numb_word += 1

			# check auxiliary
			check_in(verbs, v, v_wh)

			# check conjunctions
			check_in(conjunctions, conj, conj_wh)

			# check pronouns
			check_in(pronouns, pron, pron_wh)

			# check postpositions
			check_in(adpositions, prep, prep_wh)

			# check particles
			check_in(particles, part, part_wh)
			'''

			'''
			# check demonstartives
			if word in demonstratives:
				pron += 1
				pron_wh += 1
			elif len(word) >= 3 and (word[:2] == u'የዚ' or word[:2] == u'በዚ' or word[:2] == u'ከዚ'):
				try_word = word[2:]
				if try_word in demonstratives:
					pron += 1
					pron_wh += 1
				else:
					try_word = u'ይ' + word[2:]
					if try_word in demonstratives:
						pron += 1
						pron_wh += 1
					else:
						pron_wh += 1
			else:
				pron_wh += 1

			# check personal pronoun
			if word in personal_pronouns:
				pron += 1
				pron_wh += 1
			elif len(word) >= 2 and (word[0] == u'የ' or word[0] == u'ለ' or word[0] == u'በ'):
				try_word = word[1:]
				if try_word in personal_pronouns:
					pron += 1
					pron_wh += 1
				else:
					pron_wh += 1
			elif len(word) >= 3 and word[:2] == u'ስለ':
				try_word = word[2:]
				if try_word in personal_pronouns:
					pron += 1
					pron_wh += 1
				else:
					pron_wh += 1
			else:
				pron_wh += 1

			# check numerals
			if word in numerals:
				num += 1
				num_wh += 1
			elif len(word) >= 2 and (word[-1] == u'ኛ' or word[-1] == u'ም'):
				change = [u'ህ', u'ቶ', u'ና', u'ያ', u'ባ', u'ሳ', u'ራ', u'ር', u'ኝ', u'ት', u'ድ']
				for i in change:
					try_word = word[:-2] + i
					if try_word in numerals:
						num += 1
						num_wh += 1
						break
					else:
						num_wh += 1
			else:
				num_wh += 1

			# check question pronoun
			if word in quest_pronouns:
				pron += 1
				pron_wh += 1
			if len(word) >= 3 and ((word[-2] == u'ኛ' and (word[-1] == u'ው' or word[-1] == u'ዋ' or word[-1] in vowel_u)) or (word[-1] == u'ም' and (word[-2] == u'ው' or word[-2] == u'ዋ' or word[-2] in vowel_u))):
				try_word = word[:-2]
				if try_word in quest_pronouns:
					pron += 1
					pron_wh += 1
				else:
					pron_wh += 1
			else:
				pron_wh += 1
			'''

			### ambiguous

			# ---SIGNIFICANT---

			# check adverbial participle
			if len(word) >= 5 and word[:2] == u'እየ' and ((word[-3:] == u'ችሁም' and word[-4] in vowel_a) or (word[-2:] == u'ችም' and word[-3] in vowel_ae) or (word[-2:] == u'ንም' and word[-3] in consonants) or (word[-3] in vowel_o and word[-2:] == u'ውም')):
				adv += 1
				adv_wh += 1
			else:
				adv_wh += 1

			# check double vowels
			for i in range(0, len(word) - 1):
				if word[i] == word[i + 1]:
					adj += 1
					adj_wh += 1
					break
				else:
					adj_wh += 1

			# check object pronoun suffix
			if len(word) >= 4 and word[-3] in vowel_a and (word[-2:] == u'ቸው' or word[-2:] == u'ችሁ' or word[-2:] == u'ቸው' or word[-2:] == u'ችሁ'):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check verbal past
			if len(word) >= 4 and word[-3:] == u'አችሀ':
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check verbal present-future form
			if len(word) >= 4 and (word[0] == u'እ' or word[0] == u'ች' or word[0] == u'ይ') and (word[-3] in vowel_a and (word[-2:] == u'ለሁ' or word[-2:] == u'ለህ' or word[-2:] == u'ለሽ' or word[-2:] == u'ለች' or word[-2:] == u'ለን' or word[-2:] == u'ችሁ')):
				v += 1
				v_wh += 1
			elif len(word) >= 4 and (word[0] == u'እ' or word[0] == u'ች' or word[0] == u'ይ') and (word[-2] in vowel_a and (word[-1] == u'ሉ' or word[-1] == u'ል')):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check infinitive
			if len(word) >= 4 and word[:3] == u'አለመ':
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check analytic form
			if len(word) >= 4 and (u'አለሁ' in word or u'አለች' in word or u'አል' in word):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check subordinate of clause
			if len(word) >= 4 and (word[:2] == u'ስለ' or word[:3] == u'ስለም'):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check noun/adjective prefix
			if len(word) >= 4 and (word[:2] == u'ባለ' or word[:2] == u'ሰረ'):
				n += 1
				n_wh += 1
				adj += 1
				adj_wh += 1
			else:
				n_wh += 1
				adj_wh += 1

			# check adverbial participle
			if len(word) >= 4 and ((word[-2:] == u'ችሁ' and word[-3] in vowel_a) or (word[-2] in vowel_o and word[-1] == u'ው')):
				adv += 1
				adv_wh += 1
			elif len(word) >= 4 and (word[:2] == u'እየ' and ((word[-2:] == u'ችሁ' and word[-3] in vowel_a) or (word[-1] == u'ች' and word[-2] in vowel_ae) or (word[-1] == u'ን' and word[-2] in consonants))):
				adv += 1
				adv_wh += 1
			else:
				adv_wh += 1

			# check adverbial participle with negation
			if len(word) >= 4 and ((word[-1] == u'ም' and word[-2] in vowel_e or word[-2] in vowel_a or word[-2] in vowel_o) or ((word[-2:] == u'ህም' or word[-2:] == u'ሽም' or word[-2:] == u'ሽም') and word[-3] in vowel_ae)):
				adv += 1
				adv_wh += 1
			elif len(word) >= 4 and word[-1] == u'ም' and (word[:2] == u'እየ' and (word[-2] == u'ሁ' or word[-2] == u'ህ' or word[-2] == u'ሽ' or word[-2] in vowel_ae or word[-2] in vowel_u)):
				adv += 1
				adv_wh += 1
			else:
				adv_wh += 1

			# ---LESS SIGNIFIANT---

			# check a definite article
			if len(word) >= 3 and (word[-2:] == u'ዮዋ' or word[-2:] == u'ዮው'):
				n += 1
				n_wh += 1
			else:
				n_wh += 1

			# check verbal past
			if len(word) >= 3 and word[-2] in consonants and (word[-1] == u'ህ' or word[-1] == u'ክ' or word[-1] == u'ሁ'or word[-1] == u'ኩ' or word[-1] == u'ሽ'):
				v += 1
				v_wh += 1
			elif len(word) >= 3 and word[-2] in vowel_ae and word[-1] == u'ች':
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check object pronoun suffix
			if len(word) >= 3 and word[-2:] == u'ዎት':
				v += 1
				v_wh += 1
			elif len(word) >= 3 and word[-2] in vowel_a and word[-1] == u'ት':
				v += 1
				v_wh += 1
			elif len(word) >= 3 and word[-1] == u'ት' and word[-2] in vowel_u:
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check verbal negation
			if len(word) >= 3 and word[-1] == u'ም':
				v += 1
				v_wh += 1
			elif len(word) >= 3 and word[0] == u'አ':
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check prefix of verbal present-future stem
			if len(word) >= 3 and (word[0] == u'እ' or word[0] == u'ች' or word[0] == u'ይ'):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check attributive form of a verb
			if len(word) >= 3 and (word[0] == u'የ' or word[:2] == u'የም' or word[:2] == u'ያል'):
				adj += 1
				adj_wh += 1
			else:
				adj_wh += 1

			# check wish
			if len(word) >= 3 and ((word[-1] in consonants or word[-1] in vowel_u) and (word[0] == u'ል' or word[0] == u'ይ' or word[0] == u'ት' or word[:2] == u'እን')):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check noun suffix
			if len(word) >= 3 and ((word[-1] == u'ኛ' and (word[-2] in vowel_ae or word[-2] in consonants)) or ((word[-2:] == u'ነት' or word[-1] == u'ታ') and word[-2] in consonants)):
				n += 1
				n_wh += 1
			else:
				n_wh += 1

			# check adverbial participle
			if len(word) >= 3 and (word[-1] in vowel_e or word[-1] in vowel_a or word[-1] in vowel_o or ((word[-1] == u'ህ' or word[-1] == u'ሽ' or word[-1] == u'ሽ') and word[-2] in vowel_ae)):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check adverbial participle
			if len(word) >= 3 and word[:2] == u'በመ':
				v += 1
				v_wh += 1
			elif len(word) >= 3 and word[:2] == u'እየ' and (word[-1] == u'ሁ' or word[-1] == u'ህ' or word[-1] == u'ሽ' or word[-1] in vowel_ae or word[-1] in vowel_u):
				v += 1
				v_wh += 1
			elif len(word) >= 3 and (word[:2] == u'ስት' or word[:2] == u'ስን' or word[0] == u'ሲ'):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check adjective suffix
			if len(word) >= 3 and (((word[-1] == u'ም' or word[-1] == u'ማ' or word[-1] == u'ዊ') and word[-2] in vowel_a) or (word[-1] == u'ኛ' and (word[-2] in vowel_ae or word[-2] in consonants))):
				adj += 1
				adj_wh += 1
			else:
				adj_wh += 1

			# ---ALMOST INSIGNIFICANT---

			# check plural for nouns
			if len(word) >= 2 and ((word[-1] == u'ች' or word[-1] == u'ቹ') and word[-2] in vowel_o):
				n += 1
				n_wh += 1
			else:
				n_wh += 1

			# check a definite article
			if len(word) >= 2 and (word[-1] == u'ው' or word[-1] == u'ዋ' or word[-1] in vowel_u or word[-1] == u'ቱ'):
				n += 1
				n_wh += 1
			else:
				n_wh += 1

			# check possessive suffix
			if len(word) >= 2 and (word[-1] in vowel_e or word[-1] in vowel_u or word[-1] == u'ው' or word[-1] == u'ህ' or word[-1] == u'ህ' or word[-1] == u'ዎ' or word[-1] == u'ዋ'):
				n += 1
				n_wh += 1
				pron += 1
				pron_wh += 1
				v += 1
				v_wh += 1
			else:
				n_wh += 1
				pron_wh += 1
				v_wh += 1

			# check possessive prefix
			if len(word) >= 2 and word[0] == u'የ':
				n += 1
				n_wh += 1
			else:
				n_wh += 1

			# check verbal past
			if len(word) >= 2 and word[-1] in vowel_u:
				v += 1
				v_wh += 1
			elif len(word) >= 2 and word[-1] in vowel_ae:
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check accusative
			if len(word) >= 2 and word[-1] == u'ን':
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check prepositions
			if len(word) >= 2 and (word[0] == u'በ' or word[0] == u'ባ' or word[0] == u'ከ' or word[0] == u'ካ' or word[0] == u'እ' or word[0] == u'ለ' or word[0] == u'ስ'):
				n += 1
				n_wh += 1
				pron += 1
				pron_wh += 1
				v += 1
				v_wh += 1
			else:
				n_wh += 1
				pron_wh += 1
				v_wh += 1

			# check object pronoun suffix
			if len(word) >= 2 and word[-1] in object_suffixes:
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check infinitive
			if len(word) >= 2 and word[0] == u'መ':
				v += 1
				v_wh += 1
			elif len(word) >= 2 and word[-1] == u'ት':
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check passive voice
			if len(word) >= 2 and word[0] == u'ተ':
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check place or instrument noun
			if len(word) >= 2 and word[-1] in middle_tongue_a:
				n += 1
				n_wh += 1
			else:
				n_wh += 1

			# check actor noun
			if len(word) >= 2 and (word[-1] in middle_tongue or (word[-1] in vowel_i and word[-1] not in front_tongue_i)):
				n += 1
				n_wh += 1
			else:
				n_wh += 1

			# check causative voice
			if len(word) >= 2 and word[0] == u'አ':
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check purpose of an action
			if len(word) >= 2 and (word[0] == u'ሌ' or word[0] == u'ለ'):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check analytic form
			if len(word) >= 2 and (((word[-2:] == u'ለሁ' or word[-2:] == u'ለች') and word[-3] in vowel_a) or (word[-1] == u'ል' and word[-2] in vowel_a)):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			# check adverb prefix
			if len(word) >= 2 and (word[0] == u'በ' or word[0] == u'ለ' or word[:3] == u'እንደ' or word[:3] == u'በስተ' or word[:2] == u'ያለ' or word[:2] == u'በየ' or word[:3] == u'እስከ' or word[:3] == u'ከዎደ'):
				adv += 1
				adv_wh += 1
			else:
				adv_wh += 1

			# check order
			if len(word) >= 2 and (word[-1] in consonants or word[-1] in vowel_i or word[-1] in vowel_u):
				v += 1
				v_wh += 1
			else:
				v_wh += 1

			def writing(count, amount, w = w):
				if amount == 0:
					w.write('0;')
				else:
					w.write(str(float(count)/amount) + ';')

			writing(v, v_wh)
			writing(n, n_wh)
			writing(adj, adj_wh)
			writing(adv, adv_wh)
			writing(prep, prep_wh)
			writing(conj, conj_wh)
			writing(part, part_wh)
			if num_wh == 0:
				w.write('0')
			else:
				w.write(str(float(num)/num_wh))

			w.write('\n')
			numb_word += 1
			threshold += 1
	w.close()
	return feat_name, freq_dictionary, words_out

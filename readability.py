"""Simple readability measures.

Usage: %s [--lang=<x>] [file]

By default, input is read from standard input.
Text should be encoded with UTF-8,
one sentence per line, tokens space-separated.

  -L, --lang=<x>   set language for syllabification (default: en)."""
from __future__ import division, print_function
import io
import sys
import math
import getopt
import collections
import syllables

class Readability:
	def __init__(self, text, lang='en'):
		"""Text has one sentence per line, with space separated tokens."""
		self.words = text.split()
		char_count = get_char_count(self.words)
		syllable_count = count_syllables(self.words, lang)
		word_count = len(self.words)
		sentences = text.splitlines()
		complexwords_count = count_complex_words(self.words, sentences, lang)
		sentence_count = len(sentences)
		avg_words_p_sentence = word_count / sentence_count

		self.stats = collections.OrderedDict([
				('char_cnt', (char_count)),
				('word_cnt', (word_count)),
				('avg_char_p_word', (char_count / word_count)),
				('syllable_cnt', (syllable_count)),
				('avg_syll_p_word', (syllable_count / word_count)),
				('complex_word_cnt', (complexwords_count)),
				('sentence_cnt', (sentence_count)),
				('avg_words_p_sentence', (avg_words_p_sentence)),
			])
		self.readability = collections.OrderedDict([
				('FleschKincaidGradeLevel', self.FleschKincaidGradeLevel()),
				('ARI', self.ARI()),
				('ColemanLiauIndex', self.ColemanLiauIndex()),
				('FleschReadingEase', self.FleschReadingEase()),
				('GunningFogIndex', self.GunningFogIndex()),
				('LIX', self.LIX()),
				('SMOGIndex', self.SMOGIndex()),
				('RIX', self.RIX()),
			])

	def ARI(self):
		return 4.71 * (self.stats['char_cnt'] / self.stats['word_cnt']
				) + 0.5 * (self.stats['word_cnt']
				/ self.stats['sentence_cnt']) - 21.43
		
	def FleschReadingEase(self):
		return 206.835 - (1.015 * (self.stats['avg_words_p_sentence'])
				) - (84.6 * (self.stats['syllable_cnt'] /
					self.stats['word_cnt']))
		
	def FleschKincaidGradeLevel(self):
		return 0.39 * (self.stats['avg_words_p_sentence']) + 11.8 * (
				self.stats['syllable_cnt']/ self.stats['word_cnt']) - 15.59
		
	def GunningFogIndex(self):
		return 0.4 * ((self.stats['avg_words_p_sentence']) + (100 * (
				self.stats['complex_word_cnt']/self.stats['word_cnt'])))

	def SMOGIndex(self):
		return (math.sqrt(self.stats['complex_word_cnt']
				* (30 / self.stats['sentence_cnt'])) + 3)

	def ColemanLiauIndex(self):
		return (5.89 * (self.stats['char_cnt'] / self.stats['word_cnt'])
				) - (30 * (self.stats['sentence_cnt'] /
					self.stats['word_cnt'])) - 15.8

	def LIX(self):
		longwords = 0.0
		for word in self.words:
			if len(word) >= 7:
				longwords += 1.0
		return self.stats['word_cnt'] / self.stats['sentence_cnt'] + (
				100 * longwords) / self.stats['word_cnt']

	def RIX(self):
		longwords = 0.0
		for word in self.words:
			if len(word) >= 7:
				longwords += 1.0
		return longwords / self.stats['sentence_cnt']
		

def get_char_count(words):
	characters = 0
	for word in words:
		if word == "'s":
			characters += 2
		else:
			characters += sum(1 for char in word
					if char.isdigit() or char.isalpha() or char == '-')
	return characters
	
def count_syllables(words, lang):
	syllableCount = 0
	for word in words:
		syllableCount += syllables.count(word, lang)
	return syllableCount

#This method must be enhanced. At the moment it only
#considers the number of syllables in a word.
#This often results in that too many complex words are detected.
def count_complex_words(words, sentences, lang):
	complex_words = 0
	found = False
	cur_word = []
	
	for word in words:
		cur_word.append(word)
		if count_syllables(cur_word, lang) >= 3:
			
			#Checking proper nouns. If a word starts with a capital letter
			#and is NOT at the beginning of a sentence we don't add it
			#as a complex word.
			if not(word[0].isupper()):
				complex_words += 1
			else:
				for sentence in sentences:
					if str(sentence).startswith(word):
						found = True
						break
				if found:
					complex_words += 1
					found = False
				
		cur_word.remove(word)
	return complex_words


def main():
	shortoptions = 'hL:'
	options = 'help lang='.split()
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], shortoptions, options)
	except getopt.GetoptError as err:
		print('error: %r\n%s' % (err, __doc__ % sys.argv[0]))
		sys.exit(2)
	opts = dict(opts)
	if '--help' in opts or '-h' in opts:
		print(__doc__ % sys.argv[0])
		return
	if len(args) == 0:
		text = sys.stdin.read().decode('utf-8')
	elif len(args) == 1:
		text = io.open(args[0], encoding='utf-8').read()
	else:
		raise ValueError('expected 0 or 1 file argument.')

	rd = Readability(text, opts.get('lang', 'en'))
	print('readability grades:')
	for key, val in rd.readability.items():
		print('\t%s: %g' % (key, round(val, 2)))
	print('sentence info:')
	for key, val in rd.stats.items():
		print('\t%s: %g' % (key, round(val, 2)))
	#print('word usage:')
	#print('sentence beginnings:')

if __name__ == "__main__":
	main()

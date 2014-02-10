"""Simple readability measures.

Usage: %s [--lang=<x>] [file]

By default, input is read from standard input.
Text should be encoded with UTF-8,
one sentence per line, tokens space-separated.

  -L, --lang=<x>   set language for syllabification (available: %s)."""
from __future__ import division, print_function
import io
import re
import sys
import math
import getopt
import collections
import syllables

PUNCT = re.compile('[.,:;\'"!?]')


class Readability:
	def __init__(self, text, lang='en'):
		"""text has one sentence per line, with space separated tokens."""
		self.tokens = text.split()
		characters = 0
		words = 0
		syllable_count = 0
		complex_words = 0
		long_words = 0
		syllcount = syllables.COUNT[lang]

		paragraph_count = text.count('\n\n')
		sentence_count = text.count('\n') - paragraph_count

		for word in self.tokens:
			if PUNCT.match(word):
				continue
			words += 1
			if word == "'s":
				characters += 2
			else:
				characters += sum(1 for char in word
						if char.isdigit() or char.isalpha() or char == '-')
				syll = syllcount(word)
				syllable_count += syll
				if len(word) >= 7:
					long_words += 1

				# This method must be enhanced. At the moment it only considers
				# the number of syllables in a word. This often results in that
				# too many complex words are detected.
				if syll >= 3:
					if not word[0].isupper():
						complex_words += 1

		self.stats = collections.OrderedDict([
				('chars', characters),
				('words', words),
				('avg_chars_per_word', characters / words),
				('syllables', syllable_count),
				('avg_syll_per_word', syllable_count / words),
				('complex_words', complex_words),
				('long_words', long_words),
				('sentences', sentence_count),
				('avg_words_per_sent', words / sentence_count),
				('paragraphs', paragraph_count),
				('sent_per_paragraph', sentence_count / paragraph_count),
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
		return (4.71 * (self.stats['chars'] / self.stats['words'])
				+ 0.5 * (self.stats['words']
				/ self.stats['sentences']) - 21.43)

	def FleschReadingEase(self):
		return (206.835
				- 84.6 * (self.stats['syllables'] / self.stats['words'])
				- 1.015 * self.stats['avg_words_per_sent'])

	def FleschKincaidGradeLevel(self):
		return 0.39 * (self.stats['avg_words_per_sent']) + 11.8 * (
				self.stats['syllables'] / self.stats['words']) - 15.59

	def GunningFogIndex(self):
		return 0.4 * ((self.stats['avg_words_per_sent']) + (100 * (
				self.stats['complex_words'] / self.stats['words'])))

	def SMOGIndex(self):
		return (math.sqrt(self.stats['complex_words']
				* (30 / self.stats['sentences'])) + 3)

	def ColemanLiauIndex(self):
		#return (5.89 * (self.stats['chars'] / self.stats['words'])
		#		) - (30 * (self.stats['sentences'] /
		#			self.stats['words'])) - 15.8
		return (5.879851 * self.stats['chars'] / self.stats['words']
				- 29.587280 * self.stats['sentences'] / self.stats['words']
				- 15.800804)

	def LIX(self):
		return self.stats['words'] / self.stats['sentences'] + (
				100 * self.stats['long_words']) / self.stats['words']

	def RIX(self):
		return self.stats['long_words'] / self.stats['sentences']


def main():
	shortoptions = 'hL:'
	options = 'help lang='.split()
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], shortoptions, options)
	except getopt.GetoptError as err:
		print('error: %r\n%s' % (err, __doc__ % (
				sys.argv[0], ', '.join(syllables.COUNT))))
		sys.exit(2)
	opts = dict(opts)
	if '--help' in opts or '-h' in opts:
		print(__doc__ % (sys.argv[0], ', '.join(syllables.COUNT)))
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

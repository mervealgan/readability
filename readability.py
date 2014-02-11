"""Simple readability measures.

Usage: %s [--lang=<x>] [file]

By default, input is read from standard input.
Text should be encoded with UTF-8,
one sentence per line, tokens space-separated.

Options:
  -L, --lang=<x>   set language for syllabification (available: %s)."""
from __future__ import division, print_function, unicode_literals
import io
import re
import sys
import math
import codecs
import getopt
import collections
from langdata import LANGDATA

PUNCT = re.compile(r"^\W+$", re.UNICODE)


class Readability:
	def __init__(self, text, lang='en'):
		"""text is an iterable with one sentence per line
		and space separated tokens."""
		characters = 0
		words = 0
		syllable_count = 0
		complex_words = 0
		long_words = 0
		paragraph_count = 1
		sentence_count = 0
		syllcounter = LANGDATA[lang]['syllables']
		wordusageregexps = LANGDATA[lang]['words']
		beginningsregexps = LANGDATA[lang]['beginnings']
		self.wordusage = collections.OrderedDict([(name, 0) for name, regexp
				in wordusageregexps.items()])
		self.beginnings = collections.OrderedDict([(name, 0) for name, regexp
				in beginningsregexps.items()])

		for sent in text:
			sent = sent.strip()
			if not sent:
				paragraph_count += 1
			sentence_count += 1
			for token in sent.split():
				if PUNCT.match(token):
					continue
				words += 1
				characters += len(token)
				syll = syllcounter(token)
				syllable_count += syll
				if len(token) >= 7:
					long_words += 1

				# This method could be improved. At the moment it only
				# considers the number of syllables in a word. This often
				# results in that too many complex words are detected.
				if syll >= 3 and not token[0].isupper():  # ignore proper nouns
					complex_words += 1

			for name, regexp in wordusageregexps.items():
				self.wordusage[name] += sum(1 for _ in regexp.finditer(sent))
			for name, regexp in beginningsregexps.items():
				self.beginnings[name] += regexp.match(sent) is not None

		self.stats = collections.OrderedDict([
				('chars', characters),
				('syllables', syllable_count),
				('words', words),
				('sentences', sentence_count),
				('paragraphs', paragraph_count),
				('avg_chars_per_word', characters / words),
				('avg_syll_per_word', syllable_count / words),
				('avg_words_per_sent', words / sentence_count),
				('sent_per_paragraph', sentence_count / paragraph_count),
				('long_words', long_words),
				('complex_words', complex_words),
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
				sys.argv[0], ', '.join(LANGDATA))))
		sys.exit(2)
	opts = dict(opts)
	if '--help' in opts or '-h' in opts:
		print(__doc__ % (sys.argv[0], ', '.join(LANGDATA)))
		return
	if len(args) == 0:
		text = codecs.getreader('utf-8')(sys.stdin)
	elif len(args) == 1:
		text = io.open(args[0], encoding='utf-8')
	else:
		raise ValueError('expected 0 or 1 file argument.')

	rd = Readability(text, opts.get('--lang', opts.get('-L', 'en')))
	print('readability grades:')
	for key, val in rd.readability.items():
		print('\t%s: %g' % (key, round(val, 2)))
	print('sentence info:')
	for key, val in rd.stats.items():
		print('\t%s: %g' % (key, round(val, 2)))
	print('word usage:')
	for key, val in rd.wordusage.items():
		print('\t%s: %g' % (key, round(val, 2)))
	print('sentence beginnings:')
	for key, val in rd.beginnings.items():
		print('\t%s: %g' % (key, round(val, 2)))

if __name__ == "__main__":
	main()

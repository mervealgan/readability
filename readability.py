"""Simple readability measures.

Usage: %s [--lang=<x>] [file]

By default, input is read from standard input.
Text should be encoded with UTF-8,
one sentence per line, tokens space-separated.

Options:
  -L, --lang=<x>   set language (available: %s)."""
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


def getmeasures(text, lang='en'):
	"""Collect surface characteristics of a tokenized text.

	>>> text = "A tokenized sentence .\\nAnother sentence ."
	>>> result = getmeasures(text.splitlines())
	>>> result['sentence info']['words'] == 5
	True

	:param text: an iterable returning lines, one sentence per line
		of space separated tokens.
	:param lang: a language code to select the syllabification procedure and
		word types to count.
	:returns: a two-level ordered dictionary with measurements."""
	characters = 0
	words = 0
	syllables = 0
	complex_words = 0
	long_words = 0
	paragraphs = 1
	sentences = 0
	syllcounter = LANGDATA[lang]['syllables']
	wordusageregexps = LANGDATA[lang]['words']
	beginningsregexps = LANGDATA[lang]['beginnings']

	wordusage = collections.OrderedDict([(name, 0) for name, regexp
			in wordusageregexps.items()])
	beginnings = collections.OrderedDict([(name, 0) for name, regexp
			in beginningsregexps.items()])

	for sent in text:
		sent = sent.strip()
		if not sent:
			paragraphs += 1
		sentences += 1
		for token in sent.split():
			if PUNCT.match(token):
				continue
			words += 1
			characters += len(token)
			syll = syllcounter(token)
			syllables += syll
			if len(token) >= 7:
				long_words += 1

			# This method could be improved. At the moment it only
			# considers the number of syllables in a word. This often
			# results in that too many complex words are detected.
			if syll >= 3 and not token[0].isupper():  # ignore proper nouns
				complex_words += 1

		for name, regexp in wordusageregexps.items():
			wordusage[name] += sum(1 for _ in regexp.finditer(sent))
		for name, regexp in beginningsregexps.items():
			beginnings[name] += regexp.match(sent) is not None

	if not words:
		raise ValueError("I can't do this, there's no words there!")

	stats = collections.OrderedDict([
			('characters', characters),
			('syllables', syllables),
			('words', words),
			('sentences', sentences),
			('paragraphs', paragraphs),
			('long_words', long_words),
			('complex_words', complex_words),
			('chars_per_word', characters / words),
			('syll_per_word', syllables / words),
			('words_per_sent', words / sentences),
			('sent_per_paragraph', sentences / paragraphs),
		])
	readability = collections.OrderedDict([
			('Kincaid', KincaidGradeLevel(syllables, words, sentences)),
			('ARI', ARI(characters, words, sentences)),
			('ColemanLiauIndex',
				ColemanLiauIndex(characters, words, sentences)),
			('FleschReadingEase',
				FleschReadingEase(syllables, words, sentences)),
			('GunningFogIndex',
				GunningFogIndex(words, complex_words, sentences)),
			('LIX', LIX(words, long_words, sentences)),
			('SMOGIndex', SMOGIndex(complex_words, sentences)),
			('RIX', RIX(long_words, sentences)),
		])

	return collections.OrderedDict([
		('readability grades', readability),
		('sentence info', stats),
		('word usage', wordusage),
		('sentence beginnings', beginnings),
		])


def KincaidGradeLevel(syllables, words, sentences):
	return 11.8 * (syllables / words) + 0.39 * ((words / sentences)) - 15.59


def ARI(characters, words, sentences):
	return 4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43


def ColemanLiauIndex(characters, words, sentences):
	return (5.879851 * characters / words - 29.587280 * sentences / words
			- 15.800804)


def FleschReadingEase(syllables, words, sentences):
	return 206.835 - 84.6 * (syllables / words) - 1.015 * (words / sentences)


def GunningFogIndex(words, complex_words, sentences):
	return 0.4 * (((words / sentences)) + (100 * (complex_words / words)))


def LIX(words, long_words, sentences):
	return words / sentences + (100 * long_words) / words


def SMOGIndex(complex_words, sentences):
	return math.sqrt(complex_words * (30 / sentences)) + 3


def RIX(long_words, sentences):
	return long_words / sentences


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

	lang = opts.get('--lang', opts.get('-L', 'en'))
	for cat, data in getmeasures(text, lang).items():
		print(cat + ':')
		for key, val in data.items():
			print(('    %-20s %12.2f' % (key + ':', val)
					).rstrip('0 ').rstrip('.'))

if __name__ == "__main__":
	main()

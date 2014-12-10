"""Simple readability measures.

Usage: %(cmd)s [--lang=<x>] [FILE]
or: %(cmd)s [--lang=<x>] --csv FILES...

By default, input is read from standard input.
Text should be encoded with UTF-8,
one sentence per line, tokens space-separated.

Options:
  -L, --lang=<x>   Set language (available: %(lang)s).
  --csv            Produce a table in comma separated value format on
                   standard output given one or more filenames."""

from __future__ import division, print_function, unicode_literals
import io
import os
import re
import sys
import math
import codecs
import getopt
import collections
from readability.langdata import LANGDATA

TOKENRE = re.compile(r"\b[-\w]+\b", re.UNICODE)


def getmeasures_iter(text, lang='en', merge=False):
	"""Collect surface characteristics of a tokenized text.

	>>> text = "A tokenized sentence .\\nAnother sentence ."
	>>> result = getmeasures_iter(text.splitlines())
	>>> result['sentence info']['words'] == 5
	True

	:param text: an iterable returning lines, one sentence per line
		of space separated tokens.
	:param lang: a language code to select the syllabification procedure and
		word types to count.
	:param merge: if ``True``, return a dictionary results into a single
		dictionary of key-value pairs.
	:returns: a two-level ordered dictionary with measurements."""
	characters = 0
	words = 0
	syllables = 0
	complex_words = 0
	long_words = 0
	paragraphs = 0
	sentences = 0
	syllcounter = LANGDATA[lang]['syllables']
	wordusageregexps = LANGDATA[lang]['words']
	beginningsregexps = LANGDATA[lang]['beginnings']

	wordusage = collections.OrderedDict([(name, 0) for name, regexp
			in wordusageregexps.items()])
	beginnings = collections.OrderedDict([(name, 0) for name, regexp
			in beginningsregexps.items()])

	prevempty = True
	for sent in text:
		sent = sent.strip()

		if prevempty and sent:
			paragraphs += 1
		elif not sent:
			prevempty = True
			continue
		prevempty = False

		sentences += 1
		for token in TOKENRE.findall(sent):
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
			('characters_per_word', characters / words),
			('syll_per_word', syllables / words),
			('words_per_sentence', words / sentences),
			('sentences_per_paragraph', sentences / paragraphs),
			('characters', characters),
			('syllables', syllables),
			('words', words),
			('sentences', sentences),
			('paragraphs', paragraphs),
			('long_words', long_words),
			('complex_words', complex_words),
		])
	readability = collections.OrderedDict([
			('Kincaid', KincaidGradeLevel(syllables, words, sentences)),
			('ARI', ARI(characters, words, sentences)),
			('Coleman-Liau',
				ColemanLiauIndex(characters, words, sentences)),
			('FleschReadingEase',
				FleschReadingEase(syllables, words, sentences)),
			('GunningFogIndex',
				GunningFogIndex(words, complex_words, sentences)),
			('LIX', LIX(words, long_words, sentences)),
			('SMOGIndex', SMOGIndex(complex_words, sentences)),
			('RIX', RIX(long_words, sentences)),
		])

	if merge:
		readability.update(stats)
		readability.update(wordusage)
		readability.update(beginnings)
		return readability
	return collections.OrderedDict([
		('readability grades', readability),
		('sentence info', stats),
		('word usage', wordusage),
		('sentence beginnings', beginnings),
		])


def getmeasures_str(text, lang='en', merge=False):
	"""Collect surface characteristics of a tokenized text.

	>>> text = "A tokenized sentence .\\nAnother sentence ."
	>>> result = getmeasures_str(text)
	>>> result['sentence info']['words'] == 5
	True

	:param text: a string with one sentence per line
		of space separated tokens.
	:param lang: a language code to select the syllabification procedure and
		word types to count.
	:param merge: if ``True``, return a dictionary results into a single
		dictionary of key-value pairs.
	:returns: a two-level ordered dictionary with measurements."""
	characters = 0
	words = 0
	syllables = 0
	complex_words = 0
	long_words = 0
	syllcounter = LANGDATA[lang]['syllables']
	wordusageregexps = LANGDATA[lang]['words']
	beginningsregexps = LANGDATA[lang]['beginnings']

	wordusage = collections.OrderedDict([(name, 0) for name, regexp
			in wordusageregexps.items()])
	beginnings = collections.OrderedDict([(name, 0) for name, regexp
			in beginningsregexps.items()])

	paragraphs = sum(1 for _ in re.compile('\n\n+').finditer(text)) + 1
	sentences = sum(1 for _ in re.compile('[^\n]+(\n|$)').finditer(text))
	# paragraphs = text.count('\n\n')
	# sentences = text.count('\n') - paragraphs
	for token in TOKENRE.findall(text):
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
		wordusage[name] += sum(1 for _ in regexp.finditer(text))
	for name, regexp in beginningsregexps.items():
		beginnings[name] += sum(1 for _ in regexp.finditer(text))

	if not words:
		raise ValueError("I can't do this, there's no words there!")

	stats = collections.OrderedDict([
			('characters_per_word', characters / words),
			('syll_per_word', syllables / words),
			('words_per_sentence', words / sentences),
			('sentences_per_paragraph', sentences / paragraphs),
			('characters', characters),
			('syllables', syllables),
			('words', words),
			('sentences', sentences),
			('paragraphs', paragraphs),
			('long_words', long_words),
			('complex_words', complex_words),
		])
	readability = collections.OrderedDict([
			('Kincaid', KincaidGradeLevel(syllables, words, sentences)),
			('ARI', ARI(characters, words, sentences)),
			('Coleman-Liau',
				ColemanLiauIndex(characters, words, sentences)),
			('FleschReadingEase',
				FleschReadingEase(syllables, words, sentences)),
			('GunningFogIndex',
				GunningFogIndex(words, complex_words, sentences)),
			('LIX', LIX(words, long_words, sentences)),
			('SMOGIndex', SMOGIndex(complex_words, sentences)),
			('RIX', RIX(long_words, sentences)),
		])

	if merge:
		readability.update(stats)
		readability.update(wordusage)
		readability.update(beginnings)
		return readability
	return collections.OrderedDict([
		('readability grades', readability),
		('sentence info', stats),
		('word usage', wordusage),
		('sentence beginnings', beginnings),
		])


def getdataframe(filenames, lang='en', encoding='utf8'):
	"""Return a pandas DataFrame with readability measures for a list of files.
	"""
	import pandas
	filenames = list(filenames)
	return pandas.DataFrame([getmeasures_str(
				io.open(name, encoding=encoding).read(),
				lang=lang,
				merge=True)
			for name in filenames], index=filenames)


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
	options = 'help csv lang='.split()
	cmd = os.path.basename(sys.argv[0])
	usage = __doc__ % dict(cmd=cmd, lang=', '.join(LANGDATA))
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], shortoptions, options)
	except getopt.GetoptError as err:
		print('error: %r\n%s' % (err, usage))
		sys.exit(2)
	opts = dict(opts)
	lang = opts.get('--lang', opts.get('-L', 'en'))

	try:
		if '--help' in opts or '-h' in opts:
			print(usage)
			return
		elif '--csv' in opts:
			result = getdataframe(args, lang=lang)
			result.to_csv(sys.stdout)
			return
		elif len(args) == 0:
			result = getmeasures_iter(
					codecs.getreader('utf-8')(sys.stdin),
					lang)
		elif len(args) == 1:
			result = getmeasures_str(
					io.open(args[0], encoding='utf-8').read(),
					lang)
		else:
			raise ValueError('expected 0 or 1 file argument.')
		for cat, data in result.items():
			print(cat + ':')
			for key, val in data.items():
				print(('    %-20s %12.2f' % (key + ':', val)
						).rstrip('0 ').rstrip('.'))
	except KeyboardInterrupt:
		sys.exit(1)

if __name__ == "__main__":
	main()

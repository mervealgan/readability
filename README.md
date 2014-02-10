Readability
====================

A collection of functions that measure the readability of a given body of text.
I'd recommend checking out the wikipedia articles below--most of the metrics
estimate the grade level required to comprehend a given block of text and may
return odd results on small snippets of text.

Usage: readability.py [--lang=<x>] [file]

By default, input is read from standard input.
Text should be encoded with UTF-8,
one sentence per line, tokens space-separated.

  -L, --lang=<x>   set language for syllabification (default: en).

Demo:

    $ ucto -L en -n -s '' sometext.txt | python readability.py
	readability grades:
			FleschKincaidGradeLevel: 7.69
			ARI: 9.29
			ColemanLiauIndex: 13.95
			FleschReadingEase: 52.11
			GunningFogIndex: 7.02
			LIX: 33.14
			SMOGIndex: 7.69
			RIX: 1.8
	sentence info:
			char_cnt: 1785
			word_cnt: 308
			avg_char_p_word: 5.8
			syllable_cnt: 538
			avg_syll_p_word: 1.75
			complex_word_cnt: 33
			sentence_cnt: 45
			avg_words_p_sentence: 6.84


The following readability metrics are included in readability.py:

1. http://en.wikipedia.org/wiki/Automated_Readability_Index
2. http://en.wikipedia.org/wiki/SMOG
3. http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_Grade_Level#Flesch.E2.80.93Kincaid_Grade_Level
4. http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_test#Flesch_Reading_Ease
5. http://en.wikipedia.org/wiki/Coleman-Liau_Index
6. http://en.wikipedia.org/wiki/Gunning-Fog_Index

The code is based on:

	https://github.com/mmautner/readability

Which in turn was based on:

    https://github.com/nltk/nltk_contrib/tree/master/nltk_contrib/readability

SMOG index appears to perform most accurately.

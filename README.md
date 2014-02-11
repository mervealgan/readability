Readability
====================

A collection of functions that measure the readability of a given body of text.
The functionality is modeled after the UNIX style(1) command. Compared to the
implmentation as part of GNU diction, this version supports UTF-8 encoded text.

	$ python readability.py --help
	Simple readability measures.

	Usage: readability.py [--lang=<x>] [file]

	By default, input is read from standard input.
	Text should be encoded with UTF-8,
	one sentence per line, tokens space-separated.

	  -L, --lang=<x>   set language for syllabification (available: de, nl, en).

Demo:

    $ python readability.py LICENSE.txt
	readability grades:
		FleschKincaidGradeLevel: 7.53
		ARI: 8.09
		ColemanLiauIndex: 12.35
		FleschReadingEase: 55.52
		GunningFogIndex: 8.18
		LIX: 43.9
		SMOGIndex: 8.48
		RIX: 2.9
	sentence info:
		chars: 438
		words: 81
		avg_chars_per_word: 5.41
		syllables: 137
		avg_syll_per_word: 1.69
		complex_words: 10
		long_words: 29
		sentences: 10
		avg_words_per_sent: 8.1
		paragraphs: 3
		sent_per_paragraph: 3.33

For proper results, the text should be tokenized, for example using 'ucto':

	$ ucto -L en -n -s '' "CONRAD, Joseph - Lord Jim.txt" | python readability.py
	readability grades:
			FleschKincaidGradeLevel: 5.79
			ARI: 6.38
			ColemanLiauIndex: 6.92
			FleschReadingEase: 82.69
			GunningFogIndex: 9.94
			LIX: 32.25
			SMOGIndex: 9.46
			RIX: 2.6
	sentence info:
			chars: 553643
			words: 132780
			avg_chars_per_word: 4.17
			syllables: 168809
			avg_syll_per_word: 1.27
			complex_words: 11306
			long_words: 21122
			sentences: 8124
			avg_words_per_sent: 16.34
			paragraphs: 699
			sent_per_paragraph: 11.62

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

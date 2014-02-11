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


For proper results, the text should be tokenized, for example using [ucto](http://ilk.uvt.nl/ucto):

	$ ucto -L en -n -s '' "CONRAD, Joseph - Lord Jim.txt" | python readability.py
	readability grades:
		Kincaid:                     4.95
		ARI:                         5.78
		ColemanLiauIndex:            6.87
		FleschReadingEase:          86.18
		GunningFogIndex:             9.4
		LIX:                        30.97
		SMOGIndex:                   9.2
		RIX:                         2.39
	sentence info:
		characters:             552074
		syllables:              164207
		words:                  131668
		sentences:                8823
		paragraphs:                700
		long_words:              21122
		complex_words:           11306
		chars_per_word:              4.19
		syll_per_word:               1.25
		words_per_sent:             14.92
		sent_per_paragraph:         12.6
	word usage:
		tobeverb:                 3909
		auxverb:                  1632
		conjunction:              4413
		pronoun:                 18104
		preposition:             19271
		nominalization:           1216
	sentence beginnings:
		pronoun:                  2593
		interrogative:             215
		article:                   632
		subordination:             124
		conjunction:               240
		preposition:               404


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

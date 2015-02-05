Readability
===========

A collection of functions that measure the readability of a given body of text
using surface characteristics. These measures are basically linear regressions
based on the number of words, syllables, and sentences.

The functionality is modeled after the UNIX ``style(1)`` command. Compared to the
implementation as part of `GNU diction <http://www.moria.de/~michael/diction/>`_,
this version supports UTF-8 encoded text, but expects sentence-segmented and
tokenized text. The syllabification and word type recognition is based on
simple heuristics and only provides a rough measure.

NB: all readability formulas were developed for English, so the scales of the
outcomes are only meaningful for English texts.

Installation
------------
::

    $ pip install https://github.com/andreasvc/readability/tarball/master

Usage
-----
::

    $ readability --help
    Simple readability measures.

    Usage: readability [--lang=<x>] [FILE]
    or: readability [--lang=<x>] --csv FILES...

    By default, input is read from standard input.
    Text should be encoded with UTF-8,
    one sentence per line, tokens space-separated.

    Options:
      -L, --lang=<x>   Set language (available: de, nl, en).
      --csv            Produce a table in comma separated value format on
                       standard output given one or more filenames.
      --tokenizer=<x>  Specify a tokenizer including options that will be given
                       each text on stdin and should return tokenized output on
                       stdout. Not applicable when reading from stdin.

For proper results, the text should be tokenized.

- For English, I recommend "tokenizer",
  cf. http://moin.delph-in.net/WeSearch/DocumentParsing
- For Dutch, I recommend the tokenizer that is part of the Alpino parser:
  http://www.let.rug.nl/vannoord/alp/Alpino/.
- ``ucto`` is a  general multilingual tokenizer: http://ilk.uvt.nl/ucto

Example using ``ucto``::

    $ ucto -L en -n -s '' "CONRAD, Joseph - Lord Jim.txt" | readability
    [...]
    readability grades:
        Kincaid:                     4.95
        ARI:                         5.78
        Coleman-Liau:                6.87
        FleschReadingEase:          86.18
        GunningFogIndex:             9.4
        LIX:                        30.97
        SMOGIndex:                   9.2
        RIX:                         2.39
    sentence info:
        characters_per_word:         4.19
        syll_per_word:               1.25
        words_per_sentence:         14.92
        sentences_per_paragraph:        12.6
        characters:             552074
        syllables:              164207
        words:                  131668
        sentences:                8823
        paragraphs:                700
        long_words:              21122
        complex_words:           11306
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

The option ``--csv`` collects readability measures for a number of texts in
a table. To tokenize documents on-the-fly when using this option, use
the ``--tokenizer`` option. Example with the "tokenize" tool::

    $ readability --csv --tokenizer='tokenizer -L en-u8 -P -S -E "" -N' */*.txt >readabilitymeasures.csv

References
----------
The following readability metrics are included:

1. http://en.wikipedia.org/wiki/Automated_Readability_Index
2. http://en.wikipedia.org/wiki/SMOG
3. http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_Grade_Level#Flesch.E2.80.93Kincaid_Grade_Level
4. http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_test#Flesch_Reading_Ease
5. http://en.wikipedia.org/wiki/Coleman-Liau_Index
6. http://en.wikipedia.org/wiki/Gunning-Fog_Index

For better readability measures, consider the following:

- Collins-Thompson & Callan (2004). A language modeling approach to predicting reading difficulty.
  In Proc. of HLT/NAACL, pp. 193-200. http://aclweb.org/anthology/N04-1025.pdf
- Schwarm & Ostendorf (2005). Reading level assessment using SVM and statistical language models.
  Proc. of ACL, pp. 523-530. http://www.aclweb.org/anthology/P05-1065.pdf
- The Lexile framework for reading. http://www.lexile.com
- Coh-Metrix. http://cohmetrix.memphis.edu/
- Stylene: http://www.clips.ua.ac.be/category/projects/stylene
- T-Scan: http://languagelink.let.uu.nl/tscan

Acknowledgments
---------------
The code is based on: https://github.com/mmautner/readability

Which in turn was based on: https://github.com/nltk/nltk_contrib/tree/master/nltk_contrib/readability

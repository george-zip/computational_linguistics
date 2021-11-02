"""
Tokenizes text and extracts unigrams and bigrams then prints them out with their unsmoothed probabilities:
unigrams: their probability of occurring based on the evidence of this corpus
bigrams: the conditional probability of the second word given the the first
Note: Requires nltk and tabulate libraries to run
pip install nltk
pip install tabulate
"""

from collections import defaultdict
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.lm.preprocessing import pad_both_ends, flatten
from tabulate import tabulate
import sys

# Get text to be analyzed from stdin
text = ""
for line in sys.stdin:
	# normalize to lower case
	text += line.lower()

# Segment sentences and tokenize words
tokenizer = RegexpTokenizer(r"\w+")
sentences = [tokenizer.tokenize(sent) for sent in sent_tokenize(text)]
# Add padding symbols
padded = [list(pad_both_ends(token_sent, n=2)) for token_sent in sentences]
# Create corpus from flattened stream of tokenized words
corpus = list(flatten(padded))

unigram_counts = defaultdict(lambda: 0)
bigram_counts = defaultdict(lambda: 0)

i = 1
j = 0
# generate the raw counts
while i < len(corpus):
	bigram_counts[(corpus[j], corpus[i])] += 1
	unigram_counts[corpus[j]] += 1
	i += 1
	j += 1

unigram_counts[corpus[-1]] += 1

# find the count for each word
word_counts = {word: corpus.count(word) for word in corpus}

unigram_table = sorted(
	[(word, unigram_counts[word] / len(word_counts)) for word in unigram_counts],
	key=lambda x: x[1],
	reverse=True
)
print(tabulate(unigram_table, headers=["unigram", "probability"]))

print()

bigram_table = sorted(
	[(f"{pair[0]} {pair[1]}", bigram_counts[pair] / word_counts[pair[0]]) for pair in bigram_counts],
	key=lambda x: x[1],
	reverse=True
)
print(tabulate(bigram_table, headers=["bigram", "probability"]))


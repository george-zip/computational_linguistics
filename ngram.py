"""
Calculates the unsmoothed probability for a given bigram
from an excerpt from Green Eggs and Ham
"""

from collections import defaultdict

corpus = [
	"<s>", "I", "am", "Sam", "</s>",
	"<s>", "Sam", "I", "am", "</s>",
	"<s>", "I", "am", "Sam", "</s>",
	"<s>", "I", "do", "not", "like", "green", "eggs", "and", "Sam", "</s>"
]

bigram_counts = defaultdict(lambda: 0)

i = 1
j = 0
# calculate the raw bigram counts
while i < len(corpus):
	bigram_counts[(corpus[j], corpus[i])] += 1
	i += 1
	j += 1

# find the count for each word
word_counts = {word: corpus.count(word) for word in corpus}

# normalize the bigram counts by the total count of the first word
# in the pair
bigram_probabilities = defaultdict(lambda: 0)
for pair in bigram_counts:
	bigram_probabilities[pair] = bigram_counts[pair] / word_counts[pair[0]]

# P(Sam|am) is represented by the tuple ("am","Sam")
target_bigram = ("am", "Sam")
print(
	f"The bigram probability for P({target_bigram[1]}|{target_bigram[0]})" \
	f" is {bigram_probabilities[target_bigram]:.3f}"
)

# Output:
# The bigram probability for P(Sam|am) is 0.667

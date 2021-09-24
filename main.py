"""
Byte pair encoding tokenizer: 
Instead of defining tokens as a string of characters with some
delimiter, learn the tokens from a training corpus. 
For k rounds:
1. Scan corpus and select the most common adjacent symbols, c1 and c2.
2. Merge c1 and c2 to form new symbol and add to vocabulary.
3. Replace all co-occurances of c1 and c2 with the new symbol
in the corpus.
The algorithm continues to count and merge for k rounds, creating 
longer symbols. The resulting vocabulary is the original characters
plus k merged symbols. It can then be used to tokenize other strings.
"""
from collections import defaultdict


def most_common_pair(corpus: list) -> tuple:
	"""
	Scans corpus for most common consecutive two symbols and 
	return them as a tuple
	"""
	pair_count = defaultdict(lambda: 0)	
	for pair in zip(corpus[0::], corpus[1::]):
		pair_count[pair] += 1
	max_pair = list(pair_count.keys())[0]
	for key in pair_count:
		if pair_count[key] > pair_count[max_pair]:
			max_pair = key
	return max_pair


def replace_all(corpus: list, c1: str, c2: str):
	"""
	Scans corpus for co-occurances of c1 and c2 
	and replaces them with the merged symbol c1 + c2.
	"""
	new_corpus = []
	i = 0
	j = 1
	while j < len(corpus):
		if corpus[i] == c1 and corpus[j] == c2:
			new_corpus.append(c1 + c2)
			i += 2
		else:
			new_corpus.append(corpus[i])
			i += 1
		j = i + 1
	if i < len(corpus):
		new_corpus.append(corpus[i])
	return new_corpus
		

def byte_pair_encoding(corpus: list, k: int) -> set:
	"""
	Tokenizes corpus for k rounds
	"""
	vocabulary = set(c.lower() for c in corpus)
	for i in range(k):
		c1, c2 = most_common_pair(corpus)
		token = c1 + c2
		vocabulary.add(token)
		corpus = replace_all(corpus, c1, c2)
	return vocabulary


words = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ac mauris vitae lacus tincidunt efficitur. Donec vitae semper nunc, a condimentum eros. Cras tempor vestibulum auctor. Integer eleifend tempor felis, sed faucibus lectus fermentum nec. Ut at semper nibh. Donec egestas consectetur orci vel tincidunt. In vitae ullamcorper est. Ut interdum vitae sapien id consequat. Pellentesque luctus iaculis lectus, non aliquet leo lobortis ac. Etiam mollis enim sed dignissim vulputate. Etiam sit amet consectetur libero. Donec consectetur lacus id pretium auctor. Vestibulum varius pellentesque tincidunt. Sed ultricies, nisi vitae semper sodales, odio leo condimentum mi, mollis luctus justo ipsum a diam. Nunc porta tempor augue vitae pellentesque. Sed ut condimentum ante. Nulla quis magna ut tortor suscipit fermentum. Nam ullamcorper, dui fringilla scelerisque molestie, quam quam aliquet ante, et consectetur diam dolor sed sem. Etiam ultricies, ante et laoreet porttitor, leo est tincidunt odio, nec pellentesque sem nibh sed nibh. Nunc auctor bibendum risus sed finibus. Proin laoreet lacus ut rhoncus porta. Vivamus pharetra, ante sed mattis efficitur, nunc mi mollis erat, a dapibus elit tellus nec lorem. Duis tincidunt, mauris sed ultrices congue, quam justo commodo urna, nec elementum tortor lacus in lacus. Vestibulum eu nibh eu ligula ornare.
"""

corpus = [c for c in words]
print(byte_pair_encoding(corpus, 75))
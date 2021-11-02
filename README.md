## Detecting cognates using the minimum edit distance (MED) algorithm with weights

This script calculates the Levenshtein distance between two strings, weighted by the probability that they are 
cognates. It judges whether the two strings are cognates based on a threshold and uses a confusion matrix to assign 
a weight to German and English character pairs. The input to the script is a list of English and German word pairs, 
separated by whitespace.

To run from the command line:

```commandline
python cognate_test.py < input.txt
```

The file `input.txt` contains a English - German pair on each line.

There are a few clear limitations, which would need to be addressed for this to be a proper cognate detection 
algorithm. 

### Confusion Matrix 

I based the matrix on the confusion matrix in Kemighan (1990) that focused on spelling correction. The 
approach involves some major simplifications and workarounds, as follows:

   1. It assigns a weight to individual character pairs (for example t -> d) that are likely to be equivalent in 
      the two languages. A better approach would be for the matrix to encode rules that converts subwords or morphemes. 
      Examples of this is are rules that converts an English 'th' to German 'd' and 'gh' to 'ch'. As this algorithm 
      stands, it misses what look like valid cognates like 'six' and 'sechs.' Such as approach would need to modify 
      the MED algorithm to be able to substitute, insert or delete two or more characters at a time. It 
      would also have to adjust in some way for the weight or cost of a multi-character operation.

   2. We want to assign likely substitution pairs a lower weight, but the original spelling matrix used higher 
      weightings for pairs that were more likely to be confused. The original spelling algorithm (Kemighan, 1990) 
      added character-specific insertion and deletion weights. It also normalized them by the relative frequency of 
      the characters. Since the sample size here is so small however, I’m adopting a heuristic approach of using the 
      matrix weight as a denominator of a fraction that calculates the substitution weight as:

      ```math
      1 / sub[c1, c2]
      ```

      Insertions and deletions will have a fixed cost of 1.

   3. Finally, given the limitations on time, I adapted the weights from an internet source (WikiLists, 2009). I 
      have no idea how accurate and complete these are. It’s also not clear if the weights I’ve assigned to the 
      rules are correct. Much more careful research and experimentation needs to be done here. For a start, we need 
      a corpus of German to know the distribution of spelling combinations. Without knowing how often the English `v` 
      is replaced by `b` in equivalent words, we are shooting in the dark.  

### Threshold  

The script determines whether two strings are cognates on the ratio of the distance to the number of  characters in the 
strings. I don’t imagine this is the optimal formula, but I think it is in the right direction. We want it scaled to the 
size of the strings in some way. In other words, if the distance between two 10-character and two 3-character strings 
is the same, that implies to me that the 10-character strings have a closer relationship.

### Text Normalization

The script normalizes by case folding. Even though the sample input doesn't contain these, there’s obviously a lot more 
that should be done to handle contractions, punctuation and so on. 

There is also the problem of the different character sets in German and English. For now, I’ve worked around the 
issue by associating non-ASCII characters with ASCII equivalents. This is unfortunately hardcoded for
now.

### References

Kemighan, M. D., Church, K., & Gale, W. A. (1990). A spelling correction program based on a noisy channel model. 
In COLING 1990 Volume 2: Papers presented to the 13th International Conference on Computational Linguistics.

List of German cognates with English. WikiLists. (2009, January). Retrieved October 5, 2021, from 
https://list.fandom.com/wiki/List_of_German_cognates_with_English. 

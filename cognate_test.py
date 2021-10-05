from typing import Callable
import sys
import re
import csv


def levenshtein_distance(
		str1: str, str2: str,
		del_weight: Callable[[str, str], int],
		ins_weight: Callable[[str, str], int],
		sub_weight: Callable[[str, str], int]) -> int:
	"""
	Returns the Levenshtein distance between two strings. The cost of insertions, deletions and substitutions is
	calculated by the callables del_weight, ins_weight and sub_weight respectively.
	"""
	m = len(str1)
	n = len(str2)
	distance_table = [[row] for row in range(1, m + 1)]
	distance_table.insert(0, list(range(n + 1)))
	for j in range(1, n + 1):
		for i in range(1, m + 1):
			distance_table[i].insert(
				j,
				min(
					distance_table[i - 1][j] + del_weight(str1[i - 1], str2[j - 1]),
					distance_table[i][j - 1] + ins_weight(str1[i - 1], str2[j - 1]),
					distance_table[i - 1][j - 1] + sub_weight(str1[i - 1], str2[j - 1])
				)
			)
	return distance_table[-1][-1]


def is_cognate(str1: str, str2: str, distance: int, threshold: int = 1) -> bool:
	"""
	Determines whether str1 and str2 are cognates based on the ratio of distance and string-length
	"""
	avg_len = (len(str1) + len(str2)) // 2
	return (distance // avg_len) < threshold


def normalize(input: str) -> str:
	"""
	Normalizes the string by case-folding
	"""
	return input.lower()


def default_weight(_x, _y):
	"""
	Returns default weight
	"""
	return 1


class SingleCharacterSubstitution:

	def __init__(self, weight_matrix):
		self.weight_matrix = weight_matrix

	@staticmethod
	def char_to_index(char):
		# this is a very ugly and limited work-around for the different German and English character sets.
		# It would be better to extend the German dimension of the weight matrix but given this assignment is
		# due tomorrow, this will have to suffice.
		if char == 'ü':
			return 20
		elif char == 'ö':
			return 14
		elif char == 'ä':
			return 0
		elif char == 'ß':
			return 18
		return ord(char) - 97

	def sub_weight(self, x, y):
		weight = int(self.weight_matrix[self.char_to_index(x)][self.char_to_index(y)])
		if weight == 0:
			return 1
		else:
			return 1 / weight


def import_weights(matrix_file_path):
	with open(matrix_file_path) as f:
		reader = csv.reader(f)
		return list(reader)


def main():
	matrix_file_path = sys.argv[1] if len(sys.argv) > 2 else "./matrix.csv"
	sub = SingleCharacterSubstitution(import_weights(matrix_file_path))
	for line in sys.stdin:
		str1, str2 = re.search("^(\w+)\W+(\w+)", line).groups()[:2]
		distance = levenshtein_distance(
			normalize(str1), normalize(str2),
			default_weight, default_weight, sub.sub_weight
		)
		if is_cognate(str1, str2, distance):
			print(f"{str1} and {str2} seem to be cognates. Calculated distance: {distance:.2f}")
		else:
			print(f"{str1} and {str2} do NOT seem to be cognates. Calculated distance: {distance:.2f}")


if __name__ == '__main__':
	main()

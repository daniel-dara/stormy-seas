#!/usr/local/bin/python3


class Boat:
	def __init__(self, row, column, size):
		self.row = row
		self.column = column
		self.size = size

	def __repr__(self):
		return 'Boat' + str([self.row, self.column, self.size])


# This string defines the visible state of the waves on the board.
# dashes (-) are open spaces
# number signs (#) are blocked spaces
startingWaveConfiguration = """
--#-#-###
--#-###-#
--#-##-##
--#-#-###
--#-#-###
--#-###-#
-##0##-#-
###0###--
"""

# The row and column that the top part of the 0-ship must reach to solve the problem.
solveLocation = (6, 5)

# 2D array of booleans where 'false' is an empty space and 'true' is an occupied space.
waves = []

# Array of integers (between 0 and 2 inclusive) that indicate the offset of the wave of the same index.
waveOffsets = []

# Map of boat identifiers (number) to the list of coordinates (row, col) representing the pieces of the boat.
boats = {}

for row, line in enumerate(startingWaveConfiguration.strip().split('\n')):
	# Determine the boat locations.
	for column, boat in filter(lambda x: x[1].isdigit(), enumerate(line)):
		if boat not in boats:
			boats[boat] = Boat(row, column, 1)
		else:
			boats[boat].size += 1

	firstBlockedIndex = line.index('#')

	# Every wave has two empty spaces on each end. To simplify parsing the starting configuration, only the visible
	# spaces were defined. However the empty spaces must be added back before solving the problem since they do exist.
	fullLine = (2 - firstBlockedIndex) * '-' + line + firstBlockedIndex * '-'

	# Convert the characters to booleans.
	waves.append([bool(character != '-') for character in fullLine])

	# Determine the horizontal offset of the wave based on how many empty spaces were added to the front.
	waveOffsets.append(2 - firstBlockedIndex)

for wave in waves:
	print(wave)

print(waveOffsets)
print(boats)

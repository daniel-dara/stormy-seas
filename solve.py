#!/usr/local/bin/python3

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

winLocation = (5, 8)

waves = []
wavePositions = []

for line in startingWaveConfiguration.strip().split('\n'):
	firstBlockedIndex = line.index('#')

	# Every wave has two empty spaces on each end. To simplify parsing the starting
	# configuration, these spaces are left out and only the ones that are visible
	# are defined. However these empty spaces must be added back before solving the
	# problem since they do exist.
	fullLine = (2 - firstBlockedIndex) * '-' + line + firstBlockedIndex * '-'

	# Convert the characters to booleans
	waves.append([bool(character == '#') for character in fullLine])

	# Determine which horizontal position the wave is in based on how many of the
	# empty spaces are showing in front of the wave.
	wavePositions.append(2 - firstBlockedIndex)

for wave in waves:
	print(wave)

print(wavePositions)

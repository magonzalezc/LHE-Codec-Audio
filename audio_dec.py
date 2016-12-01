"""

This module gets and saves the decoded audio, given its symbols lists.

"""
# LHE Codec for Audio
# Author: Eduardo Rodes Pastor

import struct, wave
from example import calculateHops

# --------------#
# AUDIO DECODER #
# --------------#

#*******************************************************************************#
#	Function symbolsToHops: Given a list of symbols, this returns a list of the #
#	hops they represent. We will use a list called distribution which will work #
#	as a dictionary.                                                            #
#	Input: Symbols list.                                                        #
#	Output: Hops list.                                                          #
#*******************************************************************************#

def symbolsToHops(sym): 
	"""Transforms a symbols list into its respective hops one.

	Parameters: symbols list (integers from 1 to 9)

	Exceptions: This function does not throw an exception.

	"""

	hops = [0] * len(sym)

	distribution = [4, 5, 3, 6, 2, 7, 1, 8, 0] # Distribution of hops (0, +1, -1, +2...)

	# Hop calculation
	for i in range(0, len(sym)):

		# If the symbol is '1', hop will always be 4. Otherwise, we check distribution:
		if (sym[i] == '1'):
			hops[i] = 4
			continue
		else:
			hops[i] = distribution[int(sym[i])-1]
			continue

	return hops


#*******************************************************************************#
#	Function hopsToSamples: This gets a specific samples list given its hops    #
#	list. This method is similar to GetHops in LHEquantizer, since this is its  #
#	inverse function.                                                           #
#	Input: hops list (integers from 0 to 8), first amplitude value, number of   #
#	samples, maximum sample value and minimum sample value.                     #
#	Output: component samples list (signed integers with 16 bits)               #
#*******************************************************************************#

def hopsToSamples(hops, first_amp, n_samples, max_sample, min_sample):
	"""Returns the audio samples values given their hops list.

	Parameters: hops list (integers from 0 to 8), first amplitude value, number of samples,
	maximum sample value and minimum sample value.

	Exceptions: This function does not throw an exception.

	"""

	# Hop1 interval: [512, 1280], since we are working with 16 bits
	max_hop1 = 2560
	min_hop1 = 1024

	# We start in the center of the interval
	start_hop1 = (max_hop1 + min_hop1) / 2 
	hop1 = start_hop1

	hop0 = 0 # Predicted amplitude signal
	hop_number = 4 # Pre-selected hop -> 4 is null hop
	amp = 0 # Amplitude position, from 0 to image size        
	last_small_hop = "false" # Indicates if last hop is small. Used for h1 adaptation mechanism

	result = [-1] * n_samples  # List where we will save the samples values

	s = 0 # Sample counter

	while (s < n_samples): # # We iterate over all the audio samples

		hop_number = hops[amp]

		# HOP0 PREDICTION #
		# --------------- #

		# We just need the previous amplitude value, since audio amplitude is a continuous function
		if (s > 0):
			hop0 = result[amp-1]
		else:
			hop0 = first_amp # If there isn't previous value, we are in the first sample

		# Assignment of final value
		result[amp] = calculateHops(hop0, hop1, hop_number, max_sample, min_sample) # Final amplitude

		# Tunning hop1 for the next hop ("h1 adaptation")
		small_hop = "false" 
		if (hop_number <= 5 and hop_number >= 3): 
			small_hop = "true" # Hop 4 is in the center and is null
		else:
			small_hop = "false"      

		# If we have small hops, that means we are in a plain zone, so we increase precision
		if (small_hop == "true" and last_small_hop == "true"):
			hop1 = hop1 - 128
			if (hop1 < min_hop1):
				hop1 = min_hop1 
		else:
			hop1 = max_hop1

		# Let's go for the next sample
		last_small_hop = small_hop  
		amp = amp + 1
		s = s + 1

	# We give the result list a more readable format
	for i in range(0, len(result)):
		result[i] = int(result[i]) 

	return result 


#*******************************************************************************#
#	Function getAudio: This gets and saves an audio in .wav format based on the #
#	samples given.                                                              #
#	Input: samples list                                                         #
#	Output: None, just saves the audio in the output_lhe/audio subfolder        #
#*******************************************************************************#

def getAudio(samples):
	"""Saves the new audio in the specified subfolder given its samples values.

	Parameters: Samples values list

	Exceptions: This function will throw an exception if the specified folder
	does not exist.

	"""

	output = wave.open('output_lhe/audio/output_audio.wav', 'w')
	output.setparams((2, 2, 48000, 0, 'NONE', 'not compressed')) # 2 channels, 2 values per sample, 48000 Hz

	values = [] # Decodified amplitude values

	for i in range(0, len(samples)):
		sample = struct.pack('h', samples[i])
		values.append(sample) # Left channel
		values.append(sample) # Right channel

	value_str = ''.join(values)
	output.writeframes(value_str)

	output.close()
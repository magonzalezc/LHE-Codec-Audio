"""

This module gets the hops lists of the 16 bits audio file given.

"""
# LHE Codec for Audio
# Author: Eduardo Rodes Pastor

import struct, wave

# --------------#
# LHE QUANTIZER #
# --------------#

#*******************************************************************************#
#	Function getSamples: Given an audio file, this returns a list of its        #
#	samples (scaled to 16 bits), its length, maximum and minimum value.         #
#	Input: Input audio file                                                     #
#	Output: Samples list, length of it, maximum and minimum sample values.      #
#*******************************************************************************#

def getSamples(filename):
	"""Returns a list of samples of an audio file (scaled to 16 bits), 
	its length, maximum and minimum value.

	Parameters: Input audio file

	Exceptions: This function does not throw an exception.

	"""

	# Loading audio file
	file = wave.open(filename, "r")
	n_samples = file.getnframes()

	data = [0] * n_samples # List where we will save the samples values

	# We don't know how big are the samples, so we extract them with 'l' (32 bits)
	for i in range(0, n_samples):
		waveData = file.readframes(1)
		try:
			data[i] = int(struct.unpack("<h", waveData)[0])
		except:
			data[i] = int(struct.unpack("<hh", waveData)[0])

	# Then we scale the samples (if needed) so they have 16 bits
	# if (max(data) > 32767 or min(data) < 32768):
	# 	data = scaleSamples(data, 32767)

	return data, n_samples, max(data), min(data)


#*******************************************************************************#
#	Function scaleSamples: Given a samples list, this scales them to a          #
#	determined maximum value.                                                   #
#	Input: Samples list, maximum value of the output scaled list.               #
#	Output: Scaled samples list.                                                #
#*******************************************************************************#

def scaleSamples(samples, scaled_max_value):
	"""Returns a list of scaled samples of an audio file based on the
	original samples list.

	Parameters: Original samples list.

	Exceptions: This function does not throw an exception.

	"""

	maximum = max(max(samples), abs(min(samples))) # Maximum absolute value of the list
	ksamp = maximum/scaled_max_value # Scaling factor

	# We scale all the samples
	for i in range(0, len(samples)):
		if (ksamp != 0):
			samples[i] = int(samples[i]/ksamp)

	return samples

def nextHop(acs, prs, hop1):

	max_sample = 32768
	min_sample = -32768
	prs = prs - min_sample
	acs = acs - min_sample

	percent_range = 0.8 # Factor for positive and negative ratios
	rmax = 5.4 # Factor for ratio limits
	hop_result = 0 # Final hop
	sample_result = 0

	# Ratio values for positive hops	
	ratio_pos = pow(percent_range * abs((max_sample - min_sample - 1 - prs)/(hop1)), 0.33333333) 
	
	# Ratio values for negative hops
	ratio_neg = pow(percent_range * abs((prs)/(hop1)), 0.33333333) 	
	
	# Ratio limits
	if (ratio_pos > rmax):
		ratio_pos = rmax 
	if (ratio_neg > rmax):
		ratio_neg = rmax

	# --- AMPLITUDES COMPUTATION --- #

	h4 = prs

	# Amplitude of positive hops
	h5 = prs + hop1
	h6 = int(prs + hop1 * ratio_pos) 
	h7 = int(prs + hop1 * pow(ratio_pos, 2))
	h8 = int(prs + hop1 * pow(ratio_pos, 3))

	# Amplitude of negative hops	
	h3 = prs - hop1
	h2 = int(prs - hop1 * ratio_neg)
	h1 = int(prs - hop1 * pow(ratio_neg, 2))
	h0 = int(prs - hop1 * pow(ratio_neg, 3))

	if ((acs >= h4 and acs < h5) or (acs > h3 and acs <= h4)):
		hop_result = 4
		sample_result = h4
	elif (acs >= h5 and acs < h6):
		hop_result = 5
		sample_result = h5
	elif (acs <= h3 and acs > h2):
		hop_result = 3
		sample_result = h3
	elif (acs >= h6 and acs < h7):
		hop_result = 6
		sample_result = h6
	elif (acs <= h2 and acs > h1):
		hop_result = 2
		sample_result = h2
	elif (acs >= h7 and acs < h8):
		hop_result = 7
		sample_result = h7
	elif (acs <= h1 and acs > h0):
		hop_result = 1
		sample_result = h1
	elif (acs >= h8):
		hop_result = 8
		sample_result = h8
	elif (acs <= h0):
		hop_result = 0
		sample_result = h0

	if (sample_result <= 0):
		sample_result = 1
	if (sample_result > max_sample - min_sample):
		sample_result = max_sample - min_sample - 1

	sample_result = sample_result + min_sample
	return hop_result, sample_result
			
#*******************************************************************************#
#	Function calculateHops: This function calculates the hop assigned to a      #
#	sample, according to the previous one in the following method. This         #
#	is the LHE algorithm, so some knowledge about it is recommended to          #
#	understand better what this function does.                                  #
#	Input: Actual sample value, number of samples to the first hop, previous    #
#	hop value, scaled maximum and minimum sample values.                        #
#	Output: New hop value                                                       #
#*******************************************************************************#

def calculateHops(hop0, hop1, hop_number, max_sample, min_sample):
	"""Returns the value of the new hop based on the calculations with
	the previous one, actual sample value and distance to the first hop.

	Parameters: Actual sample value, number of samples to the first hop, 
	previous hop value, scaled maximum and minimum sample values.

	Exceptions: This function does not throw an exception.
	
	"""
	max_sample = 32768
	min_sample = -32768
	# Samples belong to the interval [-32768, 32767], so we move them to
	# [0, 65535] to avoid mathematical problems
	hop0 = hop0 - min_sample

	percent_range = 0.8 # Factor for positive and negative ratios
	rmax = 5.4 # Factor for ratio limits
	hop_result = 0 # Final hop

	# Ratio values for positive hops	
	ratio_pos = pow(percent_range * abs((max_sample - min_sample - 1 - hop0)/(hop1)), 0.33333333) 
	
	# Ratio values for negative hops
	ratio_neg = pow(percent_range * abs((hop0)/(hop1)), 0.33333333) 	
	
	# Ratio limits
	if (ratio_pos > rmax):
		ratio_pos = rmax 
	if (ratio_neg > rmax):
		ratio_neg = rmax

	# --- AMPLITUDES COMPUTATION --- #

	# Amplitude of positive hops
	h6 = hop1 * ratio_pos 
	h7 = h6 * ratio_pos 
	h8 = h7 * ratio_pos 

	# Amplitude of negative hops	                        
	h2 = hop1 * ratio_neg 
	h1 = h2 * ratio_neg 
	h0 = h1 * ratio_neg 

	# Hop result values
	if hop_number == 4:
		hop_result = hop0  # Null hop
	elif hop_number == 5:
		hop_result = hop0 + hop1
	elif hop_number == 3:
		hop_result = hop0 - hop1
	elif hop_number == 6:
		hop_result = hop0 + int(h6)
	elif hop_number == 2:
		hop_result = hop0 - int(h2)
	elif hop_number == 7:
		hop_result = hop0 + int(h7)
	elif hop_number == 1:
		hop_result = hop0 - int(h1)
	elif hop_number == 8:
		hop_result = hop0 + int(h8)
	elif hop_number == 0:
		hop_result = hop0 - int(h0)

	# Hop result limits
	if (hop_result <= 0):
		hop_result = 1
	if (hop_result > max_sample - min_sample):
		hop_result = max_sample - min_sample - 1

	# We bring back the sample to the [-32768, 32767] interval
	hop_result = hop_result + min_sample

	return hop_result


#*******************************************************************************#
#	Function getHops: This gets a specific hop list given the samples values.   #
#	The hop value will be predicted with the previous one.                      #   
#	Input: scaled samples list, total number of samples, maximum and minimum    #
#	sample value.                                                               #
#	Output: audio hops []                                                       #
#*******************************************************************************#

def getHops(samples, n_samples, max_sample, min_sample):
	"""Returns the hops lists for a given audio samples.

	Parameters: Scaled samples list (signed 16 bits integers), 
	total number of samples, maximum and minimum sample value.

	This function does not throw an exception.

	"""	

	# Hop1 interval: [1024, 2560], since we are working with 16 bits
	max_hop1 = 1280
	min_hop1 = 512	

	# We start in the center of the interval
	start_hop1 = (max_hop1+min_hop1)/2 
	hop1 = start_hop1

	hop0 = 0 # Predicted amplitude signal
	hop_number = 4 # Pre-selected hop -> 4 is null hop
	os = 0 # Original sample
	amp = 0 # Amplitude position, from 0 to n_samples   
	last_small_hop = "false" # Indicates if last hop is small. Used for h1 adaptation mechanism

	hops = [-1] * n_samples # Final hop values
	result = [-1] * n_samples # Final amplitude values

	s = 0 # Sample counter
	k = 0 # Original color counter

	while (s < n_samples): # We iterate over all the audio samples
		
		# Original audio amplitudes are stored in the array "samples"
		os = samples[k]

		# HOP0 PREDICTION #
		# ------------------------------------------------------------------------------ #

		# We just need the previous amplitude value.
		if (s > 0):
			if hops[amp-1] == 4:
				hop0 = result[amp-1]
			elif hops[amp-1] == 5:
				hop0 = result[amp-1] + 400
			elif hops[amp-1] == 3:
				hop0 = result[amp-1] - 400
			elif hops[amp-1] == 6:
				hop0 = result[amp-1] + 600
			elif hops[amp-1] == 2:
				hop0 = result[amp-1] - 600
			elif hops[amp-1] == 7:
				hop0 = result[amp-1] + 800
			elif hops[amp-1] == 1:
				hop0 = result[amp-1] - 800
			elif hops[amp-1] == 8:
				hop0 = result[amp-1] + 1000
			elif hops[amp-1] == 0:
				hop0 = result[amp-1] - 1000
		else:
			hop0 = os

		# HOPS COMPUTATION #
		# ---------------------------------------------------- #

		# Initial error values 
		emin = max_sample # Current minimum prediction error 
		e2 = 0 # Computed error for each hop 
		finbuc = 0 # We can optimize the code below with this
		lock = 0

		#Positive hops computation
		if (os - hop0 >= 0): 
			for j in range (4, 9):
				# We start checking the difference between the original amplitude and the cache
				e2 = os - calculateHops(hop0, hop1, j, max_sample, min_sample)
				if (e2 < 0): 
					e2 = - e2
					finbuc = 1 # When error is negative, we get the hop we need
				if (e2 < emin):
					hop_number = j # Hop assignment
					emin = e2
					if (finbuc == 1): # This avoids a useless iteration
						break
				else:
					break

		# Negative hops computation. Same bucle as before
		else:
			for j in range(4, -1, -1):
				e2 = calculateHops(hop0, hop1, j, max_sample, min_sample) - os  
				if (e2 < 0): 
					e2 = - e2
					finbuc = 1 
				if (e2 < emin): 
					hop_number = j 
					emin = e2
					if (finbuc == 1):
						break
				else:
					break 

		# Assignment of final value
		#hops[amp], result[amp] = nextHop(os, hop0, hop1)
		result[amp] = calculateHops(hop0, hop1, hop_number, max_sample, min_sample) # Final amplitude
		hops[amp] = hop_number  # Final hop value

		# Tunning hop1 for the next hop ("h1 adaptation")
		small_hop = "false" 
		if (hop_number <= 5 and hop_number >= 3): 
			small_hop = "true" # Hop 4 is in the center and is null.
		else:
			small_hop = "false"      

		# If we have small hops, that means we are in a plain zone, so we increase precision
		if (small_hop == "true" and last_small_hop == "true"):
			hop1 = hop1 - 100
			if (hop1 < min_hop1):
				hop1 = min_hop1 
		else:
			hop1 = max_hop1

		# Let's go for the next sample
		last_small_hop = small_hop
		amp = amp + 1

		s = s + 1 
		k = k + 1

	return hops, result
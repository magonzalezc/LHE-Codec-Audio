"""

This module writes a .lhe file with some data, given the hops lists of the audio.

"""
# LHE Codec for Audio
# Author: Eduardo Rodes Pastor

import Auxiliary.huff as huff
import struct, math, os

# ---------------#
# BINARY ENCODER #
# ---------------#

#******************************************************************************#
#	Function getSymbols: This converts a hops list into a symbol list. We will #
#	use a list called distribution, so we know which symbol we need based on   #
#	the actual hop. It will also include a symbol compressor; we will use a    #
#	symbol 'X' which means a variable '1' (null hops) chain each time, based   #
#	on the length of '1' chains we got before.                                 #
#	Input: Hops list                                                           #
#	Output: Symbols list                                                       #
#******************************************************************************#

def getSymbols(hops):
	"""Returns a list of symbols given their respective hops list.

	This function also uses the dynamic compressor: we have a 'X' symbol which
	will mean a variable '1' chain of symbols.

	Parameters: Hops list (integers from 0 to 8).

	Exceptions: This function does not throw an exception.

	"""

	n_samples = len(hops)
	sym = [0] * n_samples # Symbols list

	# Dynamic compressor variables
	cnt = 0 # Counter for '1' chains
	x_length = 8 # 'X' will start meaning eight '1' symbols

	# The following variable means we are in a chain which some of their symbols already were
	# compressed with 'X'. We dont reduce x_length
	in_chain = "false" 

	distribution = [9, 7, 5, 3, 1, 2, 4, 6, 8] # Symbols distribution: Hop 0 is '9', hop 1 is '7', hop 2 is '5'...

	# We will use the symbol 'X' to represent '1' chains. The length of these chains will be saved in an array
	for k in range(0, n_samples):

		# If the hop is null, write '1' or 'X' depending on how many null hops are behind this one
		if (hops[k] == 4): 
			cnt = cnt + 1 # We increase the length of the chain
			if (cnt < x_length): 
				sym[k] = 1 # This symbol '1' will be removed if the chain has a length >= x_length
			else:
				sym[k-(x_length-1)] = 'X' # If chain length reaches 8, we write 'X'
				cnt = 0 # Reseting counter
				in_chain = "true" # We keep analyzing the chain
				for p in range(0, x_length-1): 
					sym[k-p] = 0 # We clear all the symbols '1' we wrote in this chain
				x_length = x_length + 2 # We increase the length for next chain				
			continue

		# If the hop is not null, we check the distribution list
		else: 
			sym[k] = distribution[hops[k]]
			if (cnt != 0): # If we get a != '1' symbol, we reset the counter and save it in an array
				cnt = 0 # Reset
				if (in_chain == "false"): 
					x_length = int(math.ceil(float((x_length) + 8)/2)) # We reduce the length of the symbol 'X'
			in_chain = "false" # We are not anymore in a chain
			continue

	sym = [x for x in sym if x != 0] # This removes all '0' symbols that are remaining.

	return sym


#******************************************************************************#
#	Function writeFile: This will create a .lhe file which will contain some   #
#	data for the decoder and the amplitude symbols with Huffman coding. I know #
#	creating and deleting files can be a bit slow, but I think it's the        #
#	easiest way to understand what this method is doing.                       #
#	Input: Symbol lists, amplitude value for the first sample, maximum and     #
#	minimum sample value of the audio.                                         #
#	Output: None, this function just creates the file.                         #
#******************************************************************************#

def writeFile(sym, first_amp, n_samples, max_sample, min_sample):
	"""Writes a .lhe file with some data for the decoder.

	Parameters: Symbol lists (integers from 1 to 9), amplitude value for the 
	first sample, maximum and minimum sample value of the audio (signed 16 bits
	integers)

	Exceptions: This function does not throw an exception.

	"""

	# -- PAYLOAD -- #

	f = open("output_lhe/" + "payload" + ".lhe", "wb")

	# We write the not codified amplitude
	for item in sym:
  		f.write(str(item))

  	f.close()

	enc = huff.Encoder("output_lhe/payload.lhe") # We codify the amplitude with Huffman 
	enc.write("output_lhe/" + "payload_huff" + ".lhe") # We save the codified amplitude

	# -- HEADER -- #

	f = open("output_lhe/header.lhe", "wb")

	f.write(struct.pack("B", 0)) # We are in basic LHE, so we write a '00000000' byte. This wont be used in this codec
	f.write(struct.pack("i", len(sym))) # Length of the samples symbols list (4 bytes)
	f.write(struct.pack("i", first_amp)) # First amplitude value, so the decoder has a reference (4 bytes)
	f.write(struct.pack("i", n_samples)) # Number of total samples of the audio (4 bytes)
	f.write(struct.pack("i", max_sample)) # Number of maximum sample of the audio (4 bytes)
	f.write(struct.pack("i", min_sample)) # Number of minimum sample of the audio (4 bytes)
	f.close() # Total header length: 21 bytes.

	f = open("output_lhe/lhe_file.lhe", "wb") # This is the final lhe file

	# -- WRITING FILE -- #

	f2 = open("output_lhe/header.lhe", "rb") # Writing header
	f.write(f2.read())
	f2.close()
	f2 = open("output_lhe/" + "payload_huff" + ".lhe", "rb") # Writing payload
	f.write(f2.read())
	f2.close()
	f.close()

	# -- REMOVING OTHER FILES -- #

	os.remove("output_lhe/header.lhe")
	os.remove("output_lhe/payload.lhe")
	os.remove("output_lhe/payload_huff.lhe")
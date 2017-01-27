"""

This module gets the symbols lists from the .lhe file of the coded audio.

"""
# LHE Codec for Audio
# Author: Eduardo Rodes Pastor

import Auxiliary.huff as huff
import struct, math, os

# ---------------#
# BINARY DECODER #
# ---------------#

#*****************************************************************************#
#	Function getData: This reads some data from the .lhe file header. Since   #
#	we know the size each number has, we can identify where 4 bytes will be   #
#	needed.                                                                   #
#	Input: .lhe file                                                          #
#	Output: Data, in order: Length of the samples symbols list, first         #
#	amplitude value                                                           #
#*****************************************************************************#

def getData(lhe_file):
	"""Returns some values from the .lhe file header that will be useful for the decoding.

	Parameters: .lhe file (string)

	Output: In order: Length of the samples symbols list, first amplitude value,
	number of samples and maximum sample value.

	Exceptions: This will throw an exception if the .lhe file is not in the 
	output_lhe folder.

	"""
	
	fp = open(lhe_file, "rb")
	data = fp.read()

	i = 0 # Value to seek
	k = 0 # Position of the list where we will write a specific data

	# We need 6 slots: lhe type, length of the samples symbols list, 
	# first amplitude value, total number of samples and maximum and minimum 
	# sample value
	header = [0] * 6

	while (i <= 20): # The file header has a size of 21 bytes

		# We get a position in the file header
		fp.seek(i)

		# If this position starts a 4 byte value, we unpack it with 'i'.
		if (i != 0):
			data = fp.read(4)
			unpacked_data = struct.unpack("i", data)[0] # 'i' is for 4 bytes
			header[k] = unpacked_data # We save it in the final list
			k = k + 1 # Next position in the list to save the following value
			i = i + 4 # Seek 4 bytes forward

		# Otherwise, we only need 1 byte
		else:
			data = fp.read(1) # We read 1 byte
			unpacked_data = struct.unpack("B", data)[0] # 'B' is for 1 byte
			header[k] = unpacked_data 
			k = k + 1
			i = i + 1 

	# We return the values we need in this decoder
	return header[1], header[2], header[3], header[4], header[5]


#*****************************************************************************#
#	Function getSymbolsLists: This returns the amplitude list of symbols      #
#	given a .lhe file. It also detects the 'X' value, since it also is the    #
#	dynamic decompressor.                                                     #
#	Input: .lhe file, number of symbols of the list, number of samples of the #
#	audio (this is not equal to the number of symbols because of the symbol   #
#	'X')                                                                      #
#	Output: Symbols list                                                      #
#*****************************************************************************#

def getSymbolsList(lhe_file, n_sym, n_samples):
	"""Returns the codified symbols lists of a given .lhe file.

	Parameters: .lhe file (string), number of symbols of the audio (integer),
	number of samples of the audio (this is not equal to the number of symbols 
	because of the symbol 'X').

	Exceptions: This will throw an exception if the .lhe file is not in the 
	output_lhe folder.

	"""

	# -- AMPLITUDE FILE -- #

	# We discard the header 
	with open(lhe_file, "rb", 0) as fp:
		fp.seek(21)
		data = fp.read(n_sym)
	fp.close()

 	# Get the file with the Huffman codified amplitude
	fp = open("output_lhe/out-huffman_audio.lhe", "wb")
	fp.write(data)
	fp.close()

	# We decode with Huffman
	dec = huff.Decoder("output_lhe/out-huffman_audio.lhe")
	dec.decode_as("output_lhe/out-audio.lhe")

	# And we get the symbols of the file
	f = open("output_lhe/out-audio.lhe", "rb")
	sym = f.read()
	f.close()

	# We create the lists we are going to work with
	prov_sym = [0] * len(sym) # Provisional amplitude list (joined string)
	final_sym = [0] * n_samples # Final amplitude list

	# -- DYNAMIC DECOMPRESSOR -- #

	# We apply the necessary changes to the 'X' symbol
	# Remember it means a variable group of '1' symbols
	x_length = 8 # Starting x_length

	# The following variable means we are in a chain which some of their symbols already were
	# compressed with 'X'. We dont reduce x_length
	in_chain = "false"

	for i in range(0, n_sym):

		# If we get 'X', we change it for the correct number of '1' symbols in a row 
		if sym[i] == 'X':
			in_chain = "true" # 'X' is just a group of '1'
			chain = ''.join(['1'] * x_length) # We create the '1' chain
			prov_sym[i] = chain # And save it in the list
			x_length = x_length + 2 # Finally, we increase x_length for the next 'X'

		# If we get '1', we save it and decrease x_length if it's the first '1' we get
		elif (sym[i] == '1'):
			prov_sym[i] = '1'
			if (in_chain == "false"): # '1' after a symbol which is not 'X' or '1'
				x_length = int(math.ceil(float((x_length) + 8)/2))
			in_chain = "true"

		# Otherwise, save the symbol and we stop being in a '1' chain
		else:
			prov_sym[i] = sym[i]
			in_chain = "false" 

	# We join the lists so we can work with them
	prov_sym = ''.join(prov_sym)

	# Amplitude saving
	for i in range(0, len(prov_sym)):
		try:
			final_sym[i] = int(prov_sym[i])
		except:
			final_sym[i] = prov_sym[i]

	# We delete the files we won't use anymore.
	os.remove("output_lhe/out-huffman_audio.lhe")
	os.remove("output_lhe/out-audio.lhe")

	return final_sym
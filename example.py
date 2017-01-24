"""

Example and main function of the program.

"""
# LHE Codec for Audio
# Author: Eduardo Rodes Pastor

import sys

from LHEquantizer import *
from binary_enc import *
from binary_dec import *
from audio_dec import *
from Auxiliary.psnr import *

# ------------------------#
# CODING/DECODING EXAMPLE #
# ------------------------#

if __name__=='__main__':

	# Codec function (encoding/decoding)
	function = "none"

	# Function selection
	while (function != "enc" and function != "dec" and function != "exit"):
		print ""
		function = raw_input("Select the function. Please, type enc for encoding, dec for decoding or exit if you want to close the program: ")

	# --- ENCODER --- #

	if function == "enc":

		# Input audio path
		using = "input_audio/track1.wav"

		# LHE Quantizer
		samples, n_samples, max_sample, min_sample = getSamples(using)

		hops, result = getHops(samples, n_samples, max_sample, min_sample)
		print result[10000:10050]
		print samples[10000:10050]
		print hops[10000:10050]
		# We get the audio PSNR
		print ""
		calculatePSNR(result, samples, n_samples)
		print ""

		# Binary encoder
		sym = getSymbols(hops)
		writeFile(sym, samples[0], n_samples, max_sample, min_sample)
		print ".lhe file created."

	# --- DECODER --- #

	elif function == "dec":

		# Lhe file path
		path = "output_lhe/lhe_file.lhe"

		# Binary decoder
		n_sym, first_amp, n_samples, max_sample, min_sample = getData(path)
		sym = getSymbolsList(path, n_sym, n_samples)

		# Audio decoder
		hops = symbolsToHops(sym)

		samples = hopsToSamples(hops, first_amp, n_samples, max_sample, min_sample)
		getAudio(samples)
		print "Output audio file created."

	# --- EXIT --- #

	elif function == "exit":

		print ''
		sys.exit(1)


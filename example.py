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
	while (function != "enc" and function != "dec" and function != "exit" and function!=""):
		print ""
		function = raw_input("Select the function. Please, type ENTER for enc+dec, enc for encoding, dec for decoding or exit if you want to close the program: ")

	# --- ENCODER --- #

	if function == "enc" or function=="":

		# Input audio path
		#using = "input_audio/ali.wav"
		#using = "input_audio/insomnia.wav"
		using = "input_audio/track1.wav"
		#using = "input_audio/SafetyDance.wav"
		#using = "input_audio/dontyou.wav"
		#using = "input_audio/Alizee.wav"
		#using = "input_audio/3072.wav"
		#using = "input_audio/momentos.wav"
		# LHE Quantizer
		samples, n_samples, max_sample, min_sample = getSamples(using)

		#DEBUG FILE: SCALED AUDIO
		scaled_samples = [0] * n_samples
		for i in range (0, n_samples):
			scaled_samples[i] = samples[i] - 32767
		getAudio(scaled_samples, 'output_lhe/audio/original_scaled_audio.wav')

		hops, result = getHops(samples, n_samples, max_sample, min_sample)

		# We get the audio PSNR
		print ""
		calculatePSNR(result, samples, n_samples)
		print ""

		# Binary encoder
		print "translating from hops to symbols..."
		sym = getSymbols(hops)
		print "hops to symbols done"
		writeFile(sym, samples[0], n_samples, max_sample, min_sample)
		print ".lhe file created."

	# --- DECODER --- #

	if function == "dec" or function=="":

		# Lhe file path
		path = "output_lhe/lhe_file.lhe"

		# Binary decoder
		n_sym, first_amp, n_samples, max_sample, min_sample = getData(path)
		sym = getSymbolsList(path, n_sym, n_samples)

		# Audio decoder
		print "translating syms to hops..."
		hops = symbolsToHops(sym)
		print "syms to hops done"
		print "translating hops to samples..."
		samples = hopsToSamples(hops, first_amp, n_samples, max_sample, min_sample)

		print "hops to samples done"
		getAudio(samples, 'output_lhe/audio/output_audio.wav')
		print "Output audio file created."

	# --- EXIT --- #

	if function == "exit":

		print ''
		sys.exit(1)

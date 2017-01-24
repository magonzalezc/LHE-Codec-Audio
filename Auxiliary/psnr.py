"""

This module calculates the Peak Signal to Noise Ratio (PSNR) of a codified audio.

"""
# LHE Codec for Audio
# Author: Eduardo Rodes Pastor

import math

# ----------------#
# PSNR CALCULATOR #
# ----------------#

#*******************************************************************************#
#   Function getHops: This calculates the Peak Signal to Noise Ratio (PSNR) of  #
#   the codified audio, comparing it to the original one.                       #
#   Input: predicted amplitude list, original amplitude list and number of      #
#   samples.                                                                    #
#   Output: None, this just prints the PSNR.                                    #
#*******************************************************************************#

def calculatePSNR(amp_pred, amp, n_samples):
	"""Prints the PSNR of the audio amplitude lists given.

	It compares the predicted amplitude list with the original one and gets
	the total error between them.

	Parameters: predicted and original amplitude (integer list with values from -32768 to
	32767), number of samples of the audio (integer).

	Exceptions: This function does not throw an exception.

	"""
	total_amp = 0 # Summatory of squared errors
	sum_amp = 0
	var_amp = 0
	var = 0

	for i in range(0, len(amp)): 

		dif_amp = abs(amp_pred[i] - amp[i]) # Simple error between predicted and original amplitude
		if i>100000:
			print dif_amp,
		sum_amp = sum_amp + dif_amp
		var_amp = var_amp + abs(dif_amp)
		total_amp = total_amp + pow(dif_amp, 2) # We add its square to the summatory
		meanSquaredError = float(total_amp) / float(n_samples) # And we get the mean squared error per sample

	var = var_amp/len(amp)

	if (meanSquaredError != 0):
		# We use 65535 because we're using 16+16 bits for every amplitude value (positive and negative)
		peakSignalToNoiseRatio = float(10 * math.log(65535 * 65535 / meanSquaredError, 10))
		print "Peak Signal to Noise Ratio (PSNR) = ", round(peakSignalToNoiseRatio, 2), "dB"
		print "Mean error = ", sum_amp/len(amp), var_amp
		print "Var = ", var
	else:
		print "Peak Signal to Noise Ratio (PSNR) = 0 dB" # Ideal case
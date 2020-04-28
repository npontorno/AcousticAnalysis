import librosa
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np
import noisereduce as nr
import scipy as sp
import wavefile as wv
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.silence import split_on_silence
from matplotlib.pyplot import figure, plot, specgram
import matplotlib.pyplot as plt
from pydub.silence import detect_nonsilent
# for testing
import itertools
import csv
import time
import os


def main(song_files, output_dest):
	data = []
	no_syls = -1
	no_chunks = -1

	for song_file in song_files:
		print("Reducing Noise...")
		reduce_noise(song_file)
	
		print("Splitting song file into individual calls...")
		no_chunks = split_into_calls() 

		print("Splitting call files into individual syllables...")
		no_syls = split_into_syls(no_chunks)

		print("Generating and storing 36 points of data for each syllable...")
		data = generate_data_points(no_syls, data)

		print("Deleting chunks")
		for i in range(0, no_chunks):
			os.remove("chunk" + str(i) + ".wav")

		print("Deleting syllables")
		for i in range(0, no_syls):
			os.remove("syl" + str(i) + ".wav")

		print("Deleting Reduced Noise File")
		os.remove("reduced_noise_file.wav")

		print("Moving to next file...")

	
	print("Processing Complete.")

	print("Writing data to csv file")
	write_to_CSV(data, output_dest)
	print("Write Complete")


def reduce_noise(song_file):
	# use wavefile module to convert wav from int to float
	w = wv.load(song_file)
	data = w[1][0]

	# select section of data that is noise
	noisy_part = data[1500:2000]

	# perform noise reduction
	reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, n_std_thresh=1.5, prop_decrease=1, verbose=False)

	samplerate = 44100;
	write("reduced_noise_file.wav", samplerate, data)
	
	# remember to delete this file after
	return


def split_into_calls():
	# loading new audio into pydub
	rnbirds = AudioSegment.from_wav("reduced_noise_file.wav")

	# split into chunks using pydub
	chunks = split_on_silence(
    	# Use the loaded audio.
    	rnbirds, 
    	# Consider a chunk silent if it's less than the silence threshold
    	silence_thresh = -30
	)

	no_chunks = 0

	for i, chunk in enumerate(chunks):	
		chunk.export("chunk{0}.wav".format(no_chunks), format="wav")
		
		no_chunks = no_chunks + 1
	
	# remember to remove these chunks after
	return no_chunks


def split_into_syls(no_chunks):
	no_syls = 0

	for i in range(0, no_chunks):
		bird_call = AudioSegment.from_wav('./chunk' + str(i) + '.wav')

		syllables = split_on_silence(bird_call, min_silence_len=10, silence_thresh=-30, keep_silence=False)

		# pydub functions for testing
		nonsilent_ranges = detect_nonsilent(bird_call, min_silence_len=10, silence_thresh=-30)

		for i, syllable in enumerate(syllables):
			syllable.export("syl{0}.wav".format(no_syls), format="wav")
		
			no_syls = no_syls + 1
	
		return no_syls


def write_to_CSV(syl_data, output_dest):
	# generate file name
	timestr = time.strftime("%Y%m%d-%H%M%S")
	
	print("New file: " + output_dest+ '/' + timestr + '.csv')

	with open(output_dest+ '/' + timestr + '.csv', mode='w') as csv_file:
		fieldnames = ['Syllable', 'pt_1_freq', 'pt_1_amp', 'pt_2_freq', 'pt_2_amp', 'pt_3_freq', 'pt_3_amp', 'pt_4_freq', 'pt_4_amp', 'pt_5_freq', 'pt_5_amp', 'pt_6_freq', 'pt_6_amp', 'pt_7_freq', 'pt_7_amp',
		'pt_8_freq', 'pt_8_amp', 'pt_9_freq', 'pt_9_amp', 'pt_10_freq', 'pt_10_amp', 'pt_11_freq', 'pt_11_amp', 'pt_12_freq', 'pt_12_amp', 'pt_13_freq', 'pt_13_amp', 'pt_14_freq', 'pt_14_amp', 
		'pt_15_freq', 'pt_15_amp', 'pt_16_freq', 'pt_16_amp','pt_17_freq', 'pt_17_amp', 'pt_18_freq', 'pt_18_amp']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

		writer.writeheader()

		for i, syllable in enumerate(syl_data):
			writer.writerow({'Syllable': i, 'pt_1_freq': syllable[0], 'pt_1_amp': syllable[1], 'pt_2_freq': syllable[2], 'pt_2_amp': syllable[3], 'pt_3_freq': syllable[4], 'pt_3_amp' : syllable[5], 
			'pt_4_freq': syllable[6], 'pt_4_amp' : syllable[7], 'pt_5_freq' : syllable[8], 'pt_5_amp' : syllable[9], 'pt_6_freq' : syllable[10], 'pt_6_amp' : syllable [11], 'pt_7_freq': syllable[12], 
			'pt_7_amp' : syllable[13], 'pt_8_freq': syllable[14], 'pt_8_amp' : syllable[15], 'pt_9_freq' : syllable[16], 'pt_9_amp' : syllable[17], 'pt_10_freq' : syllable[18], 'pt_10_amp' : syllable[19], 
			'pt_11_freq' : syllable[20], 'pt_11_amp' : syllable[21], 'pt_12_freq' : syllable[22], 'pt_12_amp' : syllable[23], 'pt_13_freq' : syllable[24], 'pt_13_amp' : syllable[25], 'pt_14_freq' : syllable[26],
			 'pt_14_amp' : syllable[27], 'pt_15_freq' : syllable[28], 'pt_15_amp' : syllable[29], 'pt_16_freq' : syllable[30], 'pt_16_amp' : syllable[31] ,'pt_17_freq' : syllable[32], 'pt_17_amp':syllable[33], 
			'pt_18_freq' : syllable[34], 'pt_18_amp': syllable[35]})
    	

def generate_data_points(no_syls, data):
	for i in range(0, no_syls):
		bird_syl = AudioSegment.from_wav('./syl' + str(i) + '.wav')
		
		print("Splitting syllable into 18 equally long segments")
		print("Length of whole syllable: " + str(len(bird_syl)))
		
		leng_div_18 = len(bird_syl) / 18
		curr_position = 0
		new_seg = []
		syl_data = []

		for i in range(0, 18):
			if i is 0:
				new_seg = bird_syl[:curr_position + leng_div_18]
			elif i is 17:
				new_seg = bird_syl[curr_position:]
			else:
				new_seg = bird_syl[curr_position:curr_position + leng_div_18]

			# make new file from shortened seg
			new_seg.export('seg.wav', format="wav")
			
			y, sr = librosa.load('seg.wav', None, True, 0, None)

			syl_data.append(avg_frequency(y, sr))
			syl_data.append(avg_amplitude(y))

			os.remove("seg.wav")

			curr_position = curr_position + leng_div_18

		
		data.append(syl_data)
	
	return data


def avg_amplitude(y: np.ndarray) -> float:

	ampSum = 0
	z = librosa.core.amplitude_to_db(S=y)
    
	for i in range(len(z)):
		ampSum += abs(z[i])
    
	avg = ampSum/len(z)
	return avg

def avg_frequency(y: np.ndarray, fs: int) -> float:
	spec = np.abs(np.fft.rfft(y))
	freq = np.fft.rfftfreq(len(y), d=1/fs)    
	amp = spec / spec.sum()
	mean = (freq * amp).sum()
	return mean

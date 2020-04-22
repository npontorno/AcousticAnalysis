import librosa
import matplotlib.pyplot as plt
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
from time


def main(song_files, output_dest):
	data = []
	
	for song_file in song_files:
		print("Reducing Noise...")
		reduce_noise(song_file)
	
		print("Splitting song file into individual calls...")
		no_chunks = split_into_calls() 

		print("Splitting call files into individual syllables...")
		no_syls = split_into_syls()

		print("Generating and storing 36 points of data for each syllable...")
		
		
		print("Moving to next file..."

	print("Processing Complete.")

	print("Writing data to csv file")
	



def reduce_noise(song_file):
	# use wavefile module to convert wav from int to float
	w = wv.load(song_file)
	data = w[1][0]

	# select section of data that is noise
	noisy_part = data[1500:2000]

	# perform noise reduction
	reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, n_std_thresh=1.5, prop_decrease=1, verbose=True)

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

	no_chunks = -1

	for i, chunk in enumerate(chunks):
    	chunk.export("chunk{0}.wav".format(i), format="wav")
		
		no_chunks = i
	
	# remember to remove these chunks after
	return no_chunks


def split_into_syls(syl_file):
	bird_call = AudioSegment.from_wav('./chunk1.wav')

	syllables = split_on_silence(bird_call, min_silence_len=10, silence_thresh=-30, keep_silence=False)

	# pydub functions for testing
	nonsilent_ranges = detect_nonsilent(bird_call, min_silence_len=10, silence_thresh=-30)

	markers = []

	for rang in nonsilent_ranges:
    	markers.append(rang[0] * 21.84)
    	markers.append(rang[1] * 21.84)

	# Plot the complete bird call
	figure(figsize=(40, 10))

	spec = specgram(x=bird_call.get_array_of_samples(), NFFT=256, Fs=2, noverlap=128, mode='magnitude')[3]
	plt.ylim(0, .4)

	print(markers)

	for marker in markers:
    	plt.axvline(x=marker)


	no_syls = -1

	for i, syllable in enumerate(syllables):
		syllable.export("chunk{0}.wav".format(i), format="wav")
		
		no_syls = i

    	specgram(syllable.get_array_of_samples(), NFFT=256, Fs=2, noverlap=128)
	
	return no_syls


def write_to_CSV(syl_data):
	# generate file name
	timestr = time.strftime("%Y%m%d-%H%M%S")

	with open(timestr, mode='w') as csv_file:
    	fieldnames = ['Syllable', 'pt_1_freq', 'pt_1_amp', 'pt_2_freq', 'pt_2_amp', 'pt_3_freq', 'pt_3_amp', 'pt_4_freq', 'pt_4_amp', 'pt_5_freq', 'pt_5_amp', 'pt_6_freq', 'pt_6_amp', 'pt_7_freq', 'pt_7_amp',
		'pt_8_freq', 'pt_8_amp', 'pt_9_freq', 'pt_9_amp', 'pt_10_freq', 'pt_10_amp', 'pt_11_freq', 'pt_11_amp', 'pt_12_freq', 'pt_12_amp', 'pt_13_freq', 'pt_13_amp', 'pt_14_freq', 'pt_14_amp', 
		'pt_15_freq', 'pt_15_amp', 'pt_16_freq', 'pt_16_amp','pt_17_freq', 'pt_17_amp', 'pt_18_freq', 'pt_18_amp']
    	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    	writer.writeheader()
    	writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
    	writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})

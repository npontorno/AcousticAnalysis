import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# load first bird song
filename = 	"chunk1.wav"

# load audio as waveform, sampling rate as sr
y, sr = librosa.load(filename)

plt.figure(figsize=(240, 120))

D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

librosa.display.specshow(D, cmap='gray_r', x_axis = 'time', y_axis='linear')
plt.colorbar(format='%+2.0f dB')
plt.title('Waveform example')


# onset function... computes where each syllable begins
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onset_raw = librosa.onset.onset_detect(onset_envelope=onset_env, backtrack=False)
onset_bt = librosa.onset.onset_backtrack(onset_raw, onset_env)


# computes the time segments for the onsets
times = librosa.frames_to_time(onset_bt, sr)
print(times)

# plots the verticle lines where each syllable begins
plt.vlines(times, 0, 100000, color='r')

# subplot showing the onset function
plt.figure()
plt.subplot(2,1,1)
plt.plot(onset_env, label='Onset strength')
plt.vlines(onset_bt, 0, onset_env.max(), label='Onset', color='r')
plt.legend(frameon=True, framealpha=0.75)

plt.show()

# computes the duration of the video (used this for personal knowledge.. don't really need this info)
duration = librosa.core.get_duration(y, sr)
print(duration)

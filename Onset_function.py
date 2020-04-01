import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# load first bird song
filename = 	"/Users/edesern/Downloads/LISP,060603,0748,37.74615N,107.68739W,6.wav"

# load audio as waveform, sampling rate as sr
y, sr = librosa.load(filename)

# need to figure out this line
plt.figure(figsize=(240, 120))

D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

librosa.display.specshow(D, cmap='gray_r', y_axis='linear')
plt.colorbar(format='%+2.0f dB')
plt.title('Waveform example')

#plt.show()

#onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
#librosa.frames_to_time(onset_frames, sr=sr)
onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512, aggregate=np.median)

#show the onset of bird calls
peaks = librosa.util.peak_pick(onset_env, 3, 3, 3, 5, 0.5, 10)
peaks


times = librosa.times_like(onset_env, sr=sr, hop_length=512)
plt.figure()
ax = plt.subplot(2, 1, 2)
D = librosa.stft(y)
librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
plt.subplot(2, 1, 1, sharex=ax)
plt.plot(times, onset_env, alpha=0.8, label='Onset strength')
plt.vlines(times[peaks], 0, onset_env.max(), color='r', alpha=0.8, label='Selected peaks')
plt.legend(frameon=True, framealpha=0.8)
plt.axis('tight')
plt.tight_layout()
plt.show()


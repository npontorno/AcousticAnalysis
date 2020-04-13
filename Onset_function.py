import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# load first bird song
filename = 	"chunk1.wav"

# load audio as waveform, sampling rate as sr
y, sr = librosa.load(filename)

# need to figure out this line
plt.figure(figsize=(240, 120))

D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

librosa.display.specshow(D, cmap='gray_r', y_axis='linear')
plt.colorbar(format='%+2.0f dB')
plt.title('Waveform example')


# onset function... computes where each syllable begins
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onset_raw = librosa.onset.onset_detect(onset_envelope=onset_env, backtrack=False)
onset_bt = librosa.onset.onset_backtrack(onset_raw, onset_env)


#show the onset of bird calls 
#peaks = librosa.util.peak_pick(onset_bt, 3, 3, 3, 5, .5, 5)
#peaks

# graph

plt.figure()
plt.subplot(2,1,1)
plt.plot(onset_env, label='Onset strength')
plt.vlines(onset_bt, 0, onset_env.max(), label='Onset', color='r')
plt.legend(frameon=True, framealpha=0.75)


plt.show()

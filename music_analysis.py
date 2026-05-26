import librosa

folder = "/Users/annyhe/workspace/youtube-mp3-download/new_videos"


# 1. Load the audio file
# 'y' is the audio time series, 'sr' is the sampling rate
filename = '/Users/annyhe/workspace/youtube-mp3-download/new_videos/eric-how-are-you.m4a'
y, sr = librosa.load(filename)

# 2. Estimate the tempo (BPM)
# beat_track returns the estimated tempo and the beat frames
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

print(f"Estimated Tempo: {tempo[0]:.2f} BPM")
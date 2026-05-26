import librosa
import os

folder = "/Users/annyhe/workspace/youtube-mp3-download/new_videos"


for filename in sorted(os.listdir(folder)):  # sorted alphabetically
    if filename.endswith((".mp3", ".wav", ".m4a", ".ogg", ".flac")):
        filepath = os.path.join(folder, filename)
        try:
            y, sr = librosa.load(filepath)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            print(f"{tempo[0]:.1f} BPM — {filename}")
        except Exception as e:
            print(f"Could not analyze {filename}: {e}")
import yt_dlp
import os
import sys

# python3 download_youtube_audio.py 'https://www.youtube.com/watch?v=wAaKxOkdd8c'
print(f"Script name: {sys.argv[0]} another {sys.argv[1]}")
if len(sys.argv) < 2:
    print("Usage: python script.py <youtube_url>")
    sys.exit(1)

url = sys.argv[1]
print(f"Downloading audio from: {url}")

ydl_opts = {
    'format': 'bestaudio/best',  # Download best quality audio
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',   # Convert to mp3
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s', # Name file after video title
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Get video info without downloading first
    info = ydl.extract_info(url, download=True)
    # Construct filename based on how yt-dlp saves it
    filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
    print(f"Downloaded file: {filename}")
    ydl.download([url])

#  move filename to audio folder
if not os.path.exists('audio'):
    os.makedirs('audio')    
os.rename(filename, os.path.join('audio', filename))
print(f"Moved '{filename}' to 'audio/{filename}'")

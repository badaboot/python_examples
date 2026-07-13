import yt_dlp
import sys

# python3 download_youtube_video.py 'https://www.youtube.com/watch?v=wAaKxOkdd8c'
print(f"Received: {sys.argv[0]} file {sys.argv[1]}")
if len(sys.argv) < 2:
    print("Usage: python script.py <youtube_url>")
    sys.exit(1)

url = sys.argv[1]
print(f"Downloading video from: {url}")

def download_youtube_video(video_url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'verbose': True, # Displays the exact reason if 0 items download
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

download_youtube_video(url)
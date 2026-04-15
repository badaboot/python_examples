import os
import sys
import time
import re
import requests
from urllib.parse import urlparse

def download_images(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: file '{file_path}' not found")
        sys.exit(1)

    # 1. Parse metadata from the file
    query_name = "unknown_query"
    image_count = 0
    found_metadata = False

    with open(file_path, 'r') as f:
        content = f.read()
        # Look for the pattern: Found X image URLs for QUERY_NAME
        match = re.search(r"Found (\d+) image URLs for (.+)", content)
        
        if match:
            image_count = int(match.group(1))
            query_name = match.group(2).strip().strip("'").strip('"')
            found_metadata = True

    # 2. Condition Check
    if not found_metadata:
        print("Could not find 'Found X image URLs' line. Check file format.")
        return

    if image_count == 0:
        print(f"Zero images found for '{query_name}'. There's nothing to download.")
        return

    print(f"Found {image_count} images for '{query_name}'. Starting download...")

    # 3. Setup Directory
    output_dir = os.path.join("downloaded_images", query_name)
    os.makedirs(output_dir, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com/"
    }

    success, failed, num = 0, 0, 0

    # 4. Download Process
    # Re-reading line by line to handle the URLs
    with open(file_path, 'r') as f:
        for line in f:
            url = line.strip()
            
            # Skip empty lines, metadata lines, or comments
            if not url or url.startswith('#') or url.startswith('Found '):
                continue

            num += 1
            
            # Determine extension
            parsed_url = urlparse(url)
            ext = os.path.splitext(parsed_url.path)[1].lower().lstrip('.')
            if ext in ['pjpg', 'jpeg']: ext = 'jpg'
            if not ext: ext = 'bin'

            filename = os.path.join(output_dir, f"{num}.{ext}")

            try:
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    with open(filename, 'wb') as img_file:
                        img_file.write(response.content)
                    print(f"[{num:2}] ✓ {filename}")
                    success += 1
                else:
                    print(f"[{num:2}] ✗ Failed (HTTP {response.status_code}) — {url}")
                    failed += 1
            except Exception as e:
                print(f"[{num:2}] ✗ Error: {e}")
                failed += 1

            time.sleep(0.3)

    print(f"\nFinished — {success} succeeded, {failed} failed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_images.py <urls.txt>")
    else:
        download_images(sys.argv[1])
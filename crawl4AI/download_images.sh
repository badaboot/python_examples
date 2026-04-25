#!/bin/bash

# Usage: ./download_images.sh urls.txt optional_folder_name

if [[ -z "$1" ]]; then
  echo "Usage: $0 <urls.txt>"
  exit 1
fi

if [[ ! -f "$1" ]]; then
  echo "Error: file '$1' not found"
  exit 1
fi

if [ -n "$2" ]; then
  echo "Folder name: '$2'"
  folder_name=$2
  mkdir -p "downloaded_images/$2"
else
  folder_name="$(date +%Y-%m-%d_%H-%M-%S)"
  mkdir -p "downloaded_images/$folder_name"
fi


SUCCESS=0
FAILED=0
NUM=0

while IFS= read -r URL || [[ -n "$URL" ]]; do
  # Skip empty lines and comments
  [[ -z "$URL" || "$URL" == \#* ]] && continue

  NUM=$((NUM + 1))

  # Derive extension from URL path (before any query string)
  CLEAN_URL="${URL%%\?*}"
  EXT="${CLEAN_URL##*.}"
  [[ "$EXT" == "pjpg" || "$EXT" == "jpeg" ]] && EXT="jpg"
  FILENAME="downloaded_images/$folder_name/${NUM}.${EXT}"

  HTTP_CODE=$(curl -s -o "$FILENAME" -w "%{http_code}" \
    --max-time 30 \
    -L \
    -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" \
    -H "Referer: https://www.google.com/" \
    "$URL")

  if [[ "$HTTP_CODE" == "200" ]]; then
    echo "[$(printf '%2d' $NUM)] ✓ $FILENAME (HTTP $HTTP_CODE)"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "[$(printf '%2d' $NUM)] ✗ Failed (HTTP $HTTP_CODE) — $URL"
    rm -f "$FILENAME"
    FAILED=$((FAILED + 1))
  fi

  sleep 0.3
done < "$1"

echo ""
echo "Done — $SUCCESS succeeded, $FAILED failed"

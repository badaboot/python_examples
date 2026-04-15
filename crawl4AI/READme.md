# Craw4AI to download images

Steps

### Get images from google images search

1. `python3 crawl4AI/get_images.py 'tokyo ghoul illustration' > image_urls.txt`
2. `python3 crawl4AI/download_images.py image_urls.txt` # creates folder with query name

### Get images from wikimedia

1. `python3 crawl4AI/wikimedia.py > image_urls.txt`
2. `source crawl4AI/download_images.sh image_urls.txt` # creates folder with date timestamp

### Known issues

1. Reddit image preview fails to download image: Failed (HTTP 403) — https://preview.redd.it/some-of-sui-ishidas-illustrations-part-2-v0-e6oajgt1hxt81.jpg
2. LinkedIn scrape: get login page

TODO:

5. `get_markdown`: change to dynamic URL. current URL is static

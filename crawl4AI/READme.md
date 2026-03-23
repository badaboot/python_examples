# Craw4AI to download images

Steps

1. run `get_markdown.py > page.md` to get markdown from a url
2. run `parse_markdown.py > parsed_urls.json` to get the image urls from a markdown

### Get images from google images search

3. `python3 crawl4AI/get_images.py 'tokyo ghoul illustration' > image_urls.txt`
4. `source crawl4AI/download_images.sh image_urls.txt`

### Known issues

1. Reddit image preview fails to download image: Failed (HTTP 403) — https://preview.redd.it/some-of-sui-ishidas-illustrations-part-2-v0-e6oajgt1hxt81.jpg
2. LinkedIn scrape: get login page

TODO:

5. `get_markdown`: change to dynamic URL. current URL is static

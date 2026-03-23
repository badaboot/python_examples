steps

1. run `get_markdown.py > page.md` to get markdown from a url
2. run `parse_markdown.py > parsed_urls.json` to get the image urls from a markdown

### Get images from google images search

3. `python3 crawl4AI/get_images.py > image_urls.txt`
4. `source download_images.sh image_urls.txt`

TODO:

5. `get_markdown`: change to dynamic URL. current URL is static

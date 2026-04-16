import asyncio
import re
import sys
from urllib.parse import urlencode
from crawl4ai import AsyncWebCrawler

# usage: python3 crawl4AI/get_images.py 'tokyo ghoul illustration' > image_urls.txt
# then `python3 crawl4AI/download_images.py image_urls.txt` # creates folder with query name

def get_query():
    if len(sys.argv) < 2:
        print("Usage: python get_images.py '<search query>'")
        print("Example: python get_images.py 'tokyo ghoul illustration'")
        sys.exit(1)
    return " ".join(sys.argv[1:])  # join in case user forgot quotes

async def main():
    query = get_query()
    search_url = f"https://www.google.com/search?{urlencode({'q': query, 'tbm': 'isch'})}"
    print(f"Searching: {query}\n")

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=search_url,
            magic=True,
            simulate_user=True,
        )

        urls = re.findall(
            r'"murl":"(https://[^"]+\.(?:jpg|png|jpeg))"',
            result.html or ""
        )

        if not urls:
            urls = re.findall(
                r'https://[^\s"\']+\.(?:jpg|png|jpeg)',
                result.html or ""
            )

        seen = set()
        for url in urls:
            if url not in seen:
                seen.add(url)
                print(url)

        print(f"\nFound {len(seen)} image URLs for '{query}'")

if __name__ == "__main__":
    asyncio.run(main())
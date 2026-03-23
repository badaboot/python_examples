import asyncio
import re
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        # TODO: extract query to command line
        result = await crawler.arun(
            url="https://www.google.com/search?q=chinese+watercolor&tbm=isch",
            magic=True,          # enables stealth mode + anti-bot bypass
            simulate_user=True,  # simulates human-like behavior
        )

        # Extract image URLs from the raw HTML
        urls = re.findall(
            r'"murl":"(https://[^"]+\.(?:jpg|png|jpeg))"',
            result.html or ""
        )

        if not urls:
            # fallback: try src attributes from markdown/html
            urls = re.findall(
                r'https://[^\s"\']+\.(?:jpg|png|jpeg)',
                result.html or ""
            )

        # Deduplicate and print
        seen = set()
        for url in urls:
            if url not in seen:
                seen.add(url)
                print(url)

        print(f"\nFound {len(seen)} image URLs")

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
from crawl4ai import AsyncWebCrawler
import re

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://commons.wikimedia.org/wiki/Category:Quality_images_of_China",
        )
        # print(result.markdown)

        # Assuming 'markdown_data' is the string you pasted above
        markdown_data = result.markdown

        # Regex to find Wikimedia thumbnail URLs
        # These typically reside inside [![] (image_url)]
        image_urls = re.findall(r'https://upload\.wikimedia\.org/wikipedia/commons/thumb/[^\s\)]+', markdown_data)

        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(image_urls))

        print(f"Extracted {len(unique_urls)} unique image URLs:")
        for url in unique_urls:
            print(url)

if __name__ == "__main__":
    asyncio.run(main())
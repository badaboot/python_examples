import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    schema = {
        "name": "WikiFilePages",
        "baseSelector": ".gallerybox",
        "fields": [
            {
                "name": "file_page",
                "selector": "a.mw-file-description",
                "attribute": "href",
                "type": "attribute"  # <--- Add this line to fix the 'type' error
            }
        ],
    }

    async def extract_high_res(file_page_urls):
        # Schema to find the "Original file" link on the destination page
        file_schema = {
            "name": "HighResFile",
            "baseSelector": ".fullMedia",
            "fields": [
                {
                    "name": "high_res_url",
                    "selector": "a",
                    "attribute": "href",
                    "type": "attribute"
                }
            ],
        }

        # Browser config for stability
        browser_cfg = BrowserConfig(headless=True, verbose=False)
        
        # Run config with the extraction strategy
        run_cfg = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(file_schema),
            wait_for="css:.fullMedia a"
        )

        async with AsyncWebCrawler(config=browser_cfg) as crawler:
            # arun_many visits the list of URLs in parallel
            # We'll do a small batch first to verify
            results = await crawler.arun_many(
                urls=file_page_urls, 
                config=CrawlerRunConfig(
                    extraction_strategy=JsonCssExtractionStrategy(file_schema),
                    wait_for="css:.fullMedia a",
                ),
                dispatcher_threshold=10 # Processes in waves of 10

            )

            final_links = []
            for res in results:
                if res.success and res.extracted_content:
                    data = json.loads(res.extracted_content)
                    for item in data:
                        if 'high_res_url' in item:
                            # Add the URL to our list
                            final_links.append(item['high_res_url'])
                    # if content:
                    #     final_links.append(content[0]['high_res_url'])
            
            return final_links
        
        

    # Rest of the logic remains the same
    async with AsyncWebCrawler() as crawler:
        config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(schema),
            wait_for="css:a.mw-file-description"
        )

        result = await crawler.arun(
            url="https://commons.wikimedia.org/wiki/Category:Quality_images_of_China",
            config=config
        )

        if result.success and result.extracted_content:
            data = json.loads(result.extracted_content)
            # Filter and construct full URLs
            file_urls = [
                f"https://commons.wikimedia.org{item['file_page']}" 
                for item in data if 'file_page' in item
            ]
            print(f"Success! Found {len(file_urls)} URLs.")
            high_res_list = await extract_high_res(file_urls)
            output = "\n".join(high_res_list)
            print(output)
        else:
            print(f"Crawl failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
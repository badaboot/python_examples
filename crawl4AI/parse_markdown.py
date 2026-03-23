import re

def extract_image_urls(markdown: str) -> list[dict]:
    # Matches both ![alt](url) and bare URLs
    pattern = r'!\[.*?\]\((https?://[^\)]+\.(?:jpg|png)(?:\?[^\)]*)?)?\)|(?<!\()https?://\S+\.(?:jpg|png)(?:\S*)?'
    
    matches = re.findall(r'https?://\S+\.(?:jpg|png)(?:[^\s\)\"\']*)?', markdown)
    
    return [
        {"id": i + 1, "url": url, "format": "." + url.split("?")[0].split(".")[-1]}
        for i, url in enumerate(matches)
    ]
with open("./page.md", "r") as f:
    md = f.read()

urls = extract_image_urls(md)
print(urls)
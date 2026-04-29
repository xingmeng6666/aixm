import requests
from bs4 import BeautifulSoup

class WebCrawlerTool:
    """
    A tool for agents to crawl and extract information from web pages.
    """
    def fetch_page(self, url: str):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_text(self, html_content: str):
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator=' ', strip=True)

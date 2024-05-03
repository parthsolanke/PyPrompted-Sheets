import requests
from bs4 import BeautifulSoup
import re

class DataScraper:
    """
    A class that provides methods for scraping content from HTML web pages.
    """

    def __init__(self, timeout=10):
        self.timeout = timeout

    def scrape_content(self, url):
        """
        Scrapes the content from the specified URL.

        Args:
            url (str): The URL of the web page to scrape.

        Returns:
            str: The cleaned text content of the web page, or "N/A" if an error occurs.
        """
        try:
            response = self._get_html_response(url)
            if response is None:
                return "N/A"

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements such as headers, footers, and advertisements
            for tag in soup(["header", "footer", "nav", "aside", "script", "style"]):
                tag.decompose()

            # Extract only the main content
            main_content = soup.find("body").get_text(separator=' ')

            cleaned_content = self._clean_text_content(main_content)
            
            print(f"Scraping complete for HTML URL: {url}")
            return cleaned_content.strip()
        except requests.RequestException as e:
            print(f"Error with URL {url}: {e}")
            return "N/A"
        except Exception as e:
            print(f"Unhandled error with URL {url}: {e}")
            return "N/A"

    def scrape(self, urls):
        """
        Scrapes the content from a list of URLs.

        Args:
            urls (list): A list of URLs to scrape.

        Returns:
            list: A list of cleaned text content from the web pages.
        """
        scraped_data = []
        for url in urls:
            content = self.scrape_content(url)
            if content:
                scraped_data.append(content)
        return scraped_data

    def _get_html_response(self, url):
        """
        Sends a GET request to the specified URL and returns the response.

        Args:
            url (str): The URL to send the request to.

        Returns:
            requests.Response: The response object, or None if an error occurs.
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error with URL {url}: {e}")
            return None

    def _clean_text_content(self, text_content):
        """
        Cleans the text content by removing extra whitespace, newlines, and special characters.

        Args:
            text_content (str): The text content to clean.

        Returns:
            str: The cleaned text content.
        """
        cleaned_content = re.sub(r"\s\s+", " ", text_content).replace('\n', ' ').replace('\xa0', '').strip()
        return cleaned_content

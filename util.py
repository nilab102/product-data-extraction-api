import re
import time
from bs4 import BeautifulSoup
import html2text
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import CHROME_OPTIONS
from zenrows import ZenRowsClient  
import os 
def fetch_html_selenium(url: str, headless: bool = True) -> str:
    """
    Fetch HTML content from the given URL using Selenium.
    """
    chrome_options = Options()
    for opt in CHROME_OPTIONS:
        chrome_options.add_argument(opt)
        
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        # Optionally: add explicit wait logic if needed
        html_content = driver.page_source
        return html_content
    finally:
        driver.quit()

def clean_html(html_content: str) -> str:
    """
    Cleans the HTML by removing headers, footers, images, ads, media, and unwanted text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove headers and footers
    for element in soup.find_all(['header', 'footer']):
        element.decompose()

    # Remove images
    for img in soup.find_all('img'):
        img.decompose()

    # Remove advertisements by class or ID
    ad_classes = ['ad', 'advertisement', 'ad-banner', 'ad-overlay', 'ads']
    ad_ids = ['ad', 'advertisement', 'ad-banner', 'ad-overlay', 'ads']
    for ad in soup.find_all(class_=ad_classes):
        ad.decompose()
    for ad in soup.find_all(id=ad_ids):
        ad.decompose()

    # Remove links with javascript or specific patterns
    for link in soup.find_all('a', href=True):
        if 'javascript:void(0)' in link['href'] or '/-/en/' in link['href']:
            link.decompose()

    # Remove video and audio tags
    for media in soup.find_all(['video', 'audio']):
        media.decompose()

    # Remove comment boxes and reviews
    comment_classes = ['comments', 'comment-box', 'review', 'reviews', 'user-comments', 'feedback']
    for comment in soup.find_all(class_=comment_classes):
        comment.decompose()

    # Remove elements containing certain keywords
    keywords_to_remove = [
        "Play Video", "Mute", "Comment", "Review", "Submit Review", "Audio", "Video",
        "Post Comment", "Leave a Comment", "Unable to add item to List",
        "The video showcases", "The video guides", "Play", "Chapters", "Descriptions"
    ]
    for element in soup.find_all(text=True):
        if any(keyword in element for keyword in keywords_to_remove):
            element.extract()

    return str(soup)

def html_to_markdown_with_readability(html_content: str) -> str:
    """
    Converts cleaned HTML content to Markdown format.
    """
    cleaned_html = clean_html(html_content)
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    markdown_content = converter.handle(cleaned_html)
    return markdown_content

def remove_urls_from_text(text: str) -> str:
    """
    Removes URLs from the provided text.
    """
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    cleaned_text = re.sub(url_pattern, '', text)
    return cleaned_text


def fetch_html_zenrows(url: str, api_key: str = None) -> str:
    """
    Fetch HTML content from the given URL using the ZenRows API.

    Args:
        url (str): The URL to fetch.
        api_key (str, optional): Your ZenRows API key. If not provided,
            it will try to fetch the key from the ZENROWS_API_KEY environment variable.
            A default key is also provided for testing purposes.
    
    Returns:
        str: The HTML content retrieved via ZenRows.
    """
    # Use the provided api_key, or get it from the environment (or use the default provided key)
    if api_key is None:
        api_key = os.getenv("ZENROWS_API_KEY")
    
    client = ZenRowsClient(api_key)
    params = {"js_render":"true","premium_proxy":"true","proxy_country":"sa"}

    response = client.get(url, params=params)
    # Depending on the ZenRows response structure, adjust accordingly.
    # Here we assume the HTML content is available as text.
    return response.text


def clean_text(url: str, method: str = "selenium") -> str:
    """
    Fetches HTML content from a URL using the specified method ('selenium' or 'zenrows')
    and returns cleaned text.

    Args:
        url (str): The URL to fetch.
        method (str): The method to use: "selenium" or "zenrows".

    Returns:
        str: Cleaned text extracted from the URL.
    """
    if method.lower() == "zenrows":
        html_content = fetch_html_zenrows(url)
    else:
        html_content = fetch_html_selenium(url)
    
    markdown = html_to_markdown_with_readability(html_content)
    text = remove_urls_from_text(markdown)
    return text
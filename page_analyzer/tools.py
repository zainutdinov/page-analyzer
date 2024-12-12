from urllib.parse import urlparse

from bs4 import BeautifulSoup
from validators import url as validate_url


def parse_html(response):
    resp_code = response.status_code
    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else None
    h1_tag = soup.find("h1")
    h1 = h1_tag.get_text(strip=True) if h1_tag else None
    description_tag = soup.find("meta", attrs={"name": "description"})
    descrip = (
        description_tag["content"]
        if description_tag and "content" in description_tag.attrs
        else None
    )
    return resp_code, title, h1, descrip


MAX_URL_LENGTH = 255


def validate_and_normalize_url(url):
    if not validate_url(url):
        return None
    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    if len(normalized_url) > MAX_URL_LENGTH:
        return None
    return normalized_url

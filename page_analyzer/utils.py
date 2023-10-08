from urllib.parse import urlparse


def normalize_url(str_url):
    parsed_url = urlparse(str_url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    return normalized_url

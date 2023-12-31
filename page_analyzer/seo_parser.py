from bs4 import BeautifulSoup


def get_seo_info_dict(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1').text if soup.find('h1') else None
    title = soup.find('title').text if soup.find('title') else None
    meta = soup.find("meta", {"name": "description"})
    description = meta["content"] if meta["content"] else None

    return {'h1': h1, 'title': title, 'description': description}

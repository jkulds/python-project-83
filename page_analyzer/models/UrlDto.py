from datetime import datetime

from page_analyzer.models.UrlCkeckDto import UrlCheckDto


class UrlDto:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.id = kwargs.get('id', 0)
        self.last_url_check = UrlCheckDto(**kwargs)

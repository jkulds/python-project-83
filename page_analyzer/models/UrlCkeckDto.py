from datetime import datetime


class UrlCheckDto:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)
        self.url_id = kwargs.get('url_id', 0)
        self.status_code = kwargs.get('status_code')
        self.h1 = kwargs.get('h1', '')
        self.description = kwargs.get('description', '')
        self.title = kwargs.get('title', '')
        self.created_at = kwargs.get('created_at', datetime.now())

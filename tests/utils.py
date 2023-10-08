import os
from os.path import splitext
import json


def get_fixture_content(file_name):
    full_path = f'{os.path.dirname(__file__)}/fixtures/{file_name}'
    _, extension = splitext(full_path)
    with open(full_path) as content_file:
        if extension == '.json':
            return json.loads(content_file.read())
        else:
            return content_file.read()

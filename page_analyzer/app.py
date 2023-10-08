import os
from pathlib import Path
from urllib.parse import urlparse

import psycopg2
import validators as validators
from flask import Flask, render_template, redirect, request, flash, get_flashed_messages
from dotenv import load_dotenv, find_dotenv
from page_analyzer.UrlRepository import UrlRepository

from page_analyzer.UrlDto import UrlDto
from page_analyzer.db import create_default_table

app = Flask(__name__)
if "SECRET_KEY" not in os.environ:
    load_dotenv(find_dotenv())
app.secret_key = os.getenv('SECRET_KEY')
db_connection = psycopg2.connect(os.getenv('DATABASE_URL'))
db_connection.autocommit = True
create_default_table(db_connection, f'{str(Path(os.path.dirname(__file__)).parent)}/database.sql')
repository = UrlRepository(db_connection)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.get('/urls')
def url_list():
    urls = repository.get_all()
    return render_template('urls/list.html', urls=urls)


@app.post('/urls')
def create_url():
    data = request.form.to_dict()
    if len(data) == 0:
        return redirect('/')
    str_url = data['url']
    is_valid = validators.url(str_url)
    if not is_valid:
        flash("Некорректный URL", 'danger')
        return redirect('/')

    parsed_url = urlparse(str_url)

    correct_name = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    is_exists = repository.is_exists(correct_name)
    if is_exists:
        flash("Такая запись уже существует", 'danger')
        return redirect('/')

    url = UrlDto(name=correct_name)
    created_url = repository.add(url)

    return redirect(f'/urls/{created_url.id}')


@app.get('/urls/<id>')
def get_url_detail(id):
    url = repository.get_by_id(id)
    return render_template('urls/single.html', url=url)


@app.post("/urls/<id>/checks")
def checks():
    return 'test'

def create_app():
    return app


if __name__ == '__main__':
    app.run()



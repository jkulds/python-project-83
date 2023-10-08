import os
from pathlib import Path
from urllib.parse import urlparse

import psycopg2
import validators as validators
from flask import Flask, render_template, redirect, request, flash, url_for
from dotenv import load_dotenv, find_dotenv
from page_analyzer.UrlRepository import UrlRepository
from page_analyzer.models.UrlCkeckDto import UrlCheckDto

from page_analyzer.models.UrlDto import UrlDto
from page_analyzer.db import create_default_table

app = Flask(__name__)
if "SECRET_KEY" not in os.environ:
    load_dotenv(find_dotenv())
app.secret_key = os.getenv('SECRET_KEY')

create_default_table(f'{str(Path(os.path.dirname(__file__)).parent)}/database.sql')

repository = UrlRepository()


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

    return redirect(url_for('get_url_detail', id=created_url.id))


@app.get('/urls/<id>')
def get_url_detail(id):
    url = repository.get_by_id(id)
    url_checks = repository.get_checks_by_url_id(id)
    return render_template('urls/single.html', url=url, url_checks=url_checks)


@app.post("/urls/<id>/checks")
def checks(id):
    url_check = UrlCheckDto(url_id=id)
    repository.add_check(url_check)
    return redirect(url_for('get_url_detail', id=id))


def create_app():
    return app


if __name__ == '__main__':
    app.run()



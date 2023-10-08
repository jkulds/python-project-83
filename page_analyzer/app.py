import os
from pathlib import Path
from urllib.parse import urlparse

import requests as requests
import validators as validators
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, redirect, request, flash, url_for

from page_analyzer.UrlRepository import UrlRepository
from page_analyzer.db import bootstrap
from page_analyzer.models.UrlCkeckDto import UrlCheckDto
from page_analyzer.models.UrlDto import UrlDto

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

bootstrap(f'{str(Path(os.path.dirname(__file__)).parent)}/database.sql')

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

    return redirect(url_for('get_url_detail', url_id=created_url.id))


@app.get('/urls/<url_id>')
def get_url_detail(url_id):
    url = repository.get_by_id(url_id)
    url_checks = repository.get_checks_by_url_id(url_id)
    return render_template('urls/single.html', url=url, url_checks=url_checks)


@app.post("/urls/<url_id>/checks")
def checks(url_id):
    url = repository.get_by_id(url_id)
    try:
        response = requests.get(url.name, timeout=5)
    except (requests.ConnectionError, requests.Timeout, requests.RequestException):
        flash('Произошла ошибка при проверке', 'danger')
    else:
        if response.status_code == 200:
            url_check = UrlCheckDto(url_id=url_id, status_code=response.status_code)
            repository.add_check(url_check)
        else:
            flash('Произошла ошибка при проверке', 'danger')
    finally:
        return redirect(url_for('get_url_detail', url_id=url_id))


def create_app():
    return app


if __name__ == '__main__':
    app.run()

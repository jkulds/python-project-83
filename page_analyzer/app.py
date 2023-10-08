import os
from pathlib import Path

import requests as requests
import validators as validators
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, redirect, request, flash, url_for

from page_analyzer.UrlRepository import UrlRepository
from page_analyzer.db_utils import bootstrap
from page_analyzer.models.UrlCkeckDto import UrlCheckDto
from page_analyzer.models.UrlDto import UrlDto
from page_analyzer.seo_parser import get_seo_info_dict
from page_analyzer.utils import normalize_url

if "SECRET_KEY" not in os.environ:
    load_dotenv(find_dotenv())

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

    str_url = data['url']
    is_valid = validators.url(str_url)
    if not is_valid:
        flash("Некорректный URL", 'danger')
        return render_template('index.html', url=data), 422

    correct_name = normalize_url(str_url)

    is_exists = repository.is_exists(correct_name)
    if is_exists:
        flash("Страница уже существует", 'info')
        return redirect('/')
    else:
        url = UrlDto(name=correct_name)
        created_url = repository.add(url)
        flash('Страница успешно добавлена', 'success')
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
    except (
        requests.ConnectionError, requests.Timeout,
        requests.RequestException
    ):
        flash('Произошла ошибка при проверке', 'danger')
    else:
        if response.status_code == 200:
            seo_dict = get_seo_info_dict(response.text)
            url_check = UrlCheckDto(url_id=url_id,
                                    status_code=response.status_code,
                                    **seo_dict)
            repository.add_check(url_check)
            flash('Проверка прошла успешно', 'success')
        else:
            print(response.status_code, response.text)
            flash('Произошла ошибка при проверке', 'danger')
    finally:
        return redirect(url_for('get_url_detail', url_id=url_id))


def create_app():
    return app

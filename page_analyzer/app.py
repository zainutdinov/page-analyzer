import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (Flask, flash, get_flashed_messages, redirect,
                   render_template, request, url_for)
import requests
from validators import url as validate_url
from page_analyzer.database import UrlRepository

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

database_exec = UrlRepository()


@app.route('/')
def home():
    messages = get_flashed_messages(with_categories=True)
    return render_template('start_page.html', messages=messages)


@app.route('/urls', methods=['POST'])
def post_url():
    url = request.form.get('url')
    parsed_url = urlparse(url)
    normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    if not validate_url(normalized_url):
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('start_page.html', messages=messages), 422
    url_id = database_exec.get_url_id(normalized_url)
    if url_id:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_urls_checks_list', id=url_id))
    url_data = database_exec.create_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_urls_checks_list', id=url_data.id))


@app.route('/urls', methods=['GET'])
def get_urls_list():
    messages = get_flashed_messages(with_categories=True)
    all_urls = database_exec.get_all_urls_list()
    return render_template('urls_list.html', messages=messages,
                           urls=all_urls), 200


@app.route('/urls/<int:id>', methods=['GET'])
def get_urls_checks_list(id):
    messages = get_flashed_messages(with_categories=True)
    url_data = database_exec.get_url_from_urls_list(id)
    if not url_data:
        return render_template('url_id_error.html'), 200
    checks_data = database_exec.get_checks_from_urls_checks_list(id)
    return render_template('url_id.html', messages=messages,
                           url=url_data, checks=checks_data), 200


@app.route('/urls/<int:id>/checks', methods=['POST'])
def post_check_url(id):
    url_data = database_exec.get_url_from_urls_list(id)
    url = url_data.name
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_urls_checks_list', id=id, code=400))
    response_code = response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else None
    h1_tag = soup.find('h1')
    h1 = h1_tag.get_text(strip=True) if h1_tag else None
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = (description_tag["content"] if description_tag
                   and "content" in description_tag.attrs else None)
    url_data = database_exec.create_check(id, response_code,
                                          h1, title, description)
    if url_data:
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_urls_checks_list', id=url_data.url_id))

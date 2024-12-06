from flask import (Flask, render_template, request, redirect,
                   url_for, flash, get_flashed_messages)
from validators import url as validate_url
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
from page_analyzer.database import UrlRepository

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

database_exec = UrlRepository()


@app.route('/')
def home():
    messages = get_flashed_messages(with_categories=True)
    return render_template('start_page.html', messages=messages)


@app.post('/urls')
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


@app.get('/urls')
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
                           url=url_data, check=checks_data), 200


@app.route('/urls/<int:id>/checks', methods=['POST'])
def post_check_url(id):
    url_data = database_exec.create_check(id)
    if url_data:
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_urls_checks_list', id=url_data.url_id))

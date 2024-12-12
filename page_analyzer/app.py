import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.database import UrlRepository
from page_analyzer.tools import parse_html, validate_and_normalize_url

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

url_repository = UrlRepository()


@app.route("/")
def show_homepage():
    messages = get_flashed_messages(with_categories=True)
    return render_template("start_page.html", messages=messages)


@app.route("/urls", methods=["POST"])
def post_url():
    url = request.form.get("url")
    normalized_url = validate_and_normalize_url(url)
    if not normalized_url:
        flash("Некорректный URL", "danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template("start_page.html", messages=messages), 422
    url_id = url_repository.get_url_id(normalized_url)
    if url_id:
        flash("Страница уже существует", "warning")
        return redirect(url_for("get_urls_checks_list", id=url_id))
    url_data = url_repository.create_url(normalized_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("get_urls_checks_list", id=url_data.id))


@app.route("/urls", methods=["GET"])
def get_urls_list():
    messages = get_flashed_messages(with_categories=True)
    all_urls = url_repository.get_all_urls()
    return render_template("urls_list.html", messages=messages, urls=all_urls)


@app.route("/urls/<int:id>", methods=["GET"])
def get_urls_checks_list(id):
    messages = get_flashed_messages(with_categories=True)
    url_data = url_repository.get_url(id)
    if not url_data:
        return render_template("url_id_error.html"), 404
    checks_data = url_repository.get_checks(id)
    return render_template(
        "url_id.html", messages=messages, url=url_data, checks=checks_data
    ), 200


@app.route("/urls/<int:id>/checks", methods=["POST"])
def post_check_url(id):
    url_data = url_repository.get_url(id)
    if not url_data:
        return render_template("url_id_error.html"), 404
    url = url_data.name
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("get_urls_checks_list", id=id, code=400))
    resp_code, title, h1, descrip = parse_html(response)
    url_data = url_repository.create_check(id, resp_code, h1, title, descrip)
    if url_data:
        flash("Страница успешно проверена", "success")
        return redirect(url_for("get_urls_checks_list", id=url_data.url_id))

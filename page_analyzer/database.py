import datetime
import os

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import NamedTupleCursor

load_dotenv()


def connection_init():
    DATABASE_URL = os.getenv('DATABASE_URL')
    try:
        connection = psycopg2.connect(DATABASE_URL)
        return connection
    except Exception:
        print('Cant establish connection to database')


def execute_database(func):
    def inner(*args, **kwargs):
        with connection_init() as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
                result = func(cursor=cursor, *args, **kwargs)
                return result
    return inner


class UrlRepository:
    @execute_database
    def create_url(self, url, cursor=None):
        date = datetime.date.today()
        cursor.execute("INSERT INTO urls (name, created_at) "
                       "VALUES (%s, %s) RETURNING id, name, created_at",
                       (url, date))
        url_data = cursor.fetchone()
        return url_data

    @execute_database
    def get_url_id(self, url, cursor=None):
        cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
        url_id = cursor.fetchone()
        if not url_id:
            return None
        return url_id.id

    @execute_database
    def get_all_urls_list(self, cursor=None):
        cursor.execute("SELECT u.*, "
                       "(SELECT c.response_code "
                       "FROM urls_checks AS c "
                       "WHERE c.url_id = u.id "
                       "ORDER BY c.id DESC LIMIT 1) "
                       "AS response_code "
                       "FROM urls AS u ORDER BY id DESC")
        urls = cursor.fetchall()
        return urls

    @execute_database
    def get_url_from_urls_list(self, url_id, cursor=None):
        cursor.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
        url_data = cursor.fetchone()
        if not url_data:
            return None
        return url_data

    @execute_database
    def create_check(self, url_id, response_code, h1, title,
                     description, cursor=None):
        date = datetime.date.today()
        cursor.execute("INSERT INTO urls_checks "
                       "(url_id, response_code, h1, title, "
                       "description, created_at) "
                       "VALUES (%s, %s, %s, %s, %s, %s) "
                       "RETURNING id, url_id, created_at",
                       (url_id, response_code, h1, title, description, date))
        url_data = cursor.fetchone()
        return url_data

    @execute_database
    def get_checks_from_urls_checks_list(self, url_id, cursor=None):
        cursor.execute("SELECT * FROM urls_checks WHERE url_id=%s "
                       "ORDER BY id DESC", (url_id,))
        url_data = cursor.fetchall()
        return url_data

<div align="center">
<h1>Анализатор страниц</h1>
</div>

## Ссылка на проект: https://python-project-83-40k2.onrender.com/


### Hexlet tests and linter status:
[![Actions Status](https://github.com/zainutdinov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/zainutdinov/python-project-83/actions)

### Python CI Badge
[![Python CI](https://github.com/zainutdinov/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/zainutdinov/python-project-83/actions/workflows/pyci.yml)

### CodeClimate Badges
[![Maintainability](https://api.codeclimate.com/v1/badges/af6a6a9b49b07909571a/maintainability)](https://codeclimate.com/github/zainutdinov/python-project-83/maintainability)


## Описание проекта
Анализатор страниц - это сайт, который анализирует указанные страницы на SEO-пригодность по аналогии с PageSpeed Insights.

## Требования

- python 3.11.10
- poetry ^1.8.3
- flask ^3.1.0
- python-dotenv ^1.0.1
- psycopg2-binary ^2.9.10
- validators ^0.34.0
- requests ^2.32.3
- beautifulsoup4 ^4.12.3

## Инструкция по установке

> Чтобы использовать пакет, вам нужно скопировать репозиторий на свой компьютер. Это делается с помощью команды ``git clone``:

```bash
git clone https://github.com/zainutdinov/python-project-83
```

> Далее выполните установку пакета:

```bash
cd python-project-83
```

```bash
poetry build
python3 -m pip install --user dist/*.whl
```

> Создайте файл .env в корневой директории проекта. Добавьте в него две переменные: DATABASE_URL и SECRET_KEY.

- SECRET_KEY может быть сгенерирован или введён вручную.
- DATABASE_URL должен иметь следующий формат: {provider}://{user}:{password}@{host}:{port}/{db}


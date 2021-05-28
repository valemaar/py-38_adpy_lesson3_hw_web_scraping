import requests

import re

from bs4 import BeautifulSoup

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://www.habr.com/ru/all/'
response = requests.get(url)

if not response.ok:
    raise ValueError('no response')

text = response.text
soup = BeautifulSoup(text, features="html.parser")

articles = soup.find_all('article')


# находит текст по параметрам в soup, разбивает его на слова и добавляет в множество
def split_my_text(article_found, art_tag, art_class):
    pattern = r'[а-яёЁА-Яa-zA-Z\d]*'
    splited = set()
    for el in article_found.find_all(art_tag, class_=art_class):
        splited_1 = re.findall(pattern, el.text.lower())
        splited.update(splited_1)
    return splited


for article in articles:
    full_texts = set()
    pattern = r'[а-яёЁА-Яa-zA-Z\d]*'

    # добавляем весь текст статьи во множество
    full_article_url = article.find('a', class_='btn_outline_blue').attrs.get('href')
    full_art_res = requests.get(full_article_url)
    if not full_art_res.ok:
        raise ValueError('no full_art_res')
    full_text_raw = full_art_res.text
    soup_1 = BeautifulSoup(full_text_raw, features="html.parser")
    full_text = re.findall(pattern, soup_1.find('div', id='post-content-body').text.lower())
    full_texts.update(full_text)

    titles = split_my_text(article, 'a', 'post__title_link')
    authors = split_my_text(article, 'span', 'user-info__nickname')
    article_preview = split_my_text(article, 'div', 'post__text')
    hubs = split_my_text(article, 'a', 'hub-link')

    hubs.update(authors)  # добавляем автора статьи во множество
    hubs.update(titles)  # добавляем заголовок статьи во множество
    hubs.update(article_preview)  # добавляем текст превью статьи во множество
    hubs.update(full_texts)  # добавляем хабы (тэги) статьи во множество

    # проверяем есть ли ключевые слова в наших множествах
    if set(KEYWORDS) & hubs:
        article_href = article.find('a', class_="post__title_link").attrs.get('href')
        article_publish_date = article.find('span', class_="post__time").text
        article_title = article.find('a', class_='post__title_link').text
        print(f'\n<{article_publish_date}>-<"{article_title}">-<{article_href}>')

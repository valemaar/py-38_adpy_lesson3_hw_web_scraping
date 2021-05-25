import requests

from bs4 import BeautifulSoup

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://www.habr.com/ru/all/'
response = requests.get(url)

if not response.ok:
    raise ValueError('no response')

text = response.text
soup = BeautifulSoup(text, features="html.parser")
posts_list = soup.find('div', class_='posts_list')
posts_ul = posts_list.find('ul', class_='content-list')

posts_li = posts_ul.find_all('li', class_='content-list__item')

# posts_authors = posts_li.find_all('span', class_='user-info__nickname')
# posts_titles = posts_li.find_all('a', class_='post__title_link')
# posts_hubs = posts_li.find_all('a', class_='hub-link')


# print(posts_li)

for post in posts_li:
    # print('post', post, 'post')
    print()
    print('nickname', '--', post.find('span', class_='user-info__nickname').text)
    print('title', '--', post.find('a', class_='post__title_link').text)
    print('hub', '--', post.find('a', class_='inline-list__item-link').text)

from bs4 import BeautifulSoup
import requests

# веб-сайт, который хотим спарсить
url = 'https://www.banki.ru/investment/responses/list/'
# определим главную страницу
root = 'https://www.banki.ru'

# GET()-запрос на сайт
page = requests.get(url)
# проверка подключения
print(page.status_code)

# получаем содержимое страницы
content = page.text
# создаем объект BeautifulSoup
soup = BeautifulSoup(content, "lxml")

# сохраняем все с тэгом 'article' и классом 'responses__item'
# в них будет находится весь код отзыва, включая заголовок, оценку, текст и прочее
allfd = soup.find_all('article', class_="responses__item")

# воспользуемся циклом, чтобы получить все необходимые ссылки
links = []
for href in allfd:
    links.append(href.find('a', href=True)['href'])


with open ('banks_one_page.json', 'a+', encoding="utf-8") as file:
    for link in links:
        result = requests.get(f'{root}{link}')
        if (page.status_code == 200):
            content = result.text
            soup = BeautifulSoup(content, 'lxml')
            fd = soup.find('div', class_='article-text response-page__text markup-inside-small markup-inside-small--bullet').get_text(strip=True, separator=' ')
            title = soup.find('h1').get_text(strip=True, separator=' ')
            json.dump({'title': title,'review': fd}, file, ensure_ascii=False, indent=4)


i = 1
page = requests.get(f'https://www.banki.ru/investment/responses/list?page={i}&isMobile=0')
with open ('banks_all_pages.json', 'a+', encoding="utf-8") as file:
    while (page.status_code == 200):
        content = page.text
        soup = BeautifulSoup(content, "lxml")
        allfd = soup.find_all('article', class_="responses__item")

        links = []
        for href in allfd:
            links.append(href.find('a', href=True)['href'])

        for link in links:
            result = requests.get(f'{root}{link}')
            if (page.status_code == 200):
                #time.sleep(1)
                content = result.text
                soup = BeautifulSoup(content, 'lxml')
                fd = soup.find('div', class_='article-text response-page__text markup-inside-small markup-inside-small--bullet').get_text(strip=True, separator=' ')
                title = soup.find('h1').get_text(strip=True, separator=' ')
                json.dump({'title': title,'review': fd}, file, ensure_ascii=False, indent=4)
        i += 1
        page = requests.get(f'https://www.banki.ru/investment/responses/list?page={i}&isMobile=0')


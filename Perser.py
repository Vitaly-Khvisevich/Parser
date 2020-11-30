import requests
from bs4 import BeautifulSoup
import os
import csv


URL=''
file_name=''
l=[]
imp=[]
Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
'accept':'*/*'}
chech='ajax_block_product '


def update_html(URL, Headers):
    html=requests.get(URL,headers=Headers)
    print(f"Проверка доступности сайта {URL}")
    if html.status_code==200:
        print('Сайт доступен')
    else:
        print('Сайт недоступен')

    parsing_html(html.text, URL)

def parsing_html(html, URL):
    B_html=BeautifulSoup(html,'html.parser')
    print('Проверяем является ли страница страницей товара')
    if chech in html:
        print('Страница не является страницей товара, проверяем ссылки на странице')
        for i in B_html.find_all('a', class_="product-name"):
            l.append(i.get('href'))
        arr_a(l)
    else:
        print(f"Страница {URL} является страницей товара, формируем список данных")
        try:

            imp.append({
                'title': B_html.find('h1', class_='product_main_name').get_text(),
                'description':B_html.find('div', id='short_description_content').get_text().strip(),
                'old_price': B_html.find('span', id='old_price_display').get_text(),
                'new_price': B_html.find('span', id='our_price_display').get_text(),
                'picture': B_html.find('img', id='bigpic').get('src'),
                'link': URL
        })
        except AttributeError:
            print("Ошибка")
        note_it(imp, file_name)
    
def arr_a(l):
    for i in l:
        update_html(i, Headers)
    l.clear()


def note_it(imp, file_name):
    if os.path.isfile(file_name):
        with open (file_name, 'a', newline='') as file:
            writer= csv.writer(file, delimiter=';', )
            for item in imp:
                try:
                    item['description']=item['description'].encode('cp850').decode('cp866')
                except UnicodeEncodeError:
                    break
                writer.writerow([item['title'], item['description'], item['old_price'], item['new_price'], item['picture'],item['link']])

    else:
        with open (file_name, 'a', newline='') as file:
            writer= csv.writer(file, delimiter=';', )
            writer.writerow(['Название', 'Описание', 'Старая цена','Новая цена','Картинка','Ссылка'])
            for item in imp:
                try:
                    item['description']=item['description'].encode('cp850').decode('cp866')
                except UnicodeEncodeError:
                    break
                writer.writerow([item['title'], item['description'], item['old_price'], item['new_price'], item['picture'],item['link']])


print('Добро пожаловать в parser сайта https://www.petsonic.com')
URL=input('Введите ссылке на категорию продукции: ', )
file_name=(input('Введите название файла в который Вы хотите саписывать данные: ', ))+'.csv'

update_html(URL,Headers)
os.startfile(file_name)
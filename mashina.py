import requests
from bs4 import BeautifulSoup as bs
import csv


def get_html(url):
    response = requests.get(url)
    return response.text


def get_total_pages(html):
    soup = bs(html, 'html.parser')
    pages = soup.find('ul', class_ = 'pagination')
    last_page = pages.find_all('a')[-1]
    total_pages = last_page.get('href').split('=')[-1]
    return int(total_pages)


def write_to_csv(data):
    with open('mashina_kg.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'],
                        data['price'],
                        data['description'],
                        data['photo']])



def get_page_data(html):
    soup = bs(html, 'html.parser')
    product_list = soup.find('div', class_ = 'search-results-table')
    # print(product_list)
    products = product_list.find_all('div', class_='list-item list-label')
    # print(products)    
    for product in products:
        try:
            title = product.find('div', class_='block title').text.strip()
            # print(title)
        except:
            title = ''

        try:
            price = product.find('div', class_='block price').find('strong').text
            # print(price)
        except:
            price = ''

        try:
            desc = product.find('div', class_='block info-wrapper item-info-wrapper').text.split()
            str_desc = ''.join(desc)
            # print(str_desc)
        except:
            desc = ''
        try:
            photo = product.find('img').get('src')
            # print(photo)
        except:
            photo = ''

        data = {
            'title': title,
            'price': price,
            'description': str_desc,
            'photo': photo
        }
        print(data)
        write_to_csv(data)


def main():
    url = 'https://www.mashina.kg/search/all/'
    pages = '?page='

    # total_pages = get_total_pages(get_html(url))
    for page in range(1, 4):
        url_with_page = url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)

with open('mashina_kg.csv', 'w') as file:                                              
    writer = csv.writer(file)
    writer.writerow(['title',   'price',    'description',    'img'])

main()
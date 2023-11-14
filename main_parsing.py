import requests
from bs4 import BeautifulSoup as bs
import csv
import asyncio

link = 'https://art-ari.ru/katalog/keramogranit/'
all_page_link = [link + f'?page={i}' for i in range(1, 2530)][:2]


class ParsingArtAri(requests.Session, bs):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.response = [self.get(i) for i in self.url]
        self.soup = [bs(x.text, 'lxml') for x in self.response]

    def response_link_product(self):
        '''
        Метод возвращает ссылки всех страниц
        '''
        all_page = []
        all_cattegories = map(lambda x_soup: x_soup.find('div', class_='category_products'), self.soup)
        link_product = list(map(lambda x_all: x_all.find_all('div', class_='image'), all_cattegories))
        for y in link_product:
            all_page.append(
                [
                    str(i).split()[7].replace(
                        'href="', ''
                    ).replace(
                        '>', ''
                    ).replace(
                        'amp;', ''
                    ).replace('"', '')
                    for i in y
                ]
            )

        return sum(all_page, [])

    def get_name_product(self):
        name_product = []
        for i in self.response_link_product()[:2]:  # Убрать [:2]
            respon = self.get(i)
            soup = bs(respon.text, 'lxml')
            name_product.append(soup.find('span', class_='micro-name').text)
        return name_product

    def get_photo(self):
        '''
        Метод возвращает ссылки на изображения товаров
        '''
        photo_link = []
        price_product = []
        for i in self.response_link_product()[:2]:

            respon = self.get(i)
            soup = bs(respon.text, 'lxml')
            container_photo = soup.find('div', class_='col-sm-6 left-info').find_all('a', class_='cloud-zoom', href=True)
            price_product.append(
                soup.find('div', class_='product-price').text.strip()
            )
            for y in container_photo:
                photo_link.append(
                    str(y).split()[4].replace('href="', '').replace('"', '')
                )

        return photo_link, price_product

    def get_info(self):
        '''
        Метод возвращает всю информацию о товаре
        '''

        all_info = []
        for i in self.response_link_product()[:2]:

            respon = self.get(i)
            soup = bs(respon.text, 'lxml')
            cont = soup.find('div', class_='row product-tabs-row').text.split('\n')
            info = filter(None, cont)
            all_info.append(list(info)[3:])

        return all_info

    def get_articule(self):
        '''
        Метод возвращает артикуль товара
        '''
        ...




parsing = ParsingArtAri(all_page_link)
# print(parsing.response_link_product())  # Все ссылки категории со всех страниц
print(parsing.get_info())

# name_products = parsing.get_name_product()  # Все Наименования продуктов
# photo, price = parsing.get_photo()
# print(name_products)
# print(photo)
# print(price)






# with open('data.csv', 'w', encoding='utf-8', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Заголовок', 'URL'])
#
#     for i in parsing.all_page:
#         for y in parsing.get_name_product():
#             writer.writerow([y, i])

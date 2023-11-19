import json

from openpyxl.drawing.image import Image
from PIL import Image
from io import BytesIO
import requests
import openpyxl

with open('klinker.json', 'r', encoding='utf8') as file:
    data = json.load(file)


book = openpyxl.Workbook()
sheet = book.active

sheet['A1'] = 'Артикул'
sheet['B1'] = 'Название товара'
sheet['C1'] = 'Цена'
sheet['D1'] = 'Характеристики'
sheet['E1'] = 'Ссылка на товар'
sheet['F1'] = 'Ссылка на изображение'

# dict_haract = []
row = 2
for product in data:
    sheet[row][0].value = product['Артикул']
    sheet[row][1].value = product['Название']
    sheet[row][2].value = product['Цена']
    sheet[row][3].value = str(product['Характеристики'])[1:-1]
    sheet[row][4].value = product['Cсылка на товар']
    sheet[row][5].value = product['Изображение']
    row += 1

book.save('КЛИНКЕР.xlsx')

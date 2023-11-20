import csv
import requests
import os

with open('krup_keramo.csv', encoding='utf-8') as file:  # Открыть файл csv
    file_rider = csv.reader(file, delimiter=',')
    link_img = [i[-2] for i in file_rider][1:]

folder = 'Изображения клинкер'  # имя папки для сохранения изображений

if not os.path.exists(folder):
    os.makedirs(folder)

for i in range(len(link_img)):  # Перебрать все ссылки на изображения и скачать их
    img_data = requests.get(link_img[i])
    with open(os.path.join(folder, f'{str(i)}.jpg'), 'wb') as file:
        file.write(img_data.content)
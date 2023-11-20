import scrapy


class CatalogSpider(scrapy.Spider):
    name = "catalog"
    allowed_domains = ["art-ari.ru"]
    start_urls = [f'https://art-ari.ru/katalog/keramogranit/?page={i}' for i in range(29 + 1)][:2]

    def start_requests(self):
        for i in range(len(self.start_urls)):
            if i == 0:
                yield scrapy.Request('https://art-ari.ru/katalog/keramogranit/', callback=self.parse_in_categories)
            else:
                yield scrapy.Request(self.start_urls[i], callback=self.parse_in_categories)

    def parse_in_categories(self, response):
        for href in response.css('div.h4 a::attr("href")').extract():
            yield response.follow(href, callback=self.parse)
        #
        # for collections in response.css('div.item.subcat-box.col-md-4.col-sm-4.col-xs-12 a::attr(href)').extract():
        #     yield response.follow(collections, callback=self.parse)

    def parse(self, response, **kwargs):
        # article = 'Нет Арти' if None is response.css(
        #     'li.product-info-li.main-product-sku strong::text').get() else response.css(
        #     'li.product-info-li.main-product-sku strong::text').get()

        name_product = response.css('h1.product-header::text').get()
        price = 'Цена по запросу' if None is response.css('div.oct-price-normal::text').get() else response.css(
            'div.oct-price-normal::text').get()

        manufacturer = response.xpath('//*[@id="product"]/ul/li[1]/a/span').get().replace(
            '<span itemprop="brand">', '').replace('</span>', '')

        collection = ''.join(response.xpath('//*[@id="product"]/ul/li[2]/a/span').get().split()).replace('<span',
                                                                                                         '').replace(
            'rel="nofollow"', '').replace(
            'itemprop="brand">', ''
        ).replace(
            '</span>', ''
        ).strip()

        link_product = response.request.url
        link_img = ''.join(response.css('li.image.thumbnails-one.thumbnail a::attr(href)').extract())
        link_collection = response.css('li.product-info-li a::attr(href)').extract()[1]
        characteristics = dict(zip(response.css('div.attr-td.oct-attr-name span::text').extract(),
                                   response.css('div.attr-td::text').extract()))
        item = {
            'Артикул': name_product.split()[1],
            'Название': name_product,
            'Цена': price,
            'Производитель': manufacturer,
            'Коллекция': collection,
            'Единица измерения': '' if not characteristics.get('Единица измерения') else characteristics[
                'Единица измерения'],
            'Длина, см': '' if not characteristics.get('Длина, см') else characteristics['Длина, см'],
            'Назначение': '' if not characteristics.get('Назначение') else characteristics['Назначение'],
            'Микс': '' if not characteristics.get('Микс') else characteristics['Микс'],
            'Площадь, м2': '' if not characteristics.get('Площадь, м2') else characteristics['Площадь, м2'],
            'Размер, см': '' if not characteristics.get('Размер, см') else characteristics['Размер, см'],
            'Ректификат': '' if not characteristics.get('Ректификат') else characteristics['Ректификат'],
            'Рисунок': '' if not characteristics.get('Рисунок') else characteristics['Рисунок'],
            'Страна': '' if not characteristics.get('Страна') else characteristics['Страна'],
            'Толщина, мм': '' if not characteristics.get('Толщина, мм') else characteristics['Толщина, мм'],
            'Форма': '' if not characteristics.get('Форма') else characteristics['Форма'],
            'Кол-во плитки в коробке, шт.': '' if not characteristics.get('Кол-во плитки в коробке, шт.') else characteristics['Кол-во плитки в коробке, шт.'],
            'Поверхность': '' if not characteristics.get('Поверхность') else characteristics['Поверхность'],
            'Цвет': '' if not characteristics.get('Цвет') else characteristics['Цвет'],
            'Помещение': '' if not characteristics.get('Помещение') else characteristics['Помещение'],
            'Cсылка на товар': link_product,
            'Ссылка на изображение': link_img,
            'Ссылка на коллекцию': link_collection,
            # 'Ссылка изображения на коллекцию': response.css('li.image.thumbnails-one.thumbnail a::attr(href)').get()
        }

        yield item


# class CatalogSpider(scrapy.Spider):
#     name = "catalog"
#     allowed_domains = ["art-ari.ru"]
#     start_urls = [f'https://art-ari.ru/katalog/keramogranit/?page={i}' for i in range(2 + 1)]
#
#     def start_requests(self):
#         for i in range(len(self.start_urls)):
#             if i == 0:
#                 yield scrapy.Request('https://art-ari.ru/katalog/keramogranit/', callback=self.parse_in_categories)
#             else:
#                 yield scrapy.Request(self.start_urls[i], callback=self.parse_in_categories)
#
#     def parse_in_categories(self, response):
#         for collections in response.css('div.item.subcat-box.col-md-4.col-sm-4.col-xs-12 a::attr(href)').extract():
#             yield response.follow(collections, callback=self.parse)
#
#     def parse(self, response, **kwargs):
#         item = {
#             'Имя коллекции': response.css('h1.cat-header::text').get(),
#             'Главное изображение': response.css('li.image.thumbnails-one.thumbnail a::attr(href)').get(),
#             'Дополнительные изображения': '\n'.join(response.css('div.image-additional a::attr(href)').extract())
#         }
#
#         yield item
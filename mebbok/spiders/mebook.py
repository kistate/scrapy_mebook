# -*- coding: utf-8 -*-
import scrapy
from mebbok.items import MebbokItem

class MebookSpider(scrapy.Spider):
    page = 1
    name = 'mebook'
    allowed_domains = ['shuwu.mobi']
    start_urls = ['http://www.shuwu.mobi']

    def start_requests(self):
        urls = [
            "http://www.shuwu.mobi/date/2019/08",
            "http://www.shuwu.mobi/date/2019/07",
            "http://www.shuwu.mobi/date/2019/06",
            "http://www.shuwu.mobi/date/2019/05",
            "http://www.shuwu.mobi/date/2019/04",
            "http://www.shuwu.mobi/date/2019/03",
            "http://www.shuwu.mobi/date/2019/02",
            "http://www.shuwu.mobi/date/2019/01",
            "http://www.shuwu.mobi/date/2018/12",
            "http://www.shuwu.mobi/date/2018/11",
            "http://www.shuwu.mobi/date/2018/10",
            "http://www.shuwu.mobi/date/2018/09",
            "http://www.shuwu.mobi/date/2018/08",
            "http://www.shuwu.mobi/date/2018/07",
            "http://www.shuwu.mobi/date/2018/06",
            "http://www.shuwu.mobi/date/2018/05",
            "http://www.shuwu.mobi/date/2018/04",
            "http://www.shuwu.mobi/date/2018/03",
            "http://www.shuwu.mobi/date/2018/02",
            "http://www.shuwu.mobi/date/2018/01",
            "http://www.shuwu.mobi/date/2017/12",
            "http://www.shuwu.mobi/date/2017/11",
            "http://www.shuwu.mobi/date/2017/10",
            "http://www.shuwu.mobi/date/2017/09",
            "http://www.shuwu.mobi/date/2017/08",
            "http://www.shuwu.mobi/date/2017/07",
            "http://www.shuwu.mobi/date/2017/06",
            "http://www.shuwu.mobi/date/2017/05",
            "http://www.shuwu.mobi/date/2017/04",
            "http://www.shuwu.mobi/date/2017/03",
            "http://www.shuwu.mobi/date/2017/02",
            "http://www.shuwu.mobi/date/2017/01",
            "http://www.shuwu.mobi/date/2016/12",
            "http://www.shuwu.mobi/date/2016/11",
            "http://www.shuwu.mobi/date/2016/10",
            "http://www.shuwu.mobi/date/2016/09",
            "http://www.shuwu.mobi/date/2016/08",
            "http://www.shuwu.mobi/date/2016/07",
            "http://www.shuwu.mobi/date/2016/06"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.page += 1
        self.log('CURRENT PAGE ' + str(self.page))
        for item in response.css('.list li'):
            url = item.css('.content h2 a').attrib.get('href')
            yield scrapy.Request(url, callback=self.parse_book)
        next_page = response.css('.pagenavi .current+a').attrib.get('href')
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_book(self, response):
        down_url = response.css('.downbtn').attrib.get('href')
        self.log(down_url)
        if not down_url:
            return
        down_page = scrapy.Request(url=down_url, callback=self.parse_download, priority=10)
        down_page.meta['item'] = {
            'title': response.xpath('//*[@id="primary"]/h1/text()').get(),
            'cover': response.xpath('//*[@id="content"]/p/img').attrib.get('src'),
            'category': response.css('#primary > div.postinfo > div.left > a::text').getall(),
            'intro': response.css('#link-report > div > div.intro').get(),
            # 'down_url': down_url
        }
        yield down_page

    def parse_download(self, response):
        item = response.meta['item']
        item['down_info'] = response.css('body > div:nth-child(4) > p:nth-child(7)::text').get()
        item['target_urls'] = response.css('body > div.list a').getall()
        book_item = MebbokItem(item)
        self.log(book_item)
        yield book_item

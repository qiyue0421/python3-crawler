# -*- coding: utf-8 -*-
import scrapy
from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')  # 首先选取所有的quote，并将其赋值为quotes变量
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()  # 获取结果列表的第一个元素
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()  # 获取所有结果组成的列表
            yield item
        next = response.css('.pager .next a::attr("href")').extract_first()  # 首先使用CSS选择器获取下一个页面的链接，然后再调用extract_first()方法获取内容
        url = response.urljoin(next)  # 使用urljoin()方法将相对URL构造成一个绝对URL
        # 通过url和callback变量构造了一个新的请求，这个请求完成后，响应会重新经过parse方法处理，得到第二页的解析结果，然后生成第二页的下一页，也就是第三页的请求，这样就进入了一个循环，直到最后一页
        yield scrapy.Request(url=url, callback=self.parse)

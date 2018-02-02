# -*- coding: utf-8 -*-
import scrapy
from quotetutorial.items import Quote


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    
    def parse(self, response):
        # print(response.text)
        quotes = response.css('.quote')
        for quote in quotes:
            item = Quote()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            # quote.css('.tag .tag::text').re()
            # quote.css('.tag .tag::text').re_first().strip()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        
        # a tag的href包含page
        # next = response.css('.next a[href*=page]::attr(href)').extract_first()   
        # print(next)     
        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)

            

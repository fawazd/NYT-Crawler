# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from scrapy.spiders import CrawlSpider, Rule
from nyt.items import NewsItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

class TestSpider(CrawlSpider):
    name = "nyt" #This name will help while running the crawler itself
    allowed_domains = ["nytimes.com"] #which domains are accessible for this crawler
    start_urls = ['http://spiderbites.nytimes.com/1997/'] #initial URLs that are to be accessed first

    rules = (Rule(LxmlLinkExtractor(
            allow=("1997")),
            follow=True,
            callback='parse_item'),)
		
    def parse_item(self, response):

        if 'articles_1997' not in response.url:
            item = NewsItem()

            item['title'] = response.xpath('//*[@itemprop="headline" or @class="headline"]/text()').extract_first()
            item['author'] = response.xpath('//*[@class="byline-author" or @class="author creator"]/text()').extract_first()
            item['article'] = response.xpath('//*[@class="story-body-text story-content" or @class="css-18sbwfn"]/text()').extract()
            item['dop'] = response.xpath('//*[@itemprop="dateModified" or @class="css-pnci9ceqgapgq0"]/text()').extract_first()
            item['section'] = response.xpath('//*[@id="kicker"]/span/a/text()').extract_first()
            item['url'] = response.url

            yield item
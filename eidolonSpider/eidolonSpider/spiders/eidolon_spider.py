from scrapy import Spider
from eidolonSpider.eidolonSpider.items import EidolonspiderItem
from scrapy.selector import Selector
from random import sample


class EidolonRealSpider(Spider):
    name = "eidolonSpider"
    # start_urls = ["https://stackoverflow.com/questions"]
    myBaseUrl = ''
    start_urls = []

    def __init__(self, category='', **kwargs):
        self.myBaseUrl = category   # "https://stackoverflow.com/questions"    #
        self.start_urls.append(self.myBaseUrl)
        super().__init__(**kwargs)

    def parse(self, response):
        sect = Selector(response).xpath('//div[@class="question-summary"]//h3')
        details = Selector(response).xpath('//div[@class="question-summary"]//div[@class="excerpt"]')

        for idx in sample(range(0, 49), 3):
            item = EidolonspiderItem()
            item['name'] = sect[idx].xpath('a/text()').extract_first()
            item['url'] = sect[idx].xpath('a/@href').extract_first()
            item['story'] = details[idx].xpath('text()').extract_first().strip()[:60] + "..."

            yield item

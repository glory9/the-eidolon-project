from scrapy.item import Item, Field


class EidolonspiderItem(Item):
    name = Field()
    url = Field()
    story = Field()
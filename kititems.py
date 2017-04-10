import scrapy

class kitItem(scrapy.Item):
    bitname = scrapy.Field()
    kitlink = scrapy.Field()
    kitretailprice = scrapy.Field()
    kitname = scrapy.Field()
    bitcount = scrapy.Field()
    kitdescription = scrapy.Field()

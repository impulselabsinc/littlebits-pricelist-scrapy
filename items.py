import scrapy

class lbItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    retailprice = scrapy.Field()
    sku = scrapy.Field()
    upc = scrapy.Field()
    productid = scrapy.Field()
    producttype = scrapy.Field()
    description = scrapy.Field()

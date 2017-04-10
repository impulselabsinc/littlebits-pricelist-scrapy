import scrapy
import pprint
from items import lbItem

class lbSpider(scrapy.Spider):
    # spider name
    name = 'lb'

    # settings for output file
    # automatically quotes strings with commas so need to mess with delimiters
    custom_settings = {
            'FEED_FORMAT': 'csv',
            'FEED_URI': 'allbits.csv'
            }

    allowed_domains = ['littlebits.cc']
    start_urls = ['http://littlebits.cc/shop/bits']

    # parses the shop home and extracts basic properties and links to product detail
    def parse(self, response):
        for entry in response.xpath("//div[@class='ShopCard-content']"):
            item = lbItem()
            bitpage_rel = entry.xpath('a/@href').extract_first()
            item['name'] =  entry.xpath('a/h3/text()').extract_first()
            item['link'] =  response.urljoin(bitpage_rel)
            item['retailprice'] = entry.xpath("h4/span/text()").extract_first()
            item['description'] = entry.xpath("p/text()").extract_first()

            # callback to navigate to the product detail page
            request = scrapy.Request(item['link'], callback=self.parse_item_page)

            # the simplest way to share data with the callback function
            # each shared variable needs to be accessed through 'meta' in both the caller and the callee
            request.meta['item'] = item

            # using 'yield' instead of 'return' - generators weigh less
            yield request
            
            # debug
            #print item
            #print item['name']
            #print item['link']
            #print item['sku']
            #print item['upc']

    # callback to parse details for each bit from the detail page
    def parse_item_page(self, response):

        # the simplest way to share data with the callback function
        # each shared variable needs to be accessed through 'meta' in both the caller and the callee
        item = response.meta['item']

        # get the small bit 'ids' that are on most of the bits
        item['productid'] = response.xpath("//h3/text()").extract_first()

        # get the bit type - input/output/power/wire
        item['producttype'] = response.xpath("//h3/strong/text()").extract_first()

        # get sku/upc
        for p in response.xpath("//div[@class='ProductDetails-list']"):
            if p.xpath("h4/text()").extract_first() == "SKU":
                item['sku'] = p.xpath("p[@class='ProductDetails-item ParagraphXS']/text()").extract_first()
            if p.xpath("h4/text()").extract_first() == "UPC":
                item['upc'] = p.xpath("p[@class='ProductDetails-item ParagraphXS']/text()").extract_first()
        yield item
